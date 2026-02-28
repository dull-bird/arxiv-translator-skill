import os
import re
import sys

def split_tex_file(input_file, output_dir="sections"):
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. 定位正文部分 (begin{document} 到 end{document})
    begin_doc_match = re.search(r"\\begin\{document\}", content)
    end_doc_match = re.search(r"\\end\{document\}", content)

    if not begin_doc_match or not end_doc_match:
        print(f"Error: 找不到 \\begin{{document}} 或 \\end{{document}}，可能不是完整的主 tex 文件。")
        return

    begin_doc_idx = begin_doc_match.end()
    end_doc_idx = end_doc_match.start()

    preamble_content = content[:begin_doc_idx]
    body_content = content[begin_doc_idx:end_doc_idx]
    postamble_content = content[end_doc_idx:]

    os.makedirs(output_dir, exist_ok=True)

    # 2. 用正则匹配所有的 \section{...} 或 \section*{...}
    # 使用正则前瞻和后顾避免匹配到注释里的 section
    section_pattern = re.compile(r"((?<!%)\s*\\section\*?\{[^}]+\})")
    
    # 按照 section 劈开正文
    parts = section_pattern.split(body_content)
    
    main_tex_body = ""
    section_counter = 1

    # parts[0] 是第一个 \section 之前的内容（通常是摘要 abstract，标题，作者等）
    if parts[0].strip():
        file_name = "00_preamble_and_abstract.tex"
        with open(os.path.join(output_dir, file_name), "w", encoding="utf-8") as f:
            f.write(parts[0])
        main_tex_body += f"\\input{{{output_dir}/{file_name}}}\n"

    # 随后的 parts 是交替的: [匹配到的 section 标题, section 的内容, 下一个标题, 下一个内容...]
    for i in range(1, len(parts), 2):
        sec_title = parts[i]
        sec_content = parts[i+1] if i+1 < len(parts) else ""
        
        file_name = f"{section_counter:02d}_section.tex"
        with open(os.path.join(output_dir, file_name), "w", encoding="utf-8") as f:
            f.write(sec_title + sec_content)
            
        main_tex_body += f"\\input{{{output_dir}/{file_name}}}\n"
        section_counter += 1

    # 3. 组装新的主文件
    new_main_content = preamble_content + "\n" + main_tex_body + "\n" + postamble_content
    
    # 覆盖原文件（或者你可以存为 main_split.tex 保证安全）
    with open(input_file, "w", encoding="utf-8") as f:
        f.write(new_main_content)

    print(f"成功将论文拆分为 {section_counter} 个部分，存放于 {output_dir}/ 目录下，已重写 {input_file}。")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        split_tex_file(sys.argv[1])
    else:
        print("Usage: python split_tex.py <main.tex>")