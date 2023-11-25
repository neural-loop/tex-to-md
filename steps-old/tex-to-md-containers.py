import re
import sys

def replace_minipage(match):
    minipage_content = match.group(1).strip()
    markdown_blockquote = "> " + minipage_content.replace('\n', '\n> ')
    return markdown_blockquote

def replace_colorbox(match):
    options = re.search(r'title=(.*?)\]', match.group(1))
    if options:
        title = options.group(1)
        colorbox_content = re.sub(r'\[.*?\]', '', match.group(1).strip())  # Strip bracketed meta-information
        markdown_blockquote = "> <span class='font-bold text-xl'>" + title + "</span>\n> " + colorbox_content.replace('\n', '\n> ')
        return markdown_blockquote
    return match.group(0)  # If no title is found, retain the original tcolorbox content.

def replace_mintedbox(match):
    code_content = match.group(1).strip()
    markdown_code_block = "```python\n" + code_content + "\n```"
    return markdown_code_block

def transform_file(input_path, output_path):
    # Read the input file
    with open(input_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Replace \begin{minipage} ... \end{minipage} with a Markdown blockquote
    content = re.sub(r'\\begin{minipage}(.*?)\\end{minipage}', replace_minipage, content, flags=re.DOTALL)

    # Replace \begin{tcolorbox} ... \end{tcolorbox} with a Markdown blockquote
    content = re.sub(r'\\begin{tcolorbox}(.*?)\\end{tcolorbox}', replace_colorbox, content, flags=re.DOTALL)

    # Replace \begin{mintedbox}{python} ... \end{mintedbox} with a Markdown code block
    content = re.sub(r'\\begin{mintedbox}{python}(.*?)\\end{mintedbox}', replace_mintedbox, content, flags=re.DOTALL)

    # Save the transformed content as Markdown
    with open(output_path, "w", encoding="utf-8") as md_file:
        md_file.write(content)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python transform_script.py <input_file_path> <output_file_path>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    transform_file(input_file_path, output_file_path)
