import os
import re
import sys


def find_bib_file(main_tex_path):
    tex_file_path = os.path.join(main_tex_path, 'main.tex')
    tex_content = open(tex_file_path).read()

    # Update the regular expression to match both \bibliography and \addbibresource
    bib_name_match = re.search(r'(?:\\bibliography|\\addbibresource)\{([^}]*)\}', tex_content)


    if bib_name_match:
        bib_name = bib_name_match.group(1)
        if not bib_name.endswith('.bib'):
            bib_name += '.bib'
        bib_path = os.path.join(main_tex_path, f'{bib_name}')
        return bib_path
    else:
        return None


def tex_citations(input_path):
    # Find the BibTeX file using the provided method
    bib_path = find_bib_file(input_path)
    if bib_path is None:
        print("No \\bibliography tag found in the main.tex file.")
        sys.exit(1)

    # Read the input .tex file
    with open(input_path+'/main.tex', "r", encoding="utf-8") as md_file:
        md_content = md_file.read()

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
                        # markdown_citations.append(f"#a title='{citation}' href='#line-{num}'#\*#/a#")
                        markdown_citations.append(f"[*](#line-{num} '{citation}')")
                        break
                bib_file.seek(0)  # Reset file pointer to the beginning for the next citation

        return "<sup>{}</sup>".format(' '.join(markdown_citations))

    # Replace \cite{...} patterns with citations wrapped in <sup> and </sup> tags
    md_content = re.sub(r'(\\cite\{[^},]+\}\s*,?\s*)+', replace_citations, md_content)
    md_content = re.sub(r'(\\cite\{[^\}]+\})', replace_citations, md_content)

    md_content = md_content.replace(" <sup>", "<sup>")
    # Save the transformed content
    with open(input_path+'/main.tex', "w", encoding="utf-8") as md_file:
        md_file.write(md_content)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python process_citations.py <input_output_md_file_path> <main_tex_file_path>")
        sys.exit(1)

    input_path = sys.argv[1]

    tex_citations(input_path)
