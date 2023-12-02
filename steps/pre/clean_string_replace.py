import os
import re
import argparse
import logging

def apply_alphabetical_operations(tex_content):
    # Alphabetically organized replacements and removals
    operations = [
        (r'\begin{chapter*}', r'\begin{chapter}'),
        (r'\end{chapter*}', r'\end{chapter}'),
        (r'\begin{equation*}', r'\begin{equation}'),
        (r'\end{equation*}', r'\end{equation}'),
        (r'\begin{equation*}', r'$$'),
        (r'\end{equation*}', r'$$'),
        (r'\begin{figure*}', r'\begin{figure}'),
        (r'\end{figure*}', r'\end{figure}'),
        (r'\begin{table*}', r'\begin{table}'),
        (r'\end{table*}', r'\end{table}'),
        (r'\begin{wrapfigure*}', r'\begin{wrapfigure}'),
        (r'\end{wrapfigure*}', r'\end{wrapfigure}'),
        (r'\chapter*', r'\chapter'),
        (r'\footnote*', '\footnote'),
        (r'\section*', r'\section'),
        (r'\subsection*', r'\subsection'),
    ]

    for pattern, replacement in operations:
        tex_content = tex_content.replace(pattern, replacement)

    # Replace tabs with an empty string
    tex_content = re.sub(r'\t', r'', tex_content)
    tex_content = re.sub(r'  ', r'', tex_content)

    return tex_content

def clean_string_replace(input_path):
    # Iterate through all .tex files in the input path
    for root, dirs, files in os.walk(input_path):
        for file in files:
            if file.endswith(".tex"):
                file_path = os.path.join(root, file)

                # Read the input .tex file
                with open(file_path, "r", encoding="utf-8") as tex_file:
                    tex_content = tex_file.read()

                # Apply replacements and removals alphabetically
                tex_content = apply_alphabetical_operations(tex_content)

                # Save the cleaned content back to the same file
                with open(file_path, "w", encoding="utf-8") as tex_file:
                    tex_file.write(tex_content)

                logging.debug(f"{file_path} cleaned successfully.")
