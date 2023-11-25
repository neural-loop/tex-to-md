import re
import sys

def process_citations(input_md_path, bib_path, output_md_path):
    # Read the input .md file
    with open(input_md_path, "r", encoding="utf-8") as md_file:
        md_content = md_file.read()

    md_content = md_content.replace("_):}", "}_):}")

    # Define a function to handle the replacement for citations
    def replace_citations(match):
        citations = match.group(1).split(',')
        markdown_citations = []
        with open(bib_path, "r", encoding="utf-8") as bib_file:
            for i, citation in enumerate(citations, start=1):
                # find citation.strip() in bib_content and return the line number
                for num, line in enumerate(bib_file, 1):
                    if citation.strip() in line:
                        # Add brackets around each citation and title attribute to the anchor link
                        markdown_citations.append(f"[*](#line-{num} '{citation.strip()}')")
                        break
                bib_file.seek(0)  # Reset file pointer to the beginning for the next citation

        # Combine all citations into a single <sup> element without commas
        return f"<sup>{''.join(markdown_citations)}</sup>"

    # Replace \cite{...} with citations wrapped in <sup> and </sup> tags
    md_content = re.sub(r'\\cite{([^}]+)}', replace_citations, md_content)

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

    process_citations(input_md_path, bib_path, output_md_path)
