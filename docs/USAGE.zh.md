# 使用与自定义

[English](USAGE.md) · [简体中文](USAGE.zh.md) · [返回首页](../README.zh.md)

## 支持的文档设置

```latex
\documentclass[aspectratio=169,11pt,t]{beamer}
\usetheme{CityU}
```

使用 XeLaTeX 和 16:9 页面。其他宽高比会拉伸原始背景，不在已测试的版式范围内。示例正文为 11 pt；其他字号或特别密集的页面需要自行检查效果。本主题不支持 pdfLaTeX 和 LuaLaTeX。

字体按 TeX Live 中的文件名加载：TeX Gyre Heros 用于无衬线文字，Termes 用于衬线文字，Cursor 用于等宽文字，Latin Modern 用于数学公式。不需要 Arial、微软雅黑或其他操作系统字体。图片均使用相对路径；示例不需要 SVG 转换、shell escape、外部绘图程序或参考文献处理程序。

## 导入 Overleaf

1. 选择 **New Project → Upload Project**，上传 `cityu-beamer-overleaf.zip`。
2. 在项目设置中选择 **XeLaTeX**，使用账号当前可选的最新稳定 TeX Live 版本。
3. 将主文档设为英文示例 [main.tex](../main.tex)、中文示例 [example-zh.tex](../example-zh.tex)，或作为简洁起点的 [minimal.tex](../minimal.tex)。
4. 重新编译。引用与总帧数可能需要多轮处理；若尚未稳定，再编译一次。
5. 检查校徽、长标题、中文字符、公式和页码。英文示例有 18 个 PDF 页面、11 个编号帧；中文示例有 11 个页面、7 个编号帧；最小示例有 4 个页面、1 个编号帧。

ZIP 根目录直接包含主文档、主题和 `latexmkrc`，并附有 `assets/` 中的四张背景、两种语言的使用指南及许可声明。包内 README 是专用导入说明。在 Overleaf 上编译不需要原始 PPT、仓库预览、Python 工具或本地 TeX 安装。

已用 TeX Live 2026 检查全新解压后的本地编译；尚未验证真实 Overleaf 云端编译或旧版 TeX Live。[Gallery 提交政策](https://docs.overleaf.com/templates/submitting-to-the-overleaf-template-gallery)不接收非官方大学演示模板，因此这个社区改编版本不会仅因编译成功就获得上架资格；官方认可与素材授权需要另行确认。

## 本地编译

将 `beamerthemeCityU.sty`、`latexmkrc` 和完整的 `assets/` 目录放在主文档旁。TeX Live 需要提供 Beamer、fontspec、Latin Modern、TeX Gyre、TikZ 和 booktabs；中文示例还需要 ctex 和 Fandol。在该目录运行：

```sh
latexmk -xelatex -outdir=build main.tex
latexmk -xelatex -outdir=build example-zh.tex
latexmk -xelatex -outdir=build minimal.tex
```

附带的 `latexmkrc` 也会在运行 `latexmk main.tex` 时选择 XeLaTeX。Python 仅用于仓库维护工具，不参与主题或这些示例的编译。

## 文档信息与页脚

```latex
\title[页脚短标题]{较长的报告标题}
\subtitle{可选副标题}
\author{你的姓名}
\institute{学院／学系／研究组\\香港城市大学}
\date{\today}
\cityufooter{需要时可自定义页脚文字}
```

页脚默认显示短标题，并链接到演示文稿的开头。完整标题较长时，请填写 `\title` 的可选短标题参数。`\cityufooter{...}` 会替换页脚文字；`\cityufooter{}` 只留下分隔线和页码。若要隐藏整个页脚，使用主题选项 `footer=false`。

页脚文字应保持在一行内。封面适合最多两行的标题、简短副标题，以及约四行的作者、单位与日期信息。长文字不会自动缩小：请缩短或拆分内容，或调整相应的 Beamer 字号。较长作者名单及 `\and` 分组需要自行检查。

## 页面命令

| 命令 | 行为 |
| --- | --- |
| `\cityutitlepage` | 根据文档信息创建不显示页脚、不计入编号的封面。 |
| `\section{标题}` | 默认自动创建不计入编号的章节页。 |
| `\section*{标题}` | 不自动创建章节页。 |
| `\cityusectionpage` | 为当前章节创建不计入编号的章节页。 |
| `\cityuclosing{谢谢}` | 创建不显示页脚、不计入编号的结束页。 |
| `\cityuclosing[欢迎提问与交流]{谢谢}` | 在结束页添加副标题。 |

这些命令会创建完整的帧，不要将它们放进另一个 `frame` 环境。只有辅助命令会自动设置 `plain,noframenumbering`；原生页面模板也可以显式调用：

```latex
\begin{frame}[plain,noframenumbering]
  \titlepage
\end{frame}
```

`\sectionpage` 也可采用同样写法。手动添加章节页时，应先关闭自动章节页，避免重复：

```latex
\usetheme[sectionpages=false]{CityU}
% 在后文中、任何 frame 环境之外使用：
\section{研究方法}
\cityusectionpage
```

主题使用 Beamer 的 `\AtBeginSection` 钩子。在加载主题后另行设置该钩子，会替换自动章节页行为。子章节不会自动添加章节页。

## 主题选项

| 选项 | 默认值 | 作用 |
| --- | --- | --- |
| `sectionpages=true` / `false` | `true` | 开启或关闭自动章节页。 |
| `footer=true` / `false` | `true` | 显示或隐藏普通帧的页脚。 |
| `assetspath=directory` | `assets` | 指定包含四张固定文件名 PNG 的相对目录。 |

例如：

```latex
\usetheme[sectionpages=false,footer=true,assetspath=brand]{CityU}
```

自定义目录必须包含 `title.png`、`section.png`、`content.png` 和 `closing.png`。为便于跨平台编译，路径使用正斜杠，注意文件名大小写，目录名最好只含 ASCII 字符且不含空格。背景保持 16:9，并确认你有权使用替换素材。

## 中文与双语文档

与 `example-zh.tex` 一样，在主题之前加载 ctex：

```latex
\usepackage[UTF8,fontset=fandol]{ctex}
\usetheme{CityU}
```

这样会使用 Fandol 中文字体和中文图表标签。如果希望支持中文文字但保留英文风格的标签，可在 ctex 选项中加入 `scheme=plain`。Fandol 不覆盖全部生僻汉字；添加少见姓名或字符后应检查编译日志。

## 常规 Beamer 内容

可以使用标准的 `frame`、`columns`、`itemize`、`enumerate`、`block`、`alertblock` 和 `exampleblock` 环境。`main.tex` 演示了数学公式、`booktabs` 表格、原生 TikZ 图和 `thebibliography` 参考文献。包含 `verbatim` 的帧需要加上 `[fragile]`。

页脚按帧计数，而不是按 PDF 的物理页面计数。`<+->` 等逐步显示会沿用同一个帧号；封面、章节页和结束页辅助命令生成的页面不计入编号。自行创建的帧默认计数，除非指定 `noframenumbering`。主题不提供特殊的附录编号功能，也不依赖额外的附录宏包。

普通页标题为右上角校徽预留空间，并以右侧不强制对齐的方式换行。标题尽量控制在两行内。不要让大图或手动定位的内容覆盖校徽、页脚；主题无法阻止任意自定义绘图遮挡这些区域。分栏内的图片使用 `width=\linewidth`，不要使用整页宽度。

## 小幅外观调整

加载主题后，仍可使用标准 Beamer 自定义接口：

```latex
\setbeamerfont{title}{size=\fontsize{22}{26},series=\bfseries}
\setbeamerfont{frametitle}{size=\fontsize{18}{21},series=\bfseries}
\setbeamercolor{alerted text}{fg=CityURed}
```

可用颜色包括 `CityURed`、`CityUInk`、`CityUMuted`、`CityULine`、`CityUPaper` 和 `CityUTeal`。调整主题排版不等于获得修改学校品牌素材的权限。

## 常见问题

- **“This theme requires XeLaTeX”**：更改项目编译器，不要将源码改用 pdfLaTeX 编译。
- **找不到 `beamerthemeCityU.sty`**：将附带的主题文件放回或上传到主文档旁，并从该目录编译；它不是 TeX Live 自带宏包。
- **缺少依赖 `.sty` 或字体文件**：安装报错对应的 TeX Live 宏包，不必安装 Windows 字体。完整的 Overleaf TeX Live 环境通常已提供这些依赖。
- **缺少背景**：从项目根目录编译，检查 `assetspath`、文件名及大小写，确认四张 PNG 均已上传。
- **总页码不正确或引用未解析**：使用 `latexmk` 或再次编译，让 Beamer 的辅助文件稳定下来。
- **内容溢出或页面拥挤**：缩短内容或拆成多个帧；编译成功不代表版式一定合适。
- **没有自动章节页**：检查 `sectionpages`、是否使用星号章节，以及是否在后文替换了 `\AtBeginSection` 钩子。

素材来源与使用条款见 [NOTICE.md](../NOTICE.md)。
