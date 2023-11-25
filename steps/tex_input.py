import os
import re

def tex_input(current_preprocess_path):
    main_tex_path = os.path.join(current_preprocess_path, 'main.tex')

    # Read the content of main.tex
    with open(main_tex_path, 'r') as file:
        main_tex_content = file.read()

    # Find all \input{filename} patterns
    input_patterns = re.findall(r'\\input\{(.*?)\}', main_tex_content)

    # For each found pattern, read the corresponding file and replace the pattern with the file content
    for pattern in input_patterns:
        input_file_path = os.path.join(current_preprocess_path, pattern + '.tex')
        with open(input_file_path, 'r') as file:
            file_content = file.read()
        main_tex_content = main_tex_content.replace('\\input{' + pattern + '}', file_content)

    # Write the updated content back to main.tex
    with open(main_tex_path, 'w') as file:
        file.write(main_tex_content)