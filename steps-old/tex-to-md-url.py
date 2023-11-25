import re
import sys

def process_urls(input_path, output_path):
    # Read the input .md file
    with open(input_path, "r", encoding="utf-8") as md_file:
        md_content = md_file.read()

    # Find and replace \url{https://www.example.com} with <a href="https://www.example.com" target="_blank">https://www.example.com</a>
    md_content = re.sub(r'\\url{([^}]*)}', r'<a href="\1" target="_blank">\1</a>', md_content)

    # Save the transformed content as Markdown
    with open(output_path, "w", encoding="utf-8") as md_file:
        md_file.write(md_content)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python process_urls.py <input_file_path> <output_file_path>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    process_urls(input_file_path, output_file_path)
