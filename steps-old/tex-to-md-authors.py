import re
import sys

def process_author_section(input_path, output_path):
    # Read the input .md file
    with open(input_path, "r", encoding="utf-8") as md_file:
        md_content = md_file.read()

    # Define a regular expression pattern to match \author{...} with multiple lines and spacing
    author_pattern = r'\\author\s*{(.*?)}'

    # Use re.search with the re.DOTALL flag to find the match
    match = re.search(author_pattern, md_content, re.DOTALL)

    if match:
        author_contents = match.group(1)
        # Remove '\\\\' from author_contents
        author_contents = author_contents.replace('\\\\', '')
        author_contents = author_contents.replace('\\And', '\AND')

        # Remove all spaces before text in all lines
        author_contents = re.sub(r'^\s*', '', author_contents, flags=re.MULTILINE)
        author_contents = '\\AND\n' + author_contents

        author_contents = author_contents.replace('\\AND\n', '- ')
        # prepend any line that doesn't start with '-' with '    - '
        author_contents = re.sub(r'^([^-\n].*)$', r'  - \1', author_contents, flags=re.MULTILINE)

        author_contents = '{{< accordion title="Authors" >}}' + author_contents + '<p></p>{{< /accordion >}}'
        # Replace the original \author{...} content with the modified content in md_content
        md_content = re.sub(author_pattern, author_contents, md_content, flags=re.DOTALL)

        # Write the transformed content back to the specified output file
        with open(output_path, "w", encoding="utf-8") as md_file:
            md_file.write(md_content)
    else:
        print("No match found.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python process_author_section.py <input_file_path> <output_file_path>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    process_author_section(input_file_path, output_file_path)
