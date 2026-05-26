#!/usr/bin/env python3
import shutil
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
TEMPLATES_DIR = ROOT / "templates"
ASSETS_DIR = ROOT / "assets"
OUTPUT_DIR = ROOT / "output"


def load_data():
    path = DATA_DIR / "works.yaml"
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def render(data):
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template("index.html")
    return template.render(**data)


def copy_assets():
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    shutil.copytree(ASSETS_DIR, OUTPUT_DIR / "assets")


def main():
    data = load_data()
    html = render(data)

    copy_assets()

    (OUTPUT_DIR / "index.html").write_text(html, encoding="utf-8")

    print(f"Done. Static site generated at: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
