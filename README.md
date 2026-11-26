# Tallyfoot site

The landing page, privacy policy and support page for Tallyfoot. GitHub Pages publishes `main` at https://hextenlabs.github.io/tallyfoot/, and the same source is served at https://tallyfoot.com/.

## Deploy to tallyfoot.com

```
./deploy.sh
```

It uploads the committed `HEAD` to `newvps`, builds it there with Jekyll 3.10 and minima 2.5.1 in a `ruby:3.3.4` container (the GitHub Pages versions), using `_config.tallyfoot-com.yml` for the tallyfoot.com URL. Then it publishes the build to `/var/www/tallyfoot/web`, where Caddy serves it, and checks every page and linked asset over HTTPS against the server's IP.

Uncommitted changes are not deployed.

To build the working tree (including uncommitted files) without publishing, and check every internal link and sitemap entry in the result:

```
./deploy.sh --build-only
```

The build lands in `_preview/`.

## Guides

Guides are Markdown files in `_guides/`, published at `/guides/<slug>`, listed at `/guides/` and in `sitemap.xml`. `tools/guide-brief.md` holds the house rules and the topic backlog.

```
python tools/guide.py draft <slug> --topic "<the question>"   # claude researches and writes it
python tools/guide.py new <slug> --title "<title>"            # empty scaffold to write by hand
python tools/guide.py check                                   # lint every guide
```

`draft` gives claude only web search and fetch, reads Tallyfoot claims from the app repo's `docs/store/listing.md` on `origin/main`, and lints the result. Read every draft and open its `sources` before committing: the lint cannot tell a true claim from a false one.

Each guide gets its own App Store campaign token, `ct=guide-<slug>`.
