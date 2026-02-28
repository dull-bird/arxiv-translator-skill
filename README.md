# arXiv Translator Skill for Gemini CLI

This is a custom skill for [Gemini CLI](https://github.com/google/gemini-cli) that enables the AI agent to automatically download LaTeX source files from arXiv, translate them into a target language (defaulting to Chinese), and compile them into a high-quality PDF.

## Features

- **Automated Workflow**: Downloads the paper's source code, unzips it, splits it into manageable sections, translates them, and compiles the final document.
- **Modern LaTeX Support**: Uses `xelatex` and `xeCJK` for modern, robust multi-lingual font support.
- **Modular Translation**: Safely splits large monolithic `.tex` files into smaller sub-files using a provided Python script (`scripts/split_tex.py`), ensuring reliable translation without token limits or string-replacement errors.
- **Auto-Fixing**: Capable of reading LaTeX compilation logs to auto-correct syntax or missing package errors during the PDF generation phase.

## Prerequisites

Ensure your system has the following dependencies installed and accessible in your system `PATH`:
- `curl`
- `tar`
- `xelatex` (usually provided by TeX Live, MacTeX, or MiKTeX)
- `bibtex`
- Appropriate CJK fonts (e.g., `Microsoft YaHei` on Windows, `PingFang SC` on macOS, `Noto Sans CJK SC` on Linux).

## Installation

1. Create a directory named `arxiv-translator` inside your Gemini CLI skills folder (usually `~/.gemini/skills/`).
2. Copy the `SKILL.md` and the `scripts/` folder into this new directory.

```bash
mkdir -p ~/.gemini/skills/arxiv-translator
git clone https://github.com/dull-bird/arxiv-translator-skill.git ~/.gemini/skills/arxiv-translator
```

## Usage

Simply invoke the skill in Gemini CLI by mentioning an arXiv paper and asking for a translation:

```
> Can you translate arXiv paper 2508.11825 into Chinese and generate the PDF?
```

The agent will automatically activate the skill, download the source, run the translation process, and compile the final `_CN.pdf` for you.
