import re
import sys
import urllib.parse

def process_references(input_path, output_path):
    # Read the input .tex file
    with open(input_path, "r", encoding="utf-8") as tex_file:
        tex_content = tex_file.read()

    # Replace Figure~\ref{fig:*} references with <a href="#*">Display Text</a>
    tex_content = re.sub(r'(?i)Figure~\\ref\{fig:([^}]+)\}',
                         lambda match: generate_link(match.group(1)), tex_content)

    # Save the transformed content as Markdown
    with open(output_path, "w", encoding="utf-8") as md_file:
        md_file.write(tex_content)

def generate_link(caption):
    # Generate a slug-style display text
    display_text = caption.replace("_", " ")

    # Create the link with original formatting
    link = f'<a href="#{urllib.parse.quote(caption.lower())}">{display_text}</a>'

    return link

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python process_references.py <input_file_path> <output_file_path>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    process_references(input_file_path, output_file_path)
