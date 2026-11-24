# Tallyfoot site

The landing page, privacy policy and support page for Tallyfoot. GitHub Pages publishes `main` at https://hextenlabs.github.io/tallyfoot/, and the same source is served at https://tallyfoot.com/.

## Deploy to tallyfoot.com

```
./deploy.sh
```

It uploads the committed `HEAD` to `newvps`, builds it there with Jekyll 3.10 and minima 2.5.1 in a `ruby:3.3.4` container (the GitHub Pages versions), using `_config.tallyfoot-com.yml` for the tallyfoot.com URL. Then it publishes the build to `/var/www/tallyfoot/web`, where Caddy serves it, and checks every page and linked asset over HTTPS against the server's IP.

Uncommitted changes are not deployed.
