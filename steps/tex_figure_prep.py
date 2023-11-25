import os
import re
from pdf2image import convert_from_path
from PIL import Image
from pathlib import Path
import logging

image_path = "images-preprocessed"

def preprocess_pdf(input_pdf, output_png):
    # Use convert_from_path to convert PDF to images
    logging.info(f" Preprocessing {input_pdf} -> {output_png}")

    # check if file exists
    if os.path.isfile(output_png):
        logging.info(f"File already exists: {output_png}")
        return
    images = convert_from_path(input_pdf)
    for i, image in enumerate(images):
        image.save(f'{output_png}.png', 'PNG')
        print(f'FS PDF Converted -> {output_png}')

def convert_to_png(input_image, output_image):
    # Convert various image formats to PNG
    image = Image.open(input_image)
    image.save(output_image, 'PNG')


def get_figure_paths(input_path, match, prepend_img=None):
    # get graphics matches
    includegraphics_matches = re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', match.group(1))

    if not includegraphics_matches:
        return match.group(0)

    updated_tex_content = match.group(0)

    for latex_src_img in includegraphics_matches:
        latex_src_img_lower = latex_src_img.lower()
        if '.' not in latex_src_img:
            print(f' Figure without extension')
            supported_extensions = ('.pdf', '.eps', '.svg', '.jpg', '.jpeg', '.gif', '.png')
            for ext in supported_extensions:
                potential_path = os.path.join(input_path, f"{latex_src_img}{ext}")

                if os.path.isfile(potential_path):
                    updated_tex_content = updated_tex_content.replace(latex_src_img,
                                                                      f"{latex_src_img_lower}{ext}")
                    latex_src_img = f"{latex_src_img_lower}{ext}"
                    break
            else:
                logging.error(
                    f"Error: No supported file with extension {supported_extensions} found for '{latex_src_img}'.")

        # Prepend the graphics path if it is defined
        if prepend_img is not None:
            latex_src_img = os.path.join(prepend_img, latex_src_img)

        dest_latex_img_name = os.path.splitext(os.path.basename(latex_src_img_lower))[0] + ".png"
        latex_img_replace_full = os.path.join(input_path, latex_src_img).lower()

        destination_path = os.path.join(input_path, image_path, dest_latex_img_name)
        Path(os.path.dirname(destination_path)).mkdir(parents=True, exist_ok=True)
        if latex_img_replace_full.endswith('.pdf'):
            preprocess_pdf(latex_img_replace_full, destination_path.replace('.png', ''))
        # handle other types
        elif latex_img_replace_full.endswith(('.eps', '.svg', '.jpg', '.jpeg', '.gif', '.png')):
            convert_to_png(latex_img_replace_full, destination_path)
        else:
            logging.error(
                f"Error: Unsupported file format for '{latex_img_replace_full}'. Only PDF, EPS, SVG, JPG, JPEG, GIF, and PNG are supported.")
            return match.group(0)

        print(f'LX Updated Content: {latex_src_img}, {image_path}, {destination_path}')

        new_path = os.path.join(image_path, os.path.basename(destination_path))
        updated_tex_content = updated_tex_content.replace(latex_src_img, new_path.lower())

    return updated_tex_content
def tex_figure_prep(input_path):
    # Read the .tex file
    with open(input_path+'/main.tex', "r", encoding="utf-8") as tex_file:
        tex_content = tex_file.read()

    graphics_path_match = re.search(r'\\graphicspath\{\{(.+)\}\}', tex_content)
    if graphics_path_match:
        graphics_path = graphics_path_match.group(1)
        print(f"Found graphics path: {graphics_path}")
    else:
        graphics_path = None

    # Find image filenames in LaTeX figure and wrapfigure environments
    tex_content = re.sub(r'\\begin{figure}(.*?)\\end{figure\*?}',
                         lambda match: get_figure_paths(input_path, match, graphics_path),
                         tex_content, flags=re.DOTALL)
    tex_content = re.sub(r'\\begin{wrapfigure}(.*?)\\end{wrapfigure}',
                         lambda match: get_figure_paths(input_path, match, graphics_path),
                         tex_content, flags=re.DOTALL)

    # Write the updated content back to the same file
    with open(input_path+'/main.tex', "w", encoding="utf-8") as tex_file:
        tex_file.write(tex_content)

