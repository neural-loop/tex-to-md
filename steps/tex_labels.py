import os
import re
from slugify import slugify
import logging

def tex_labels(input_path):
    main_tex_path = os.path.join(input_path, "main.tex")

    # Read the content of main.tex
    with open(main_tex_path, "r", encoding="utf-8") as tex_file:
        tex_content = tex_file.read()

    # Replace \label{data} with <div id="data"></div>
    tex_content = re.sub(r'\\label\{([^}]*)\}',
                         lambda match: generate_div(match.group(1)), tex_content)

    # Save the transformed content back to main.tex
    with open(main_tex_path, "w", encoding="utf-8") as tex_file:
        tex_file.write(tex_content)

    logging.debug(f" {main_tex_path} processed successfully.")

def generate_div(label):
    # Generate a slug-style ID
    div_id = slugify(label)
    # Create the <div> with original formatting
    div_tag = f'<div id="{div_id}"></div>\n'

    return div_tag
