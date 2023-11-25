import sys
import re

def process_footnotes(input_path, output_path):
    # Read the input .tex file
    with open(input_path, "r", encoding="utf-8") as tex_file:
        tex_content = tex_file.read()

    # Find all instances of '\footnote{' and replace with formatted quote
    start_pos = 0
    while '\\footnote{' in tex_content[start_pos:]:
        footnote_start = tex_content.index('\\footnote{', start_pos) + len('\\footnote{')
        bracket_count = 1
        footnote_end = footnote_start
        while bracket_count > 0:
            if tex_content[footnote_end] == '{':
                bracket_count += 1
            elif tex_content[footnote_end] == '}':
                bracket_count -= 1
            footnote_end += 1

        footnote_content = tex_content[footnote_start:footnote_end-1]  # -1 to remove trailing '}'
        tex_content = tex_content[:footnote_start-len('\\footnote{')] + \
            f" [ Note: {footnote_content}]" + tex_content[footnote_end:]

    # Save the transformed content as Markdown
    with open(output_path, "w", encoding="utf-8") as md_file:
        md_file.write(tex_content)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python process_footnotes.py <input_file_path> <output_file_path>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    process_footnotes(input_file_path, output_file_path)
