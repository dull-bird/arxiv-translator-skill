---
name: arxiv-translator
description: "Automatically downloads LaTeX source from arXiv, translates it to a target language (default Chinese), and compiles it to PDF using xelatex. Uses modern xeCJK for multilingual support. Trigger when the user provides an arXiv URL, paper ID, or natural language query about an arXiv paper and wants it translated/compiled."
---

# arXiv LaTeX Translator & Compiler (Modern Solution)

This skill handles the end-to-end workflow of converting an arXiv paper's LaTeX source into a translated PDF on Windows, macOS, and Linux using modern `xeCJK` and `fontspec`.

## Workflow

### 0. Pre-flight Dependency Check
Before starting, verify that all required system tools are installed.
- **Windows (PowerShell):** `Get-Command curl, tar, xelatex, bibtex -ErrorAction SilentlyContinue`
- **macOS / Linux (Bash):** `for cmd in curl tar xelatex bibtex; do command -v $cmd >/dev/null 2>&1 || echo "Missing: $cmd"; done`

### 1. Identify & Download
- Extract the ID (e.g., `2508.11825v2`) from the URL or find it via search.
- Create a target directory and download/extract the source and the paper pdf (for final check) using native tools (`curl`, `tar`).
  - Abstract: `https://arxiv.org/abs/xxxx.xxxxx`
  - Source: `https://arxiv.org/src/xxxx.xxxxx`
  - PDF: `https://arxiv.org/pdf/xxxx.xxxxx.pdf`

### 2. Analyze Structure & Indexing (Mandatory)
- Read the original `.pdf` file to build a mental map of the paper's structure.
- **Section Indexing (Crucial):** Run `grep -n "\\section" main.tex` (and any other sub-tex files identified) to list all major sections. **Create a checklist** of these sections in your memory.
- **Dependency Scan:** Scan for `\input{}` or `\include{}` commands to identify all sub-files that need translation.
- **Terminology Glossary:** Before translating, skim the abstract and introduction to identify 5-10 core technical terms. Create a local mental glossary to ensure consistent translation throughout the paper (e.g., ensuring "Relative Position" is always translated as "相对位置").
- Copy the entire LaTeX project to a new `translated/` working directory to preserve the original.

### 3. Translate & Modernize (Iterative Chunking with Checklist)
- **Sequential Chunking:** NEVER attempt to translate a large `.tex` file in one massive operation. Break the work down section by section according to your checklist from Step 2.
- **Checkpointing:** After replacing each section, explicitly state: "Finished translating Section X. [X/Total Sections]".
- **Content Preservation:** Translate text while rigorously preserving LaTeX commands, math environments (`$`, `\begin{equation}`), citations (`\cite{}`), and references (`\ref{}`). Keep reference paper titles and author names untranslated unless necessary.
- **Modern Chinese Support (xeCJK)**:
    - Avoid `ctex` to prevent template style conflicts.
    - Inject the following into the preamble:
      ```latex
      \usepackage{xeCJK}
      % Platform-specific fonts (Auto-detected based on environment)
      % Windows: \setCJKmainfont{Microsoft YaHei}
      % macOS: \setCJKmainfont{PingFang SC}
      % Linux: \setCJKmainfont{Noto Sans CJK SC}
      ```
    - *Font Fallback:* If the specified font causes compilation errors, fallback to `SimSun` (Windows) or `Noto Sans CJK SC` (Linux).

### 4. Compile & Auto-Fix
- Use `xelatex -interaction=nonstopmode` for all platforms to leverage `fontspec` and `xeCJK` while preventing compilation hangs on minor errors.
- **Standard compilation loop:** `xelatex` -> `bibtex` -> `xelatex` x2.
- **Error Auto-Fixing:** If compilation fails (exit code != 0), do not just give up. Read the generated `.log` file, specifically looking for lines starting with `!` (e.g., `! Undefined control sequence.`). Identify the exact line number and file causing the error, use the `replace` tool to fix the LaTeX syntax issue, and recompile.

### 5. Integrity Verification & Review (Final Gate)
- **Completeness Check:** Use `grep "\\section" translated/main.tex` and compare the titles against your original checklist from Step 2. If any section title is still in English or missing, you MUST backtrack and fix it before reporting success.
- **Visual Check:** Compare the translated PDF's visual layout with the original PDF to spot any severe formatting degradation (e.g., images overflowing, missing sections).
- **Template adjustments:** If Chinese translation causes significant layout overflow, consider suggesting minor layout tweaks (e.g., adding `\small` to a matrix, or ensuring figures use `[t]` or `[h]`).
- Clean up intermediate files (`.aux`, `.log`, `.out`, etc.) if requested, or move the final `_CN.pdf` to the root directory for easy user access.

## Guidelines
- **Font Selection**:
    - On **Windows**: Always prefer `\setCJKmainfont{Microsoft YaHei}` or `SimSun`.
    - On **macOS**: Always prefer `\setCJKmainfont{PingFang SC}`.
    - On **Linux**: Always prefer `\setCJKmainfont{Noto Sans CJK SC}`.
- **Preserve Template**: Modern academic templates are fragile. Using `xeCJK` is less intrusive than `ctex` as it doesn't redefine headers or section spacing by default.
- **Heredocs**: Use single-quoted heredocs in shells to handle backslashes (`\`) correctly.