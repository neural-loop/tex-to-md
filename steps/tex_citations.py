import re
import sys


def tex_citations(input_md_path, bib_path, output_md_path):
    # Read the input .md file
    with open(input_md_path, "r", encoding="utf-8") as md_file:
        md_content = md_file.read()
    md_content = md_content.replace("_):}", "}_):}")

    # Define a function to handle the replacement for multiple citations
    def replace_citations(match):
        citations = re.findall(r'{(.+?)}', match.group())
        markdown_citations = []

        for citation in citations:
            # Skip citations with commas
            if ',' in citation:
                continue

            with open(bib_path, "r", encoding="utf-8") as bib_file:
                # find citation in bib_content and return the line number
                for num, line in enumerate(bib_file, 1):
                    if citation.strip() in line:
                        markdown_citations.append(f"<a title='{citation}' href='#line-{num}'>\*</a>")
                        break
                bib_file.seek(0)  # Reset file pointer to the beginning for the next citation

        return "<sup>{}</sup>".format(' '.join(markdown_citations))

    # Replace \cite{...} patterns with citations wrapped in <sup> and </sup> tags
    md_content = re.sub(r'(\\cite\{[^},]+\}\s*,?\s*)+', replace_citations, md_content)

    md_content = md_content.replace(" <sup>", "<sup>")
    # Save the transformed content as Markdown
    with open(output_md_path, "w", encoding="utf-8") as md_file:
        md_file.write(md_content)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python process_citations.py <input_md_file_path> <bib_file_path> <output_md_file_path>")
        sys.exit(1)

    input_md_path = sys.argv[1]
    bib_path = sys.argv[2]
    output_md_path = sys.argv[3]

    tex_citations(input_md_path, bib_path, output_md_path)
