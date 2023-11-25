import os
import re
import sys
import shutil
from pdf2image import convert_from_path

image_path = "images"

def preprocess_pdf(input_pdf, output_pdf):
    # Use pdftocairo to convert PDF to PDF with all layers flattened
    os.system(f"pdftocairo -pdf {input_pdf} {output_pdf}")

def get_figure_paths(match):
    figure_content = match.group(1)
    # Use regular expressions to extract the image filename
    includegraphics_match = re.search(r'\\includegraphics\{([^}]+)\}', figure_content)
    if includegraphics_match:
        image_filename = includegraphics_match.group(1)  # may include path part path/filename
        target_file = os.path.join(input_path, image_filename)
        output_file = os.path.join(input_path, image_filename.replace('figures', 'images'))
        print(target_file)
        print(output_file)
        # Make the images folder if it doesn't exist
        os.makedirs(input_path + '/' + image_path, exist_ok=True)

        if os.path.exists(target_file):
            if target_file.lower().endswith('.pdf'):
                # Preprocess PDF to flatten layers
                preprocessed_pdf = os.path.join(image_path, 'preprocessed_temp.pdf')
                preprocess_pdf(target_file, preprocessed_pdf)

                # Convert preprocessed PDF to PNG
                images = convert_from_path(preprocessed_pdf)
                output_file = output_file.replace('.pdf', '.png')
                images[0].save(output_file, 'PNG')

                # Remove temporary preprocessed PDF
                os.remove(preprocessed_pdf)
            else:
                # Copy other image types
                os.makedirs(os.path.dirname(output_file), exist_ok=True)
                shutil.copyfile(target_file, output_file)

    return match.group(0)  # Return the original figure if no match

def print_image_filenames_in_tex(input_path):
    # Read the input .tex file
    with open(input_path, "r", encoding="utf-8") as tex_file:
        tex_content = tex_file.read()

    # Find image filenames in LaTeX figure and wrapfigure environments
    re.sub(r'\\begin{figure}(.*?)\\end{figure\*?}', get_figure_paths, tex_content, flags=re.DOTALL)
    re.sub(r'\\begin{wrapfigure}(.*?)\\end{wrapfigure}', get_figure_paths, tex_content, flags=re.DOTALL)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python print_image_filenames.py <input_file_path>")
        sys.exit(1)

    input_path = sys.argv[1]  # path to working dir / contents
    input_file = sys.argv[2]  # markdown file to search for figure images

    print_image_filenames_in_tex(input_file)
