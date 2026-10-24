#!/usr/bin/env python3
import json
import os
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
USERNAME = "igugyj"


def fetch_json(url):
    headers = {"User-Agent": "fetch-participation/1.0", "Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    req = Request(url, headers=headers)
    with urlopen(req) as resp:
        return json.loads(resp.read())


def load_ignore():
    path = DATA_DIR / "ignore.json"
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def fetch_authored_items(owners):
    """All issues/PRs authored by USERNAME, excluding repos owned by `owners`."""
    qualifiers = f"author:{USERNAME}" + "".join(f" -user:{o}" for o in owners)
    items = []
    page = 1
    while page <= 10:  # Search API caps at 1000 results
        url = ("https://api.github.com/search/issues?q=" + quote(qualifiers) +
               f"&sort=updated&order=desc&per_page=100&page={page}")
        data = fetch_json(url)
        batch = data.get("items", [])
        items.extend(batch)
        if len(batch) < 100 or len(items) >= data.get("total_count", 0):
            break
        page += 1
    return items


def fetch_fork_names():
    """Names of repos forked by USERNAME (used for the Fork badge)."""
    names = set()
    page = 1
    while True:
        batch = fetch_json(f"https://api.github.com/users/{USERNAME}/repos?type=forks&per_page=100&page={page}")
        for repo in batch:
            names.add(repo["name"])
        if len(batch) < 100:
            break
        page += 1
    return names


def repo_full_name(item):
    return item["repository_url"].split("/repos/")[-1]


def main():
    ignore = load_ignore()
    owners = ignore.get("owners", [USERNAME])
    ignore_repos = set(ignore.get("repos", []))

    items = fetch_authored_items(owners)

    # Aggregate per repo: separate issues and PRs
    repos = {}
    for it in items:
        name = repo_full_name(it)
        owner = name.split("/", 1)[0]
        if owner in owners or name in ignore_repos:
            continue
        entry = repos.setdefault(name, {"issues": [], "prs": []})
        if "pull_request" in it:
            merged = bool(it["pull_request"].get("merged_at"))
            entry["prs"].append({
                "type": "pr",
                "title": it["title"],
                "url": it["html_url"],
                "state": "merged" if merged else it["state"],
                "date": it.get("created_at", ""),
            })
        else:
            entry["issues"].append({
                "type": "issue",
                "title": it["title"],
                "url": it["html_url"],
                "state": it["state"],
                "date": it.get("created_at", ""),
            })

    fork_names = fetch_fork_names()

    result = []
    for name, entry in repos.items():
        issues = entry["issues"]
        prs = entry["prs"]
        if not issues and not prs:
            continue

        # Repo description (best effort; repo may be renamed/deleted)
        desc = ""
        try:
            info = fetch_json(f"https://api.github.com/repos/{name}")
            desc = info.get("description") or ""
        except Exception:
            pass

        tags = []
        if issues:
            tags.append(f"Issue ×{len(issues)}")
        if prs:
            merged = sum(1 for p in prs if p["state"] == "merged")
            tags.append(f"PR ×{len(prs)}" + (f" ({merged} merged)" if merged else ""))
        if name.split("/", 1)[1] in fork_names:
            tags.append("Fork")

        parts = []
        if issues:
            parts.append(f"{len(issues)} issue{'s' if len(issues) != 1 else ''}")
        if prs:
            merged = sum(1 for p in prs if p["state"] == "merged")
            parts.append(f"{len(prs)} PR" + (f" ({merged} merged)" if merged else ""))
        detail = "Participation: " + ", ".join(parts)

        participation = issues + prs
        participation.sort(key=lambda p: p["date"], reverse=True)
        last_activity = max((p["date"] for p in participation), default="")

        result.append({
            "title": name,
            "description": desc or detail,
            "detail": detail,
            "tags": tags,
            "links": [{"label": "GitHub", "url": f"https://github.com/{name}"}],
            "participation": participation,
            "last_activity": last_activity,
        })

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "participation.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Fetched {len(result)} participated repos → data/participation.json")


if __name__ == "__main__":
    main()
