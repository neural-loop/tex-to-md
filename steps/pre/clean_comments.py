import re
import argparse

def clean_comments(input_path):
    # Read the input .tex file
    with open(input_path, "r", encoding="utf-8") as tex_file:
        tex_content = tex_file.read()

    # Remove commented sections (lines starting with '%')
    tex_content = re.sub(r'^\s*%[^\n]*\n', '', tex_content, flags=re.MULTILINE)

    # Remove non-escaped '%' in the middle of a sentence
    tex_content = re.sub(r'(?<!\\)%[^\n]*(\n|$)', '\n', tex_content, flags=re.DOTALL)

    # Save the cleaned content back to the .tex file
    with open(input_path, "w", encoding="utf-8") as output_file:
        output_file.write(tex_content)

    print(f"Cleaned {input_path}")
