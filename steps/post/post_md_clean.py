import re
import sys
import logging

def post_md_clean(input_path):
    # Read the content of the input markdown file
    with open(input_path, 'r', encoding='utf-8') as md_file:
        md_content = md_file.read()

    # Look for ## Introduction and remove content before it
    intro_match = re.search(r'## Introduction', md_content)
    if intro_match:
        md_content = md_content[intro_match.start():]

    # Write the modified content back to the same file
    with open(input_path, 'w', encoding='utf-8') as md_file:
        md_file.write(md_content)

    logging.info(f"Post-processing complete. Output written to {input_path}")