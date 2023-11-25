import os
import re
import sys
import argparse
from slugify import slugify
import logging

# Custom function to process matches
def process_match(match):
    value = match.group(1)
    # Replace colons with dashes in the value
    value = slugify(value)
    # Return the modified reference
    return f"<a href='#{value}'>{value}</a>"

def tex_refs(input_path):
    # Iterate through all .tex files in the input path
    for root, dirs, files in os.walk(input_path):
        for file in files:
            if file.endswith(".tex"):
                file_path = os.path.join(root, file)

                # Read the input .tex file
                with open(file_path, "r", encoding="utf-8") as tex_file:
                    tex_content = tex_file.read()

                # Replace \Cref{value} and \ref{value} with the result of the custom function
                tex_content = re.sub(r'\\Cref{([^}]*)}', process_match, tex_content)
                tex_content = re.sub(r'\\ref{([^}]*)}', process_match, tex_content)

                # Save the transformed content back to the same file
                with open(file_path, "w", encoding="utf-8") as tex_file:
                    tex_file.write(tex_content)

                logging.debug(f" {file_path} processed successfully.")
