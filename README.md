# MyWorks

基于 Python 的静态作品集站点生成器，生成纯静态 HTML/CSS/JS，可部署到 Cloudflare Pages、Vercel、Netlify 等平台。

## 使用

```bash
pip install -r requirements.txt
python build.py
```

构建产物在 `output/` 目录。

## 页面板块

Hero → Works（作品）→ Ecosystems（按社区细分的项目）→ Contributions（参与过的开源项目）→ About → Links

- **Works**：自己的仓库，GitHub 自动同步 + 手动补充
- **Ecosystems**：手动维护，按社区分组（Firefox、VSCode、greasyfork 等）
- **Contributions**：自动同步，在他人仓库发起的 issue / PR，按最近活动排序

卡片点击弹出详情窗（tags、介绍、链接、参与明细）。

## 数据源

Works 数据：JSON 合并，优先级 `custom.json` > `github.json`（同名覆盖，不同名追加）。

| 文件                      | 说明                                            | 维护方式 |
| ------------------------- | ----------------------------------------------- | -------- |
| `data/site.json`          | 站点配置（标题、导航、板块标题、简介、外链）    | 手动     |
| `data/custom.json`        | 手动维护的作品（中文描述、额外链接、配图）      | 手动     |
| `data/categories.json`    | Ecosystems 板块，按社区分组的项目               | 手动     |
| `data/github.json`        | GitHub 仓库自动同步（Action 每周生成）          | 自动     |
| `data/participation.json` | 参与的外部仓库自动同步（Action 每周生成）       | 自动     |
| `data/ignore.json`        | 排除规则（见下）                                | 手动     |

### 排除规则（`data/ignore.json`）

```json
{
  "owners": ["igugyj"],
  "repos": ["owner/repo"],
  "titles": ["repo-name"],
  "urls": ["https://github.com/owner/repo"]
}
```

- `owners`：排除这些账号名下的所有仓库（Works 和 Contributions 都生效）
- `repos`：按 `owner/repo` 精确排除 Contributions 条目
- `titles` / `urls`：按标题或链接排除 Works 条目

## 文件结构

```
├── build.py                  # 构建脚本
├── scripts/
│   ├── fetch_repos.py        # GitHub 仓库抓取（Action 调用）
│   └── fetch_participation.py# 参与数据抓取（Action 调用）
├── data/                     # JSON 数据源
│   ├── site.json
│   ├── custom.json
│   ├── categories.json
│   ├── github.json
│   ├── participation.json
│   └── ignore.json
├── templates/
│   ├── base.html             # HTML 骨架（导航、弹窗、页脚）
│   └── index.html            # 首页内容
├── assets/
│   ├── css/style.css         # 样式（深浅色模式，Maple Mono 字体）
│   ├── js/main.js            # 交互（弹窗、主题切换、回到顶部）
│   ├── images/               # 配图目录
│   └── font/                 # Maple Mono woff2（OFL 协议）
├── output/                   # 构建产物（可上传部署）
└── requirements.txt          # jinja2
```

## GitHub Action

每周日 00:00 UTC 自动运行（也支持 push 和手动触发）：

1. `fetch_repos.py`：抓取 GitHub 非 fork 仓库，按星数和推送时间排序，生成 `data/github.json`
2. `fetch_participation.py`：用 Search API 抓取在他人仓库发起的 issue/PR，按仓库聚合生成 `data/participation.json`

生成的数据自动 commit 回仓库。

## 部署

将 `output/` 目录上传至 Cloudflare Pages 即可。
