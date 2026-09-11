# 我的小站

Hugo + PaperMod + PagesCMS + GitHub Pages 的个人博客。

- 线上地址：<https://combig.github.io/>
- 内容后台：<https://app.pagescms.org/>

## 本地预览

需要先有 Hugo extended（本仓库用 v0.166.0）：

```bash
hugo server -D
# 打开 http://localhost:1313
```

主题已随仓库提交，克隆下来直接能跑。升级主题：

```bash
bash scripts/fetch-theme.sh v8.0
```

## 写文章

### 方式一：PagesCMS（推荐，不用装任何东西）

1. 打开 <https://app.pagescms.org/>，用 GitHub 登录
2. 选中本仓库 → 左侧「文章」写博客，「独立页面」改关于页
3. 新建 / 编辑 → Save，它会自动往 `main` 提交 commit
4. GitHub Actions 跑完（约 1 分钟）网站自动更新

> 站点标题、作者、社交链接这些在 `hugo.toml` 里，直接在 GitHub 网页上改就行
> （没开放给 PagesCMS：它会重写整个文件，未声明的配置项会被清掉）。

### 方式二：本地写

```bash
hugo new content posts/文章标题.md
```

生成的文件在 `content/posts/`，把 `draft: true` 改成 `false` 才会发布。

## 目录结构

```
content/posts/      博客文章
content/about.md    关于页
static/images/      图片（PagesCMS 上传的图也放这）
hugo.toml           站点配置
.pages.yml          PagesCMS 后台表单配置
scripts/            主题升级脚本
.github/workflows/  自动部署
```

## 发布流程

推送到 `main` 后，`.github/workflows/hugo.yml` 会：

1. 装 Hugo extended
2. `hugo --minify` 构建到 `public/`
3. 上传到 GitHub Pages 并发布

## 换成你自己的信息

- `hugo.toml`：`baseURL`、`title`、`[params]` 里的 author / description、社交链接
- `content/about.md`：自我介绍
- 删掉 `content/posts/` 下的示例文章
