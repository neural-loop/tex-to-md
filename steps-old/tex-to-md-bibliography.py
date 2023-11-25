import re
import sys

def merge_bibliography(input_tex_path, input_bib_path, output_md_path):
    # Read the input .tex file
    with open(input_tex_path, "r", encoding="utf-8") as tex_file:
        tex_content = tex_file.read()

    # Read the input .bib file
    with open(input_bib_path, "r", encoding="utf-8") as bib_file:
        bib_content = bib_file.read()

    # Get id lines from bib_content
    # Assuming you have a function or method to extract id lines from bib_content

    # Merge .tex and .bib content
    tex_content = tex_content + '## Bibliography\n<div id="biblio">{{< highlight bibtex "linenos=inline,anchorlinenos=true,lineanchors=line" >}}\n' + bib_content + '\n{{< / highlight >}}</div>'

    # Save the transformed content as Markdown
    with open(output_md_path, "w", encoding="utf-8") as md_file:
        md_file.write(tex_content)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python merge_bibliography.py <input_tex_file_path> <input_bib_file_path> <output_md_file_path>")
        sys.exit(1)

    input_tex_path = sys.argv[1]
    input_bib_path = sys.argv[2]
    output_md_path = sys.argv[3]

    merge_bibliography(input_tex_path, input_bib_path, output_md_path)
