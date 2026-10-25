#!/usr/bin/env python3
import json
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
TEMPLATES_DIR = ROOT / "templates"
ASSETS_DIR = ROOT / "assets"
OUTPUT_DIR = ROOT / "output"


def load_json(name):
    path = DATA_DIR / name
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def merge_works(autos, customs):
    if not autos:
        return customs or []
    if not customs:
        return autos

    auto_map = {w["title"]: w for w in autos}
    for custom in customs:
        auto_map[custom["title"]] = custom
    return list(auto_map.values())


def load_ignore():
    path = DATA_DIR / "ignore.json"
    if not path.exists():
        return {"titles": [], "urls": []}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def filter_works(works, ignore):
    if not ignore or (not ignore.get("titles") and not ignore.get("urls")):
        return works
    ignore_titles = set(ignore.get("titles", []))
    ignore_urls = set(ignore.get("urls", []))
    result = []
    for w in works:
        if w["title"] in ignore_titles:
            continue
        urls = {link["url"] for link in w.get("links", [])}
        if urls & ignore_urls:
            continue
        result.append(w)
    return result


def normalize_item(item):
    out = dict(item)
    out.setdefault("title", "")
    desc = out.get("description") or out["title"]
    out["description"] = desc
    out.setdefault("detail", desc)
    out.setdefault("tags", [])
    out.setdefault("links", [])
    return out


def load_categories():
    data = load_json("categories.json")
    if not data:
        return []
    result = []
    for cat in data:
        name = cat.get("category")
        items = [normalize_item(i) for i in cat.get("items", []) if i.get("title")]
        if not name or not items:
            continue
        result.append({"category": name, "items": items})
    return result


def load_contributions():
    data = load_json("participation.json")
    if not data:
        return []
    ignore = load_ignore() or {}
    ignore_owners = set(ignore.get("owners", []))
    ignore_repos = set(ignore.get("repos", []))
    result = []
    for c in data:
        name = c.get("title", "")
        owner = name.split("/", 1)[0]
        if owner in ignore_owners or name in ignore_repos:
            continue
        result.append(normalize_item(c))
    result.sort(key=lambda c: c.get("last_activity", ""), reverse=True)
    return result


def load_mentors():
    data = load_json("mentors.json")
    if not data:
        return []
    result = []
    for m in data:
        name = m.get("name")
        link = m.get("link")
        if not name or not link:
            continue
        result.append({"name": name, "avatar": m.get("avatar", ""), "link": link})
    return result


def build_modal_data(works, categories, contributions):
    modal = [normalize_item(w) for w in works]
    for cat in categories:
        for item in cat["items"]:
            item["index"] = len(modal)
            modal.append(item)
    for c in contributions:
        c["index"] = len(modal)
        modal.append(c)
    return modal


def sort_works(works):
    from datetime import datetime, timezone
    def score(w):
        stars = w.get("stars", 0) or 0
        s = stars * 10
        pushed = w.get("pushed_at", "")
        if pushed:
            try:
                days = (datetime.now(timezone.utc) -
                        datetime.fromisoformat(pushed.replace("Z", "+00:00"))).days
                if days <= 30:
                    s += 3
                elif days <= 90:
                    s += 1
            except Exception:
                pass
        return s
    return sorted(works, key=score, reverse=True)


def main():
    site = load_json("site.json")
    if not site:
        print("Error: data/site.json not found")
        return

    auto_works = load_json("github.json")
    custom_works = load_json("custom.json")
    works = merge_works(auto_works, custom_works)
    works = filter_works(works, load_ignore())
    works = sort_works(works)

    categories = load_categories()
    contributions = load_contributions()
    mentors = load_mentors()
    modal_data = build_modal_data(works, categories, contributions)

    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template("index.html")
    html = template.render(site=site, works=works, categories=categories,
                           contributions=contributions, mentors=mentors,
                           modal_data=modal_data, **site)

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    shutil.copytree(ASSETS_DIR, OUTPUT_DIR / "assets")

    (OUTPUT_DIR / "index.html").write_text(html, encoding="utf-8")

    print(f"Done. {len(works)} works → {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
