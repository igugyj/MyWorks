#!/usr/bin/env python3
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
USERNAME = "igugyj"


def fetch_json(url):
    headers = {"User-Agent": "fetch-repos/1.0", "Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    req = Request(url, headers=headers)
    with urlopen(req) as resp:
        return json.loads(resp.read())


def main():
    repos = fetch_json(f"https://api.github.com/users/{USERNAME}/repos?per_page=100&type=source")

    result = []
    for repo in repos:
        if repo.get("fork"):
            continue

        language = repo.get("language")
        tags = [language] if language else []

        links = [{"label": "GitHub", "url": repo["html_url"]}]

        desc = repo.get("description") or ""

        result.append({
            "title": repo["name"],
            "description": desc,
            "detail": desc,
            "tags": tags,
            "links": links,
        })

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "github.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Fetched {len(result)} repos → data/github.json")


if __name__ == "__main__":
    main()
