import sys
import re

def process_center_environment(input_path, output_path):
    # Read the input .tex file
    with open(input_path, "r", encoding="utf-8") as tex_file:
        tex_content = tex_file.read()

    # Replace \begin{displayquote} and \end{displayquote} with Markdown-style blockquote
    tex_content = re.sub(r'\\begin{displayquote}(.*?)\\end{displayquote}', r'> \1', tex_content, flags=re.DOTALL)
    tex_content = re.sub(r'\\begin{quote}(.*?)\\end{quote}', r'> \1', tex_content, flags=re.DOTALL)

    # Remove newlines within the blockquote
    tex_content = re.sub(r'>\s*\n\s*', '> ', tex_content)

    # Save the transformed content as Markdown
    with open(output_path, "w", encoding="utf-8") as md_file:
        md_file.write(tex_content)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python process_center_environment.py <input_file_path> <output_file_path>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    process_center_environment(input_file_path, output_file_path)
