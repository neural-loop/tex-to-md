import os
import re
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

def read_bib_file(bib_path):
    with open(bib_path, 'r', encoding='utf-8') as bib_file:
        return bib_file.read()

def parse_bib_entries(bib_content):
    bib_db = bibtexparser.loads(bib_content)
    return bib_db.entries

def format_bib_entries(bib_entries):
    formatted_entries = ""
    for entry in bib_entries:
        formatted_entries += f"@{entry['ENTRYTYPE']}{{"
        formatted_entries += f"{entry['ID']},\n"
        for field, value in entry.items():
            if field not in ('ENTRYTYPE', 'ID'):
                formatted_entries += f"  {field} = {{{value}}},\n"
        formatted_entries += "}\n\n"
    return formatted_entries

def update_index_md(md_path, formatted_bib_entries):
    index_md_path = os.path.join(md_path, 'index.md')

    # Append the formatted bibliography content to the end of the index.md file
    with open(index_md_path, 'a', encoding='utf-8') as index_md_file:
        index_md_file.write("\n\n## Bibliography\n")
        index_md_file.write('<div id="biblio">{{< highlight bibtex "linenos=inline,anchorlinenos=true,lineanchors=line" >}}\n')
        index_md_file.write(formatted_bib_entries)
        index_md_file.write('{{< / highlight >}}</div>\n')

def tex_bibliography(tex_path, md_path):
    main_tex_path = os.path.join(tex_path, 'main.tex')
    bib_name_match = re.search(r'(?:\\bibliography|\\addbibresource)\{([^}]*)\}', open(main_tex_path).read())

    if bib_name_match:
        bib_name = bib_name_match.group(1)
        bib_path = os.path.join(tex_path, f'{bib_name}')
        if not bib_path.endswith('.bib'):
            bib_path += '.bib'

        if os.path.exists(bib_path):
            bib_content = read_bib_file(bib_path)
            bib_entries = parse_bib_entries(bib_content)
            formatted_bib_entries = format_bib_entries(bib_entries)
            update_index_md(md_path, formatted_bib_entries)
            print(f"Bibliography content from '{bib_path}' successfully appended to 'index.md'.")
        else:
            print(f"Bibliography file '{bib_path}' not found.")
    else:
        print("No \\bibliography tag found in the main.tex file.")

if __name__ == "__main__":
    # Replace 'your_input_path' with the actual path to your input directory
    tex_bibliography('your_input_path', 'your_output_path')
