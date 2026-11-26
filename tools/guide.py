import argparse
import datetime
import os
import re
import subprocess
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
GUIDES = SITE / "_guides"
BRIEF = Path(__file__).resolve().parent / "guide-brief.md"
APP_REPO = Path(os.environ.get("TALLYFOOT_APP_REPO", r"C:\Data\Repos\Tallyfoot"))
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONT = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.S)
HYPE = re.compile(
    r"\b(revolutionary|game[- ]changer|ultimate|best-in-class|seamless(ly)?|effortless(ly)?|"
    r"unlock|supercharge|elevate|delve|must-have|cutting-edge|world-class|amazing|incredible)\b",
    re.I,
)
EMOJI = re.compile("[\u2600-\u27bf\U0001f000-\U0001faff]")
MIN_WORDS, MAX_WORDS = 500, 1500


def front_matter(text: str) -> tuple[dict, str]:
    m = FRONT.match(text.replace("\r\n", "\n"))
    if not m:
        raise ValueError("no front matter block")
    meta: dict = {}
    key = None
    for line in m.group(1).split("\n"):
        if line.startswith("  - ") and key:
            meta.setdefault(key, []).append(line[4:].strip())
        elif ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            meta[key] = value.strip('"') if value else []
    return meta, m.group(2)


def check_file(path: Path, seen_ct: dict[str, Path]) -> list[str]:
    problems: list[str] = []
    try:
        meta, body = front_matter(path.read_text(encoding="utf-8"))
    except ValueError as e:
        return [str(e)]
    slug = path.stem
    if not SLUG.match(slug):
        problems.append(f"file name {slug!r} is not a lowercase-hyphen slug")
    if meta.get("layout") != "guide":
        problems.append("layout must be guide")
    for key in ("title", "description", "lede", "ct", "date"):
        if not isinstance(meta.get(key), str) or not meta.get(key):
            problems.append(f"missing {key}")
    desc = meta.get("description") if isinstance(meta.get("description"), str) else ""
    if desc and not 50 <= len(desc) <= 160:
        problems.append(f"description is {len(desc)} chars; keep it 50-160")
    for key in ("title", "description", "lede"):
        if '"' in str(meta.get(key, "")):
            problems.append(f"{key} contains a double quote")
    ct = meta.get("ct") if isinstance(meta.get("ct"), str) else ""
    if ct:
        if not re.fullmatch(r"guide-[a-z0-9-]+", ct) or len(ct) > 30:
            problems.append(f"ct {ct!r} must match guide-[a-z0-9-]+ and be at most 30 chars")
        if ct in seen_ct and seen_ct[ct] != path:
            problems.append(f"ct {ct!r} is also used by {seen_ct[ct].name}")
        seen_ct[ct] = path
    try:
        datetime.date.fromisoformat(str(meta.get("date", "")))
    except ValueError:
        problems.append("date must be YYYY-MM-DD")
    sources = meta.get("sources")
    if not isinstance(sources, list) or not sources or not all(re.fullmatch(r"https://[^\s/]+\.[^\s/]+\S*", s) for s in sources):
        problems.append("sources must list at least one https URL")
    if "STORE_URL" not in body:
        problems.append("body never links Tallyfoot as [Tallyfoot](STORE_URL)")
    if "apps.apple.com" in body:
        problems.append("body hard-codes an App Store link; use STORE_URL")
    if re.search(r"\]\(/", body):
        problems.append("body links a bare /path; use {{ \"/path\" | relative_url }}")
    if re.search(r"^# ", body, re.M):
        problems.append("body has a # heading; the page prints the title")
    if "!" in re.sub(r"!\[", "", body):
        problems.append("body has an exclamation mark")
    for word in sorted({m.group(0).lower() for m in HYPE.finditer(body)}):
        problems.append(f"hype word: {word}")
    if EMOJI.search(body):
        problems.append("body has an emoji")
    words = len(re.findall(r"[A-Za-z0-9']+", body))
    if not MIN_WORDS <= words <= MAX_WORDS:
        problems.append(f"body is {words} words; keep it {MIN_WORDS}-{MAX_WORDS}")
    return problems


def cmd_check(args: argparse.Namespace) -> int:
    files = [Path(p) for p in args.files] or sorted(GUIDES.glob("*.md"))
    if not files:
        print("no guides to check")
        return 1
    seen: dict[str, Path] = {}
    failed = 0
    for f in sorted(GUIDES.glob("*.md")):
        try:
            meta, _ = front_matter(f.read_text(encoding="utf-8"))
            if isinstance(meta.get("ct"), str):
                seen.setdefault(meta["ct"], f)
        except ValueError:
            pass
    for f in files:
        problems = check_file(f.resolve(), seen)
        print(f"{'FAIL' if problems else 'ok  '} {f.name}")
        for p in problems:
            print(f"     - {p}")
        failed += bool(problems)
    return 1 if failed else 0


def ct_for(slug: str, ct: str | None = None) -> str:
    if ct:
        return ct
    token = "guide-" + slug
    if len(token) > 30:
        raise SystemExit(f"{token!r} is over 30 chars; pass --ct guide-<short-name>")
    return token


def scaffold(slug: str, title: str, ct: str | None) -> str:
    return (
        "---\n"
        "layout: guide\n"
        f"title: {title}\n"
        "description: \n"
        "lede: \n"
        f"ct: {ct_for(slug, ct)}\n"
        f"date: {datetime.date.today().isoformat()}\n"
        "sources:\n"
        "  - https://\n"
        "---\n"
        "## \n\n"
        "[Tallyfoot](STORE_URL)\n"
    )


def cmd_new(args: argparse.Namespace) -> int:
    if not SLUG.match(args.slug):
        print(f"slug {args.slug!r} must be lowercase words joined by hyphens")
        return 2
    path = GUIDES / f"{args.slug}.md"
    if path.exists():
        print(f"{path} already exists")
        return 1
    GUIDES.mkdir(exist_ok=True)
    path.write_text(scaffold(args.slug, args.title, args.ct), encoding="utf-8", newline="\n")
    print(path)
    return 0


def app_doc(rel: str) -> str:
    subprocess.run(["git", "-C", str(APP_REPO), "fetch", "-q", "origin", "main"], check=True)
    return subprocess.run(
        ["git", "-C", str(APP_REPO), "show", f"origin/main:{rel}"],
        check=True, capture_output=True, text=True, encoding="utf-8",
    ).stdout


def existing_titles() -> list[str]:
    titles = ["How to put a step counter on your Apple Watch face (/apple-watch-step-counter)"]
    for f in sorted(GUIDES.glob("*.md")):
        try:
            titles.append(f"{front_matter(f.read_text(encoding='utf-8'))[0].get('title')} (/guides/{f.stem})")
        except ValueError:
            pass
    return titles


def cmd_draft(args: argparse.Namespace) -> int:
    if not SLUG.match(args.slug):
        print(f"slug {args.slug!r} must be lowercase words joined by hyphens")
        return 2
    path = GUIDES / f"{args.slug}.md"
    if path.exists() and not args.force:
        print(f"{path} already exists; pass --force to replace it")
        return 1
    listing = app_doc("docs/store/listing.md").split("## What's New", 1)[0]
    today = datetime.date.today().isoformat()
    prompt = f"""You are writing one guide page for tallyfoot.com, the site for Tallyfoot, a free step-goal app for Apple Watch and iPhone.

Topic: {args.topic}

Follow this brief exactly:

{BRIEF.read_text(encoding="utf-8")}

## The App Store listing (the only source for claims about Tallyfoot)

{listing}

## Guides that already exist (do not repeat them; you may link one with a site-relative link)

{chr(10).join("- " + t for t in existing_titles())}

## Research

Use WebSearch and WebFetch now to confirm every claim about Apple Watch, iPhone, Apple Health, and any other app you name. Prefer support.apple.com and each app's own App Store page or site. Leave out anything you cannot confirm.

## Output

Reply with the finished Markdown file and nothing else: no preamble, no code fence. It must start with this front matter, filled in:

---
layout: guide
title: <the question, phrased as a search would phrase it, under 65 characters, no double quotes>
description: <50-160 characters, no double quotes>
lede: <one or two sentences that answer the question, no double quotes>
ct: {ct_for(args.slug, args.ct)}
date: {today}
sources:
  - <each https URL you fetched and relied on, one per line>
---
"""
    print(f"== drafting {path.name} with claude (web research on, no file access)", file=sys.stderr)
    result = subprocess.run(
        ["claude", "-p", "--output-format", "text", "--allowedTools", "WebSearch", "WebFetch"],
        input=prompt, capture_output=True, text=True, encoding="utf-8", timeout=args.timeout,
    )
    if result.returncode != 0:
        print(result.stderr or result.stdout)
        return result.returncode
    text = result.stdout.strip()
    start = text.find("---\nlayout: guide")
    if start < 0:
        print("draft has no front matter; raw output follows\n")
        print(text)
        return 1
    GUIDES.mkdir(exist_ok=True)
    path.write_text(text[start:] + "\n", encoding="utf-8", newline="\n")
    print(path)
    return cmd_check(argparse.Namespace(files=[str(path)]))


def main() -> int:
    parser = argparse.ArgumentParser(prog="guide", description="Write and check tallyfoot.com guides.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("new", help="scaffold an empty guide")
    p.add_argument("slug")
    p.add_argument("--title", required=True)
    p.add_argument("--ct", help="campaign token, guide-<name>, at most 30 chars")
    p.set_defaults(func=cmd_new)
    p = sub.add_parser("draft", help="have claude research and write a guide")
    p.add_argument("slug")
    p.add_argument("--topic", required=True)
    p.add_argument("--force", action="store_true")
    p.add_argument("--ct", help="campaign token, guide-<name>, at most 30 chars")
    p.add_argument("--timeout", type=int, default=1200)
    p.set_defaults(func=cmd_draft)
    p = sub.add_parser("check", help="lint guides (all of them by default)")
    p.add_argument("files", nargs="*")
    p.set_defaults(func=cmd_check)
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
