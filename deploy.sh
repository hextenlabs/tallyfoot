#!/usr/bin/env bash
set -euo pipefail

host="${TALLYFOOT_HOST:-newvps}"
ip="${TALLYFOOT_IP:-107.175.127.15}"
domain="tallyfoot.com"

mode=deploy
case "${1:-}" in
  "") ;;
  --build-only) mode=preview ;;
  *) echo "usage: $0 [--build-only]" >&2; exit 2 ;;
esac

cd "$(dirname "$0")"
sha="$(git rev-parse --short HEAD)"

if [ "$mode" = preview ]; then
  src=preview-src
  out=preview-site
  echo "== upload the working tree (tracked + untracked, not ignored) to $host"
  git ls-files -z -co --exclude-standard | tar --null -cf - -T - | ssh "$host" "
    set -e
    rm -rf ~/tallyfoot/$src
    mkdir -p ~/tallyfoot/$src ~/tallyfoot/$out
    tar -x -C ~/tallyfoot/$src
  "
else
  src=src
  out=site
  if [ -n "$(git status --porcelain)" ]; then
    echo "warning: uncommitted changes are not deployed; deploying committed HEAD $sha" >&2
  fi
  echo "== upload $sha to $host"
  git archive --format=tar HEAD | ssh "$host" "
    set -e
    rm -rf ~/tallyfoot/$src
    mkdir -p ~/tallyfoot/$src ~/tallyfoot/$out
    tar -x -C ~/tallyfoot/$src
  "
fi

echo "== build on $host"
ssh "$host" bash -s -- "$src" "$out" <<'REMOTE'
set -euo pipefail
src="$1"
out="$2"
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
rm -rf ~/tallyfoot/"$out"/*
docker run --rm --cpus 1 --user "$(id -u):$(id -g)" \
  -e HOME=/tmp -e BUNDLE_GEMFILE=/build/Gemfile -e BUNDLE_PATH=/build/gems \
  -v ~/tallyfoot:/build \
  ruby:3.3.4 sh -c "bundle install --quiet && cd /build/$src && bundle exec jekyll build -s /build/$src -d /build/$out --config _config.yml,_config.tallyfoot-com.yml"
test -s ~/tallyfoot/"$out"/index.html
test -s ~/tallyfoot/"$out"/privacy.html
test -s ~/tallyfoot/"$out"/support.html
REMOTE

if [ "$mode" = preview ]; then
  rm -rf _preview
  mkdir -p _preview
  ssh "$host" "tar -C ~/tallyfoot/$out -cf - ." | tar -x -C _preview
  echo "== check the build in _preview"
  python -I tools/check_site.py _preview
  echo "preview of working tree at $sha: ok (not published)"
  exit 0
fi

echo "== publish on $host"
ssh "$host" "rsync -a --delete ~/tallyfoot/site/ /var/www/tallyfoot/web/"

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
listed="$(get "https://$domain/sitemap.xml" | grep -oE "<loc>https://$domain[^<]*</loc>" | sed -E "s#<loc>https://$domain##; s#</loc>##" || true)"
if [ -z "$listed" ]; then
  echo "sitemap.xml lists no pages"
  fail=1
fi
pages="$(printf '%s\n' / /privacy /support /press /apple-watch-step-counter $listed | sort -u)"
refs="$(for page in $pages; do
  get "https://$domain$page" | grep -oE '(href|src)="[^"#]+"' | sed -E 's/^(href|src)="//; s/"$//' | while read -r ref; do
    case "$ref" in
      http*|mailto:*|/*) printf '%s\n' "$ref" ;;
      ./) printf '%s\n' "${page%/*}/" ;;
      *) printf '%s%s\n' "${page%/*}/" "$ref" ;;
    esac
  done || true
done | sort -u)"
for path in $pages /robots.txt /sitemap.xml; do
  check "$path"
done
while read -r ref; do
  case "$ref" in
    "") ;;
    "https://$domain/"*) check "${ref#https://$domain}" ;;
    http*|mailto:*) ;;
    *) check "$ref" ;;
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
