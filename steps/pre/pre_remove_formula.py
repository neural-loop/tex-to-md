import os
import re

def pre_remove_formula(input_path):
    tex_file_path = os.path.join(input_path, 'main.tex')

    if not os.path.exists(tex_file_path):
        return 'Error: main.tex not found'

    with open(tex_file_path, 'r', encoding='utf-8') as tex_file:
        tex_content = tex_file.read()

        # Define patterns for equations and graphicspath
        equation_patterns = [
            r'\\begin{equation\*?}'
        ]

        graphicspath_pattern = re.compile(r'\\graphicspath\s*\{(.+?)\}')

        # Check for equations
        for pattern in equation_patterns:
            if re.search(pattern, tex_content):
                return 2  # Equations found

        # Check for graphicspath
        graphicspath_matches = graphicspath_pattern.findall(tex_content)
        if graphicspath_matches:
            if len(graphicspath_matches) > 1:
                return 3  # Multiple entries found, indicating an error

