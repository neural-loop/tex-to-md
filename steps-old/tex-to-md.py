import re
import sys

def replace_itemize(match):
    items = match.group(1).strip().split('\n')
    markdown_list = "\n".join([f'* {item.strip()}' for item in items if item.strip()])
    markdown_list = re.sub(r'\\begin{itemize}|\\end{itemize}|\\item', '', markdown_list)
    return markdown_list



def convert_tex_to_md(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as tex_file:
        tex_content = tex_file.read()

    tex_content = re.sub(r'\\begin{itemize}(.*?)\\end{itemize}', replace_itemize, tex_content, flags=re.DOTALL)
    # tex_content = re.sub(r'\\begin{enumerate}(.*?)\\end{enumerate}', replace_enumerate, tex_content, flags=re.DOTALL)

    tex_content = re.sub(r'\\section\s*{([^}]+(?:\s*[\r\n]+\s*[^}]+)*)}', r'## \1', tex_content)
    tex_content = re.sub(r'\\chapter{([^}]+)}', r'## \1', tex_content)
    tex_content = re.sub(r'\\subsection{([^}]+)}', r'### \1', tex_content)
    tex_content = re.sub(r'\\subsubsection{([^}]+)}', r'#### \1', tex_content)

    tex_content = re.sub(r'\\textbf{([^}]+)}', lambda match: f'**{match.group(1).strip()}**', tex_content)
    tex_content = re.sub(r'\\emph{([^}]+)}', lambda match: f'**{match.group(1).strip()}**', tex_content)
    tex_content = re.sub(r'\\textit{([^}]+)}', lambda match: f'_{match.group(1).strip()}_', tex_content)

    with open(output_path, "w", encoding="utf-8") as md_file:
        md_file.write(tex_content)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python tex-to-md.py <input_file_path> <output_file_path>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    convert_tex_to_md(input_file_path, output_file_path)
