"""Check that every s.dhamma.gift sutta link in docs/ returns HTTP 200 and that its #anchor id exists on the page."""

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

from tools.printer import printer as pr

ROOT_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT_DIR / "docs"
CACHE_DIR = ROOT_DIR / "temp" / "sutta_link_ids"
URL_RE = re.compile(r"https://s\.dhamma\.gift[^)\s\"'<>]*")
ID_RE = re.compile(r'"id":\s*"([^"]*)"|\bid="([^"]*)"')


def extract_ids(html: str) -> set[str]:
    """Collect ids from the page's embedded JSON data and from plain id attributes."""
    return {a or b for a, b in ID_RE.findall(html)}


def fragment_ok(fragment: str, ids: set[str]) -> bool:
    """An anchor is valid if the page resolves it: an id, `<fragment>/0` (dhp), or a merged range id (sn35.192-194)."""
    if fragment in ids or f"{fragment}/0" in ids:
        return True
    m = re.fullmatch(r"([a-z][a-z0-9-]*?\d+)\.(\d+)", fragment)
    if not m:
        return False
    prefix, n = m.group(1), int(m.group(2))
    for i in ids:
        r = re.fullmatch(re.escape(prefix) + r"\.(\d+)-(\d+)", i)
        if r and int(r.group(1)) <= n <= int(r.group(2)):
            return True
    return False


def collect_urls(paths: list[Path]) -> dict[str, set[Path]]:
    """Map every distinct s.dhamma.gift URL to the files that use it."""
    found: dict[str, set[Path]] = {}
    for root in paths:
        files = [root] if root.is_file() else sorted(root.rglob("*.md"))
        for path in files:
            for url in URL_RE.findall(path.read_text(encoding="utf-8")):
                found.setdefault(url, set()).add(path)
    return found


def page_ids(page_url: str, refresh: bool) -> tuple[int, set[str]]:
    """Return (HTTP status, ids) for a page, fetching once and caching the ids."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache = CACHE_DIR / (re.sub(r"\W+", "_", page_url) + ".json")
    if cache.exists() and not refresh:
        data = json.loads(cache.read_text(encoding="utf-8"))
        return data["status"], set(data["ids"])
    try:
        with urllib.request.urlopen(page_url, timeout=60) as resp:
            status = resp.status
            ids = extract_ids(resp.read().decode("utf-8", errors="replace"))
    except urllib.error.HTTPError as e:
        status, ids = e.code, set()
    except (urllib.error.URLError, TimeoutError):
        return 0, set()  # network failure: reported, never cached
    cache.write_text(
        json.dumps({"status": status, "ids": sorted(ids)}), encoding="utf-8"
    )
    return status, ids


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths", nargs="*", type=Path, help="files/dirs to scan (default: docs/)"
    )
    parser.add_argument("--refresh", action="store_true", help="ignore the id cache")
    args = parser.parse_args()

    urls = collect_urls(args.paths or [DOCS_DIR])
    pages = sorted({u.split("#")[0] for u in urls})
    pr.green_tmr(f"checking {len(urls)} links, {len(pages)} pages")
    cache = {p: page_ids(p, args.refresh) for p in pages}
    failures: list[str] = []
    for url in sorted(urls):
        page, _, fragment = url.partition("#")
        status, ids = cache[page]
        where = ", ".join(
            sorted(
                str(p.relative_to(ROOT_DIR)) if p.is_relative_to(ROOT_DIR) else str(p)
                for p in urls[url]
            )[:2]
        )
        if status != 200:
            failures.append(f"HTTP {status}: {url}  ({where})")
        elif fragment and not fragment_ok(fragment, ids):
            failures.append(f"missing id: {url}  ({where})")
    if failures:
        pr.no(f"{len(failures)} failed")
        for f in failures:
            pr.amber(f)
        return 1
    pr.yes("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
