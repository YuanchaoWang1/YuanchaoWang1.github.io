# Yuanchao Wang · Personal Homepage

个人学术主页初稿，包含 Home、Publications、Projects。网页使用英文，维护说明使用中文。

采用独立的静态实现，保留参考主页的顶部导航与左侧个人资料布局。页面直接输出 HTML，运行时无需 JavaScript；生成脚本仅使用 Python 标准库。可以部署到 GitHub Pages，也可以直接打开 `dist/index.html` 查看。

## 快速修改

| 要修改的内容 | 文件 |
| --- | --- |
| 姓名、职位、简介、邮箱、个人链接、经历 | `content/site.json` |
| 论文标题、作者顺序、年份、会议、项目简介 | `content/papers.json` |
| 排版、字体、颜色、手机布局 | `dist/assets/style.css` |
| 照片 | `dist/assets/portrait.png` |
| 页面结构与导航 | `scripts/build.py` |
| 算法示意图 | `dist/assets/diagrams/` 中直接维护的高分辨率 PNG |
| GitHub 自动部署 | `.github/workflows/pages.yml` |

修改后，在仓库根目录运行：

```sh
python scripts/build.py
python scripts/check_site.py
```

Windows 也可以使用 `py` 代替 `python`。需要 Python 3.10 或更新版本，无需安装第三方包。

生成的 HTML 和 PNG 都纳入 Git。`dist/assets/style.css`、照片和上传的 PNG 示意图属于直接维护的源文件，生成脚本不会覆盖。请修改 JSON 后重新生成 HTML；直接修改生成的 HTML 会在下次生成时被覆盖。

## 页面结构

| 路径 | 用途 |
| --- | --- |
| `/` | 简介、研究主线、教育、经历、奖项和服务 |
| `/publications/` | 按时间倒序排列的单列论文列表，展示会议名称或预印本状态；无年份分组和论文配图 |
| `/projects/` | 四个已有论文项目的介绍与算法图，以及 CROSS 占位介绍 |
| `/research/` | 兼容原名称，跳转到 Publications |

导航和资源使用相对路径，兼容用户主页与仓库子路径。Projects 将 CROSS 排在最上方，并提供五个稳定锚点：`#cross`、`#ood-tv-irm`、`#ectr`、`#shellood`、`#attention-trees`。

## 关于目标地址

本站目标地址为 `https://yuanchaowang1.github.io`，对应 GitHub 账号 `yuanchaowang1` 及用户主页仓库 `YuanchaoWang1/YuanchaoWang1.github.io`。

本地仓库的 `origin` 已连接到该仓库。GitHub Pages 是否已经启用，仍以远程仓库的 **Settings → Pages** 页面为准。

官方说明：[GitHub Pages 的站点类型与命名](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)。

## 首次部署到 GitHub Pages

1. 登录控制目标地址的 GitHub 账号。
2. 新建空的公开仓库 `YuanchaoWang1.github.io`。首次创建时保持为空，避免自动生成 README。
3. 将此项目所有源文件推送到该仓库的 `main` 分支。
4. 在仓库 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**。
5. 打开 **Actions → Deploy homepage to GitHub Pages → Run workflow**。之后每次推送 `main` 都会自动更新网站。

如果使用下载的源码 ZIP，解压后进入含有本 README 的目录，运行：

```sh
git init -b main
git add .
git commit -m "Create academic homepage"
git remote add origin https://github.com/yuanchaowang1/YuanchaoWang1.github.io.git
git push -u origin main
```

如 Git 首次要求配置身份，可在仓库内使用 `git config user.name` 和 `git config user.email` 设置你的提交姓名和邮箱。推送使用你正常的 GitHub 登录方式。

从已存在的 Git 仓库迁移时，可以新增名为 `github` 的 remote，再执行 `git push -u github main`。无需更改其他用途的 remote。

自动部署会重新生成页面和图，并将 `dist` 发布。`SITE_URL` 由 Pages 配置自动注入，用于 canonical 元信息。在其他平台部署时，可以通过环境变量 `SITE_URL` 或 `content/site.json` 中的 `site_url` 设置实际网址；留空会省略 canonical。

官方说明：[GitHub Pages 自定义工作流](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)。

## 后续维护

### 更新论文或项目

在 `content/papers.json` 中修改对应条目。

| 字段 | 含义 |
| --- | --- |
| `id` | 稳定项目标识，同时对应图文件名与锚点 |
| `title` / `authors` | 论文题目与完整作者顺序 |
| `year` | Publications 的倒序排列依据 |
| `venue` / `venue_detail` | 会议简称及完整名称，或稿件状态 |
| `links` | 已有的论文、会议、代码等链接 |
| `summary` / `takeaway` | 项目简述与核心思想 |
| `caption` / `diagram_alt` | 图注和无障碍替代说明 |
| `diagram` / `diagram_width` / `diagram_height` | 自定义图文件名及其原始像素尺寸 |
| `has_diagram` | 设为 `false` 时允许仅有文字的项目占位 |
| `availability` | 待补材料的简短说明 |

新加项目时，在 `dist/assets/diagrams/` 中加入图片并在论文条目中填写图文件名与尺寸，同时在 `scripts/build.py` 的 `projects()` 中更新 `order` 列表。首页不重复整份论文目录，所有论文集中在 Publications。

CROSS 当前设置 `has_diagram: false`、空的 `links` 和 `authors`，因此不会生成虚构的论文链接、作者名单或算法图。取得 PDF 后补齐作者、链接与方法图，并把 `has_diagram` 改为 `true`。首页研究轨迹单独在 `content/site.json` 的 `trajectory` 字段维护。

### 修改算法图

四个项目均使用直接维护的高分辨率 PNG：`ood-tv-irm.png`、`ectr.png`、`shellood.png` 和 `attention-trees.png`。图片按原始宽高比响应式缩放，并在宽屏上获得更大的展示区域；项目页同时提供全尺寸入口。替换时保持稳定文件名，或同步更新 `content/papers.json` 中的 `diagram` 与尺寸字段。

这些图展示算法关系，点的位置、大小和注意力矩阵均为示意，未展示实验测量值。项目页图注说明了省略的细节。

### 提交更新

```sh
python scripts/build.py
python scripts/check_site.py
git add .
git commit -m "Update homepage content"
git push
```

更新 `content/site.json` 的 `updated` 字段，以显示新的维护月份。

## 本轮内容核对

详细来源、发表状态与需要下轮确认的字段见 [CONTENT_NOTES.md](CONTENT_NOTES.md)。正式发表条目为 **ICLR 2025**；根据本轮用户补充，ECTR 和 ShellOOD 标为 **Under review at NeurIPS 2026**，CROSS 标为 **ICLR 2027 submission**。CROSS 的 2026 年分组表示当前稿件年份。ShellOOD 使用新名称，并明确标出公开链接仍指向早期 BootOOD 版本。

页面的本地路径、锚点、PNG 文件结构和标注尺寸由 `scripts/check_site.py` 检查。算法图已做内容核对；GitHub Pages 工作流需在目标远程仓库创建并启用 Pages 后首次运行。
