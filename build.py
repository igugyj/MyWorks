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


def main():
    site = load_json("site.json")
    if not site:
        print("Error: data/site.json not found")
        return

    auto_works = load_json("github.json")
    custom_works = load_json("custom.json")
    works = merge_works(auto_works, custom_works)

    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template("index.html")
    html = template.render(site=site, works=works, **site)

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    shutil.copytree(ASSETS_DIR, OUTPUT_DIR / "assets")

    (OUTPUT_DIR / "index.html").write_text(html, encoding="utf-8")

    print(f"Done. {len(works)} works → {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
