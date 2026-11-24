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
  mkdir -p ~/tallyfoot/src ~/tallyfoot/site ~/tallyfoot/gems
  tar -x -C ~/tallyfoot/src
'

echo "== build and publish on $host"
ssh "$host" bash -s <<'REMOTE'
set -euo pipefail
gems="jekyll:3.10.0 minima:2.5.1 jekyll-seo-tag:2.8.0 jekyll-feed:0.17.0 kramdown:2.4.0 kramdown-parser-gfm:1.1.0 jekyll-sass-converter:1.5.2 sass:3.7.4 rouge:3.30.0 liquid:4.0.4 webrick"
rm -rf ~/tallyfoot/site/*
docker run --rm --cpus 1 --user "$(id -u):$(id -g)" \
  -e HOME=/tmp -e GEM_HOME=/gems -e PATH=/gems/bin:/usr/local/bin:/usr/bin:/bin \
  -v ~/tallyfoot/gems:/gems -v ~/tallyfoot/src:/src -v ~/tallyfoot/site:/out \
  ruby:3.3.4 sh -c "gem install --conservative --no-document $gems >/dev/null && cd /src && jekyll build -s /src -d /out --config _config.yml,_config.tallyfoot-com.yml"
test -s ~/tallyfoot/site/index.html
test -s ~/tallyfoot/site/privacy.html
test -s ~/tallyfoot/site/support.html
rsync -a --delete ~/tallyfoot/site/ /var/www/tallyfoot/web/
REMOTE

echo "== verify https://$domain via $ip"
fail=0
fetch() {
  curl -s -o /dev/null -w '%{http_code}' --max-time 20 --resolve "$domain:443:$ip" "https://$domain$1"
}
check() {
  local code
  code="$(fetch "$1")"
  printf '%s %s\n' "$code" "$1"
  [ "$code" = "200" ] || fail=1
}
for path in / /privacy /support; do
  check "$path"
done
for page in / /privacy /support; do
  curl -s --max-time 20 --resolve "$domain:443:$ip" "https://$domain$page" \
    | grep -oE '(href|src)="[^"#]+"' | sed -E 's/^(href|src)="//; s/"$//' \
    | while read -r ref; do
        case "$ref" in
          https://$domain/*) echo "${ref#https://$domain}" ;;
          http*|mailto:*) ;;
          /*) echo "$ref" ;;
          ./) echo "/" ;;
          *) echo "/$ref" ;;
        esac
      done
done | sort -u > "${TMPDIR:-/tmp}/tallyfoot-refs.txt"
while read -r ref; do
  check "$ref"
done < "${TMPDIR:-/tmp}/tallyfoot-refs.txt"
grep -q "https://$domain/assets/img/og-1200x630.jpg" <(curl -s --max-time 20 --resolve "$domain:443:$ip" "https://$domain/") \
  || { echo "og:image does not point at $domain"; fail=1; }

if [ "$fail" -ne 0 ]; then
  echo "deploy $sha: verification FAILED" >&2
  exit 1
fi
echo "deploy $sha: ok"
