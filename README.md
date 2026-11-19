# 英语练习空间

姊妹网站 monorepo。每个应用独立维护，通过根目录 sites.json 注册。

| 网站 | 源码 | 统一部署路径 |
| --- | --- | --- |
| 脱口而出 | apps/english-reflex | /english-reflex/ |
| 动词练习室 | apps/verb-workshop | /verb-workshop/ |

## 本地运行

需要 Python 3；构建无需安装第三方依赖。

```sh
npm run dev
```

打开 http://localhost:8000 。`npm run build` 生成统一发布目录 dist。

## Vercel 部署

导入本仓库，Root Directory 保持仓库根目录，Framework Preset 选 Other。根目录 vercel.json 已设置构建命令和输出目录。构建环境需要 Python 3。

也可为两个网站分别创建 Vercel Project：Root Directory 分别为 apps/english-reflex 与 apps/verb-workshop，跳过构建，Output Directory 为 dist。独立部署保留原有线上姊妹网站链接；统一部署会自动将这两个链接替换为同源路径。

## 添加姊妹网站

1. 新建 apps/<site-id>/dist，放入网站 index.html 与资源。
2. 在 sites.json 添加 id、name、path、currentUrl。
3. 执行 npm run build 验证。首页目录和已知网站链接由注册表构建。

现有网站内的“练习空间”菜单仍由各应用维护；新增网站时同步补充菜单。

## 数据与源码

保留脱口而出的语料快照、转换脚本与图片资源，以及动词练习室的数据文件。apps 内 dist 是原网站可直接发布的源文件，不应全局忽略。

未导出运行环境密钥、Notion 凭据或 Sites 站点身份配置。语料为静态快照，新增 Notion 内容不会自动同步。

## 导出来源

- 脱口而出：v30，源提交 8b5b00e8a12dae51ec73ff510eda52b70e531884
- 动词练习室：v5，源提交 35675af4b9192c7553b9f1bfbc757ac1bdafa0ee

首次建议创建 private 仓库；语料快照中包含原始学习记录与来源信息。
