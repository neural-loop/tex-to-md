import re
import os

def tex_mdframed(input_path):
    file_path = os.path.join(input_path, "main.tex")

    with open(file_path, "r", encoding="utf-8") as tex_file:
        tex_content = tex_file.read()

    # Define the pattern to match nested mdframed within quote within figure
    pattern = re.compile(r'(\\begin{figure}(.*?(\\begin{mdframed}).*?\\end{mdframed}).*?\\end{figure})', re.DOTALL)

    # Wrap the matched content with the specified HTML div
    def replace(match):
        return f'<div class="px-3 pt-5 pb-5 bg-theme-light dark:bg-darkmode-theme-light rounded">{match.group(1)}</div>'

    # Replace matching patterns with the wrapped HTML div
    tex_content = pattern.sub(replace, tex_content)

    # Save the modified content back to the file
    with open(file_path, "w", encoding="utf-8") as tex_file:
        tex_file.write(tex_content)
