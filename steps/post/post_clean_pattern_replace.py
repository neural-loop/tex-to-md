import os
import re
import argparse
import logging


def replacement_patterns(tex_content):
    # Define the pattern to match \begin{enumerate}[...] and remove the bracketed area
    pattern = re.compile(r'\\begin{enumerate}\[.*?\]', re.DOTALL)
    pattern2 = re.compile(r'\\begin{itemize}\[.*?\]', re.DOTALL)
    pattern3 = re.compile(r'\\begin{mdframed}\[.*?\]', re.DOTALL)
    # Replace matching patterns with \begin{enumerate}
    tex_content = pattern.sub(r'\\begin{enumerate}', tex_content)
    tex_content = pattern2.sub(r'\\begin{itemize}', tex_content)
    tex_content = pattern3.sub(r'\\begin{mdframed}', tex_content)

    return tex_content


def clean_pattern_replace(input_path):
    # Construct the full file path
    file_path = os.path.join(input_path, "main.tex")

    # Read the input main.tex file
    with open(file_path, "r", encoding="utf-8") as tex_file:
        tex_content = tex_file.read()

    # Apply replacements for the specified patterns
    tex_content = replacement_patterns(tex_content)

    # Save the cleaned content back to the same file
    with open(file_path, "w", encoding="utf-8") as tex_file:
        tex_file.write(tex_content)

    logging.debug(f"{file_path} cleaned successfully.")


if __name__ == "__main__":
    # Specify the input path
    input_path = "/path/to/your/project"

    # Process the LaTeX file in the specified input path
    clean_string_replace(input_path)
