import os
import re

def read_bib_file(bib_path):
    if not bib_path.endswith('.bib'):
        bib_path += '.bib'

    with open(bib_path, 'r', encoding='utf-8') as bib_file:
        return bib_file.read()

def update_main_tex(main_tex_path, bib_content):
    with open(main_tex_path, 'a', encoding='utf-8') as main_tex_file:
        # Append the formatted bibliography content to the end of the file
        main_tex_file.write("\n\n## Bibliography\n")
        main_tex_file.write('<div id="biblio">\{\{< highlight bibtex "linenos=inline,anchorlinenos=true,lineanchors=line" >\}\}\n')
        main_tex_file.write(bib_content)
        main_tex_file.write('\n\{\{< / highlight >\}\}</div>\n')

def tex_bibliography(input_path):
    # Construct the path to main.tex
    main_tex_path = os.path.join(input_path, 'main.tex')

    bib_name_match = re.search(r'\\bibliography\{([^}]*)\}', open(main_tex_path).read())
    if bib_name_match:
        bib_name = bib_name_match.group(1)
        bib_path = os.path.join(input_path, f'{bib_name}.bib')
        if os.path.exists(bib_path):
            bib_content = read_bib_file(bib_path)
            update_main_tex(main_tex_path, bib_content)
            print(f"Bibliography content from '{bib_path}' successfully appended to '{main_tex_path}'.")
        else:
            print(f"Bibliography file '{bib_path}' not found.")
    else:
        print("No \\bibliography tag found in the main.tex file.")

if __name__ == "__main__":
    # Replace 'your_input_path' with the actual path to your input directory
    tex_bibliography('your_input_path')
