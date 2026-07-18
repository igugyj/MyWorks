# MyWorks

基于 Python 的静态作品集站点生成器，生成纯静态 HTML/CSS/JS，可部署到 Cloudflare Pages、Vercel、Netlify 等平台。

## 使用

```bash
pip install -r requirements.txt
python build.py
```

构建产物在 `output/` 目录。

## 数据源

JSON 文件合并，优先级 `custom.json` > `github.json`（同名覆盖，不同名追加）。

| 文件               | 说明                                       | 维护方式 |
| ------------------ | ------------------------------------------ | -------- |
| `data/site.json`   | 站点配置（标题、导航、简介、外链）         | 手动     |
| `data/custom.json` | 手动维护的作品（中文描述、额外链接、配图） | 手动     |
| `data/github.json` | GitHub 仓库自动同步（Action 每周生成）     | 自动     |
| `data/ignore.json` | 按标题或链接排除作品                       | 手动     |

## 文件结构

```
├── build.py              # 构建脚本
├── scripts/fetch_repos.py# GitHub API 抓取（Action 调用）
├── data/                 # JSON 数据源
│   ├── site.json
│   ├── custom.json
│   ├── github.json
│   └── ignore.json
├── templates/
│   ├── base.html         # HTML 骨架（导航、弹窗、页脚）
│   └── index.html        # 首页内容
├── assets/
│   ├── css/style.css     # 样式（深浅色模式，Maple Mono 字体）
│   ├── js/main.js        # 交互（弹窗、主题切换、回到顶部）
│   ├── images/           # 配图目录
│   └── font/             # Maple Mono woff2（OFL 协议）
├── output/               # 构建产物（可上传部署）
└── requirements.txt      # jinja2
```

## GitHub Action

每周日 00:00 UTC 自动抓取 GitHub 非 fork 仓库，按星数和推送时间排序，生成 `data/github.json`。

## 部署

将 `output/` 目录上传至 Cloudflare Pages 即可。
