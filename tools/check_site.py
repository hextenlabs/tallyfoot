import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

DOMAIN = "https://tallyfoot.com"
REF = re.compile(r'(?:href|src)="([^"#]+)"')
LOC = re.compile(r"<loc>([^<]+)</loc>")


def resolve(root: Path, path: str) -> Path | None:
    rel = path.lstrip("/")
    target = root / rel
    candidates = [target / "index.html"] if path.endswith("/") or not rel else [target, root / f"{rel}.html"]
    return next((c for c in candidates if c.is_file()), None)


def site_path(root: Path, page: Path) -> str:
    rel = page.relative_to(root).as_posix()
    if rel.endswith("index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel[: -len(".html")] if rel.endswith(".html") else "/" + rel


def main() -> int:
    root = Path(sys.argv[1]).resolve()
    missing: list[str] = []
    pages = sorted(root.rglob("*.html"))
    if not pages:
        print(f"no html under {root}")
        return 1
    for page in pages:
        base = site_path(root, page)
        base_dir = base if base.endswith("/") else base.rsplit("/", 1)[0] + "/"
        for ref in REF.findall(page.read_text(encoding="utf-8")):
            ref = ref.replace("&amp;", "&")
            if ref.startswith(DOMAIN):
                ref = ref[len(DOMAIN):] or "/"
            elif ref.startswith(("http:", "https:", "mailto:")):
                continue
            path = urlsplit(ref).path
            if not path.startswith("/"):
                path = base_dir + (path[2:] if path.startswith("./") else path)
            if resolve(root, path) is None:
                missing.append(f"{base} -> {ref}")
    sitemap = root / "sitemap.xml"
    locs = LOC.findall(sitemap.read_text(encoding="utf-8")) if sitemap.is_file() else []
    if not locs:
        missing.append("sitemap.xml lists no pages")
    for loc in locs:
        path = loc[len(DOMAIN):] if loc.startswith(DOMAIN) else None
        if path is None or resolve(root, path or "/") is None:
            missing.append(f"sitemap -> {loc}")
    for line in missing:
        print("MISSING", line)
    print(f"checked {len(pages)} pages, {len(locs)} sitemap entries, {len(missing)} problems")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
