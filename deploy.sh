#!/usr/bin/env bash
set -euo pipefail

host="${TALLYFOOT_HOST:-newvps}"
ip="${TALLYFOOT_IP:-107.175.127.15}"
domain="tallyfoot.com"

cd "$(dirname "$0")"
sha="$(git rev-parse --short HEAD)"
if [ -n "$(git status --porcelain)" ]; then
  echo "warning: uncommitted changes are not deployed; deploying committed HEAD $sha" >&2
fi

echo "== upload $sha to $host"
git archive --format=tar HEAD | ssh "$host" '
  set -e
  rm -rf ~/tallyfoot/src
  mkdir -p ~/tallyfoot/src ~/tallyfoot/site
  tar -x -C ~/tallyfoot/src
'

echo "== build and publish on $host"
ssh "$host" bash -s <<'REMOTE'
set -euo pipefail
cat > ~/tallyfoot/Gemfile <<'GEMS'
source "https://rubygems.org"
gem "jekyll", "3.10.0"
gem "minima", "2.5.1"
gem "jekyll-seo-tag", "2.8.0"
gem "jekyll-feed", "0.17.0"
gem "jekyll-sass-converter", "1.5.2"
gem "sass", "3.7.4"
gem "kramdown", "2.4.0"
gem "kramdown-parser-gfm", "1.1.0"
gem "rouge", "3.30.0"
gem "liquid", "4.0.4"
GEMS
rm -rf ~/tallyfoot/site/*
docker run --rm --cpus 1 --user "$(id -u):$(id -g)" \
  -e HOME=/tmp -e BUNDLE_GEMFILE=/build/Gemfile -e BUNDLE_PATH=/build/gems \
  -v ~/tallyfoot:/build \
  ruby:3.3.4 sh -c "bundle install --quiet && cd /build/src && bundle exec jekyll build -s /build/src -d /build/site --config _config.yml,_config.tallyfoot-com.yml"
test -s ~/tallyfoot/site/index.html
test -s ~/tallyfoot/site/privacy.html
test -s ~/tallyfoot/site/support.html
rsync -a --delete ~/tallyfoot/site/ /var/www/tallyfoot/web/
REMOTE

echo "== verify https://$domain via $ip"
fail=0
get() {
  curl -s --max-time 20 --resolve "$domain:443:$ip" "$@" || true
}
check() {
  local code
  code="$(get -o /dev/null -w '%{http_code}' "https://$domain$1")"
  printf '%s %s\n' "$code" "$1"
  [ "$code" = "200" ] || fail=1
}
refs="$(for page in / /privacy /support; do
  get "https://$domain$page" | grep -oE '(href|src)="[^"#]+"' | sed -E 's/^(href|src)="//; s/"$//' || true
done | sort -u)"
for path in / /privacy /support; do
  check "$path"
done
while read -r ref; do
  case "$ref" in
    "") ;;
    "https://$domain/"*) check "${ref#https://$domain}" ;;
    http*|mailto:*) ;;
    /*) check "$ref" ;;
    ./) check / ;;
    *) check "/$ref" ;;
  esac
done <<< "$refs"
if ! get "https://$domain/" | grep -q "https://$domain/assets/img/og-1200x630.jpg"; then
  echo "og:image does not point at $domain"
  fail=1
fi

if [ "$fail" -ne 0 ]; then
  echo "deploy $sha: verification FAILED" >&2
  exit 1
fi
echo "deploy $sha: ok"
