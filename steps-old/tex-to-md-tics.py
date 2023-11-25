import re
import sys

def update_backticks(input_path, output_path):
    # Read the input .md file
    with open(input_path, "r", encoding="utf-8") as tex_file:
        tex_content = tex_file.read()

    # Define a regular expression pattern to match single backticks not followed by another backtick
    pattern = r'`(?![`])'

    # Use re.sub to replace single backticks
    tex_content = re.sub(pattern, r'\'', tex_content)

    # Save the transformed content as Markdown
    with open(output_path, "w", encoding="utf-8") as md_file:
        md_file.write(tex_content)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python update_backticks.py <input_file_path> <output_file_path>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    update_backticks(input_file_path, output_file_path)
