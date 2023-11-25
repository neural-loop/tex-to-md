import re
import sys

def process_figures(input_file_path, output_file_path):
    # Read the input file
    with open(input_file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Perform processing on the content (e.g., removing \normalsize)
    content = re.sub(r'{\\normalsize\s+(.*?)}', r'\1', content)

    # Save the transformed content
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write(content)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python normalsize.py <input_file_path> <output_file_path>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    process_figures(input_file_path, output_file_path)
