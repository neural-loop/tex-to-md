import re
import sys

def update_latex_operators(input_path, output_path):
    # Read the input .tex file
    with open(input_path, "r", encoding="utf-8") as tex_file:
        tex_content = tex_file.read()

    # Update latex operators $$ \argmax $$ and $$ \argmin $$ to \arg\,max and \arg\,min
    tex_content = re.sub(r'\\argmax', r'\\arg\,max', tex_content, flags=re.DOTALL)
    tex_content = re.sub(r'\\argmin', r'\\arg\,min', tex_content, flags=re.DOTALL)

    # Update latex operators $$ \vect $$ to \boldsymbol
    tex_content = re.sub(r'\\vect', r'\\boldsymbol', tex_content, flags=re.DOTALL)

    # Update latex operators $$ \tensorsym $$ to \mathbf
    tex_content = re.sub(r'\\tensorsym', r'\\mathbf', tex_content, flags=re.DOTALL)

    # Save the transformed content as Markdown
    with open(output_path, "w", encoding="utf-8") as md_file:
        md_file.write(tex_content)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python update_latex_operators.py <input_file_path> <output_file_path>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    update_latex_operators(input_file_path, output_file_path)
