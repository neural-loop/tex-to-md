import re
import sys

# Custom function to process matches
def process_match(match):
    value = match.group(1)
    # Replace colons with dashes in the value
    value = value.replace(":", "-")
    value = value.replace(".", "-")
    # Return the modified reference
    return f"<a href='#{value}'>{value}</a>"

def process_references(input_path, output_path):
    # Read the input .tex file
    with open(input_path, "r", encoding="utf-8") as tex_file:
        tex_content = tex_file.read()

    # Replace \Cref{value} with the result of the custom function
    tex_content = re.sub(r'\\Cref{([^}]*)}', process_match, tex_content)

    # Save the transformed content as Markdown
    with open(output_path, "w", encoding="utf-8") as md_file:
        md_file.write(tex_content)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python process_references.py <input_file_path> <output_file_path>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    process_references(input_file_path, output_file_path)
