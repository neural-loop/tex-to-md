import re
import sys

def transform_abstract(input_path, output_path):
    # Read the input .md file
    with open(input_path, "r", encoding="utf-8") as md_file:
        md_content = md_file.read()

    # Define a regular expression pattern to match the LaTeX abstract block
    latex_abstract_pattern = r'\\begin{abstract}(.*?)\\end{abstract}'

    # Find and replace LaTeX abstract with Markdown heading and content
    md_content = re.sub(latex_abstract_pattern, r'## Abstract\n\1', md_content, flags=re.DOTALL)

    # Write the transformed content back to the same file
    with open(output_path, "w", encoding="utf-8") as md_file:
        md_file.write(md_content)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python transform_abstract.py <input_file_path> <output_file_path>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    transform_abstract(input_file_path, output_file_path)
