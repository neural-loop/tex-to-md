import re
import sys
import os
import argparse
import logging

def replace_itemize(match):
    items = match.group(1).strip().split('\n')
    markdown_list = "\n".join([f'- {item.strip()}' for item in items if item.strip()])
    markdown_list = re.sub(r'\\begin{itemize}|\\end{itemize}|\\item', '', markdown_list)
    return markdown_list

def tex_itemize(input_path):
    # Iterate over all .tex files in the input_path
    for file in os.listdir(input_path):
        if file.endswith(".tex"):
            tex_file_path = os.path.join(input_path, file)

            # Read the .tex file
            with open(tex_file_path, "r", encoding="utf-8") as tex_file:
                tex_content = tex_file.read()

            # Replace LaTeX itemize environments with Markdown list syntax
            tex_content = re.sub(r'\\begin{itemize}(.*?)\\end{itemize}', replace_itemize, tex_content, flags=re.DOTALL)
            # Add additional replacements for other environments if needed

            # Write the updated content back to the same file
            with open(tex_file_path, "w", encoding="utf-8") as tex_file:
                tex_file.write(tex_content)

            logging.debug(f" {tex_file_path} processed successfully.")