import re
import sys

def convert_equation(input_path, output_path):
    # Read the input .md file
    with open(input_path, "r", encoding="utf-8") as tex_file:
        tex_content = tex_file.read()

    # Define a function to convert LaTeX equations to Markdown format and remove labels
    def convert_equation_func(match):
        equation = match.group(1)

        # Replace \\ with \\\\ for markdown format
        equation_escaped = re.sub('\\\\\\\\', '\\\\\\\\\\\\\\\\', equation)

        # Remove \label{value} part from the equation
        equation_without_label = re.sub(r'\\label\{.*?\}', '', equation_escaped)

        # Escape underscores with double backslashes
        equation_cleaned = re.sub(r'_', '\\\\_', equation_without_label)

        # Remove line breaks and spaces
        equation_cleaned = re.sub(r'\n\s*', ' ', equation_cleaned)
        return f"$$ {equation_cleaned} $$"

    # Use a more flexible regular expression to find and replace LaTeX equations
    tex_content = re.sub(r'\\begin{equation}(.*?)\\end{equation}', convert_equation_func, tex_content, flags=re.DOTALL)

    # Save the transformed content as Markdown
    with open(output_path, "w", encoding="utf-8") as md_file:
        md_file.write(tex_content)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_equations.py <input_file_path> <output_file_path>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    convert_equation(input_file_path, output_file_path)
