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
| `data/categories.json` | Optional. Ecosystem section — projects grouped by community (Firefox, VSCode, greasyfork, ...) | Manual |
| `data/github.json` | Optional. Auto-generated via Action — non-fork repos from GitHub API | `scripts/fetch_repos.py` |
| `data/participation.json` | Optional. Auto-generated via Action — external repos where user opened issues/PRs | `scripts/fetch_participation.py` |
| `data/ignore.json` | Optional. Exclusion rules (see below) | Manual |

**`ignore.json` keys**:
- `titles` — hide works by exact `title` match
- `urls` — hide works by any `links[].url` match
- `owners` — skip all repos owned by these accounts (works + contributions); auto-applied in `fetch_participation.py` query (`-user:` qualifier) and again at build time
- `repos` — skip specific `owner/repo` in contributions (works use `titles`/`urls` instead)

**Merge logic** (`build.py:merge_works`):
- `custom.json` entries override `github.json` entries with the same `title` (full replacement)
- Different titles are appended
- Then `filter_works` removes anything matching `ignore.json`
- Then `sort_works` orders by `stars * 10 + recency(30d=+3, 90d=+1)`, descending

**Ecosystems** (`build.py:load_categories`):
- `categories.json` is fully independent — not merged with GitHub/custom works, not sorted, not filtered by `ignore.json`
- Order follows the JSON file: category order and item order within each category
- Missing `detail` falls back to `description`; missing `tags`/`links` normalize to `[]` (modal JS requires these keys)
- Empty categories (no titled items) are skipped; if all empty, the whole section is not rendered
- Category cards reuse the same detail modal via a shared `modal_data` array (category items appended after works)

**Contributions** (`build.py:load_contributions`):
- `participation.json` is auto-generated; each entry is one external repo aggregated from user-authored issues/PRs
- `build.py` re-applies `owners`/`repos` exclusions at render time, then sorts by `last_activity` descending
- `tags` are generated badges: `Issue ×N`, `PR ×N（M 已合并）`, `Fork` (fork badge only if user forked that repo)
- `participation` array holds per-item detail (`type`/`title`/`url`/`state`/`date`) rendered inside the modal by `main.js`
- Appended to `modal_data` after works + ecosystem items; section hidden if list is empty

No `data/works.yaml` — that was replaced by JSON files.

## GitHub Action

`.github/workflows/fetch-repos.yml`
- Runs weekly (Sun 00:00 UTC) + on push to `mine` + manual dispatch
- `fetch_repos.py`: `GET /users/igugyj/repos?type=source`, filters `fork: false`; outputs `stars` and `pushed_at` for sorting
- `fetch_participation.py`: Search API `author:igugyj -user:<ignored owners>` for issues/PRs, aggregated per repo; `users/igugyj/repos?type=forks` for fork badges; one `repos/{owner}/{repo}` call per participated repo for descriptions
- Commits `data/github.json` + `data/participation.json` back using `${{ github.token }}` for auth
- `GITHUB_TOKEN` env var passed to both scripts; Search API quota (30/min) and core quota (1000/hr) are far above actual usage (~10–20 calls total)

## Structure

```
build.py                         # Entrypoint: read JSON → merge → filter → sort → render → write
scripts/fetch_repos.py           # GitHub API fetcher (called by Action)
scripts/fetch_participation.py   # Issues/PRs participation fetcher (called by Action)
data/
  site.json                      # Required: title, nav, section titles, about, links
  custom.json                    # Manual works (override/extend github.json)
  categories.json                # Ecosystem section: grouped by community, modal-ready
  github.json                    # Auto-fetched by Action (do not edit by hand)
  participation.json             # Auto-fetched by Action (do not edit by hand)
  ignore.json                    # Exclusion rules: titles/urls/owners/repos
templates/
  base.html                      # Shell: nav, modal, back-to-top, feather icons CDN
  index.html                     # Content: hero, works, ecosystems, contributions, about, links sections
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
