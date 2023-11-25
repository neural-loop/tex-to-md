import sys
import re

def replace_enumerate(match):
    items = match.group(1).strip().split('\n')
    markdown_list = []

    for item in items:
        item_text = item.strip()
        # Replace \item with '1. '
        item_text = item_text.replace('\\item', '1. ')
        # Replace \smallskip with '  - '
        item_text = item_text.replace('\\smallskip', '\t- ')
        markdown_list.append(item_text)

    return '\n'.join(markdown_list)

def process_enumerate(input_path, output_path):
    # Read the input .tex file
    with open(input_path, "r", encoding="utf-8") as tex_file:
        tex_content = tex_file.read()

    # Replace \begin{enumerate} and \end{enumerate} with Markdown-style list
    tex_content = re.sub(r'\\begin{enumerate}(.*?)\\end{enumerate}', replace_enumerate, tex_content, flags=re.DOTALL)

    # Save the transformed content as Markdown
    with open(output_path, "w", encoding="utf-8") as md_file:
        md_file.write(tex_content)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python process_enumerate.py <input_file_path> <output_file_path>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    process_enumerate(input_file_path, output_file_path)
