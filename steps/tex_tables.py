import re
from slugify import slugify
import os

def tex_tables(path):
    main_tex_path = os.path.join(path, 'main.tex')

    # Read the content of main.tex
    with open(main_tex_path, 'r') as file:
        main_tex_content = file.read()

    # Find all \begin{table}...\end{table} patterns
    table_patterns = re.findall(r'\\begin\{table\}(.*?)\\end\{table\}', main_tex_content, re.DOTALL)

    for table in table_patterns:
        # Find the label of the table
        label_match = re.search(r'\\label\{(.*?)\}', table)
        if label_match:
            label = label_match.group(1)
            slugified_label = slugify(label)
        else:
            slugified_label = ""

        # Find the caption of the table
        caption_match = re.search(r'\\caption\{((?:[^{}]|{[^{}]*})*)\}', table)
        if caption_match:
            caption = caption_match.group(1).replace('"','\'').replace('\n','').strip()
            caption = re.sub(r'\\label\{(.*?)\}', '', caption)
        else:
            caption = ""



        # blockquote = div_tag + caption_text + "\{\{" + "< pdf \""+ caption + "\">" + "\}\}\n"
        blockquote = '\{\{< pdf caption="' + caption + '" id="' + slugified_label + '" >\}\}\n'
        # Replace the table with the blockquote
        main_tex_content = main_tex_content.replace(table, blockquote)

    # Write the updated content back to main.tex
    with open(main_tex_path, 'w') as file:
        file.write(main_tex_content)