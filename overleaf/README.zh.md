# CityU Beamer — Overleaf 导入包

[English](README.md) · [简体中文](README.zh.md)

主题 v1.0.1 · XeLaTeX · 16:9 · 2025 年 1 月 PPT 素材

基于香港城市大学 PowerPoint 模板制作的社区改编版本，并非校方官方认可的模板。以下路径均相对于解压后的项目根目录。

## 编译

1. 在 Overleaf 中选择 **New Project → Upload Project**，上传 `cityu-beamer-overleaf.zip`。
2. 在项目设置中选择 **XeLaTeX**，使用账号当前可选的最新稳定 TeX Live 版本。
3. 将主文档设为 `main.tex`（英文）、`example-zh.tex`（中文）或 `minimal.tex`（简洁起点）。
4. 重新编译，检查文字、校徽和帧页码。若引用或总页码尚未稳定，再编译一次。

将 `beamerthemeCityU.sty`、`latexmkrc` 和完整的 `assets/` 目录保留在主文档旁。不需要原始 PPT、预览 PDF 或 Python 工具。

详细用法与自定义接口见 `docs/USAGE.zh.md`（中文）和 `docs/USAGE.md`（英文）。本地编译时，在项目根目录运行 `latexmk -xelatex -outdir=build main.tex`。

## 验证状态与许可

已用 TeX Live 2026 检查全新解压后的本地编译；尚未验证真实 Overleaf 云端编译。模板市场上架资格与编译兼容性是两回事，详见使用指南。

原创代码与文档采用 `LICENSE` 中的 MIT 许可；CityU 品牌素材不在其中。分享带品牌素材的版本前，请阅读 `NOTICE.md` 中的来源与权利说明。
