# Portfolio Builder — AGENTS.md

## Build & Run

```bash
pip install -r requirements.txt   # jinja2 only
python build.py                    # generates output/
```

Output in `output/` — deploy as static site to Cloudflare Pages / Vercel / Netlify.

## Data Sources (JSON, priority order)

| File | Purpose | Source |
|---|---|---|
| `data/site.json` | **Required.** Site config (title, subtitle, nav, about, links) | Manual |
| `data/custom.json` | Optional. Manually curated works (Chinese descriptions, extra links, images) | Manual |
| `data/github.json` | Optional. Auto-generated via Action — non-fork repos from GitHub API | `scripts/fetch_repos.py` |
| `data/ignore.json` | Optional. Exclude works by `title` or `link.url` (case-sensitive match) | Manual |

**Merge logic** (`build.py:merge_works`):
- `custom.json` entries override `github.json` entries with the same `title` (full replacement)
- Different titles are appended
- Then `filter_works` removes anything matching `ignore.json`
- Then `sort_works` orders by `stars * 10 + recency(30d=+3, 90d=+1)`, descending

No `data/works.yaml` — that was replaced by JSON files.

## GitHub Action

`.github/workflows/fetch-repos.yml`
- Runs weekly (Sun 00:00 UTC) + on push to `mine` + manual dispatch
- Fetches `GET /users/igugyj/repos?type=source`, filters `fork: false`
- Outputs `stars` and `pushed_at` for sorting
- Commits `data/github.json` back using `${{ github.token }}` for auth
- `GITHUB_TOKEN` env var passed to `fetch_repos.py` for API calls

## Structure

```
build.py                         # Entrypoint: read JSON → merge → filter → sort → render → write
scripts/fetch_repos.py           # GitHub API fetcher (called by Action)
templates/
  base.html                      # Shell: nav, modal, back-to-top, feather icons CDN
  index.html                     # Content: hero, work cards, about, links sections
assets/
  css/style.css                  # Full stylesheet, dark/light via CSS vars + data-theme attr
  js/main.js                     # Modal, theme toggle, back-to-top
  font/                          # Maple Mono woff2 (OFL licensed, OFL.txt included)
output/                          # gitignored, build artifact
```

## Conventions

- **No emoji anywhere.** Icons via Feather Icons CDN (`<i data-feather="...">`)
- **No images on homepage cards.** Modal optionally shows image if `work.image` exists
- **Tags default to `[language]`** from GitHub API. Empty tags → no tag section rendered (`templates/index.html` checks `work.tags` length)
- **Branch: `mine`** (not `main`). Action pushes to `mine`.
- **Font:** Maple Mono (via `@font-face`), falls back to system-ui stack
- **Card click** opens detail modal (no button needed, whole card clickable)
