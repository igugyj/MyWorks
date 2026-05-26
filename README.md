# MyWorks

基于 Python 的静态作品集站点生成器，生成纯静态 HTML/CSS/JS，可部署到 Cloudflare Pages、Vercel、Netlify 等平台。

## 使用

```bash
pip install -r requirements.txt
python build.py
```

构建产物在 `output/` 目录。

## 自定义

编辑 `data/works.yaml` 修改站点信息和作品数据：

| 字段            | 说明                                               |
| --------------- | -------------------------------------------------- |
| `site.title`    | 站点标题                                           |
| `site.subtitle` | 副标题                                             |
| `about`         | 个人简介                                           |
| `works`         | 作品列表（卡片标题、描述、标签、链接）             |
| `links`         | 底部外链                                           |
| `works[].image` | 可选，弹窗配图路径，如 `assets/images/project.png` |

配图放入 `assets/images/`，然后在作品中通过 `image` 字段引用。

## 文件结构

```
├── build.py              # 构建脚本
├── data/works.yaml       # 所有数据
├── templates/
│   ├── base.html         # HTML 骨架（导航、弹窗、页脚）
│   └── index.html        # 首页内容
├── assets/
│   ├── css/style.css     # 样式（含深浅色模式）
│   ├── js/main.js        # 交互（弹窗、主题切换、回到顶部）
│   └── images/           # 配图目录
├── output/               # 构建产物（上传此目录）
└── requirements.txt      # pyyaml, jinja2
```

## 部署

将 `output/` 目录上传至 Cloudflare Pages 即可。
