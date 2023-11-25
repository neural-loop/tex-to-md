import os
import re
import argparse
import logging

def apply_alphabetical_operations(tex_content):
    # Replace '. _' with ''
    tex_content = re.sub(r'\. _', '', tex_content)
    return tex_content

def post_clean_string_replace(input_path):
    # Read the input .tex file
    with open(input_path, "r", encoding="utf-8") as tex_file:
        tex_content = tex_file.read()

    # Apply replacements and removals alphabetically
    tex_content = apply_alphabetical_operations(tex_content)

    # Save the cleaned content back to the same file
    with open(input_path, "w", encoding="utf-8") as tex_file:
        tex_file.write(tex_content)

    logging.debug(f"{input_path} cleaned successfully.")

if __name__ == "__main__":
    # Specify the input file path
    input_path = "/path/to/your/project/main.tex"

    # Process the LaTeX file in the specified input path
    post_clean_string_replace(input_path)
