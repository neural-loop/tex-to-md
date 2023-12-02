import logging
import subprocess
from pathlib import Path
from PIL import Image
from slugify import slugify

def filesystem_operation(fs_from_img, fs_dest_img):
    def preprocess_pdf(input_pdf, output_png):
        logging.info(f" Preprocessing {input_pdf} -> {output_png}")

        try:
            subprocess.run(["pdftocairo", "-png", "-singlefile", input_pdf, output_png.replace('.png', '')])
            logging.info(f'PDF Converted -> {output_png}')
        except subprocess.CalledProcessError as e:
            logging.error(f"Error converting PDF to PNG: {e}")

    def convert_to_png(input_image, output_image):
        # Convert various image formats to PNG
        image = Image.open(input_image)
        image.save(output_image, 'PNG')

    def upscale_png(input_image, output_image, target_width=1920, target_height=1080, fill_background=True):
        # Open the image
        image = Image.open(input_image)

        if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
            # Create a new image with a white background
            background = Image.new('RGBA', image.size, (255, 255, 255, 255))

            # Check if the tuple has enough elements before accessing index 3
            if len(image.split()) > 3:
                background.paste(image, mask=image.split()[3])  # Paste image with alpha channel
            else:
                background.paste(image)

            image = background.convert('RGB')  # Convert to RGB for resizing
        elif fill_background:
            # If no alpha channel but fill_background is True, create a new image with white background
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image)
            image = background

        # Calculate the scaling factor for width and height
        width_ratio = target_width / image.width
        height_ratio = target_height / image.height

        # Choose the smaller scaling factor to maintain aspect ratio
        scaling_factor = min(width_ratio, height_ratio)

        # Calculate the new width and height
        new_width = int(image.width * scaling_factor)
        new_height = int(image.height * scaling_factor)

        # Resize the image
        resized_image = image.resize((new_width, new_height), Image.LANCZOS)

        # Save the resized image as PNG
        resized_image.save(output_image, 'PNG')

    Path(os.path.dirname(fs_dest_img)).mkdir(parents=True, exist_ok=True)
    if fs_from_img.endswith('.pdf'):
        preprocess_pdf(fs_from_img, fs_dest_img)
    elif fs_from_img.endswith(('.eps', '.svg', '.jpg', '.jpeg', '.gif', '.png')):
        convert_to_png(fs_from_img, fs_dest_img)
    else:
        logging.error(
            f"Error: Unsupported file format for '{fs_from_img}'. Only PDF, EPS, SVG, JPG, JPEG, GIF, and PNG are supported.")
        return match.group(0)
    upscale_png(fs_dest_img, fs_dest_img)

import re

def parse_graphicspath(tex_content):
    # Define the pattern for extracting \graphicspath
    graphicspath_pattern = re.compile(r'\\graphicspath\s*\{((?:[^{}]|{[^{}]*})*)\}')

    # Find all matches
    graphicspath_matches = graphicspath_pattern.findall(tex_content)

    # Process each match to create a list of paths
    paths = []
    for match in graphicspath_matches:
        # Remove extra spaces and split by '} {' or '}{' to get individual paths
        paths += [path.strip(' {}').replace('./', '') for path in re.split(r'\} ?\{|\}\{', match)]

    logging.info(f"graphicspath: {paths}")
    return paths



def tex_fig(tex_path):
    with open(os.path.join(tex_path, 'main.tex'), "r", encoding="utf-8") as tex_file:
        tex_content = tex_file.read()

    prepend_paths = parse_graphicspath(tex_content)
    # Find image filenames in LaTeX figure and wrapfigure environments
    tex_content = re.sub(r'\\begin{figure}(.*?)\\end{figure\*?}',
                         lambda match: process_figure(tex_path, match, prepend_paths),
                         tex_content, flags=re.DOTALL)
    tex_content = re.sub(r'\\begin{wrapfigure}(.*?)\\end{wrapfigure}',
                         lambda match: process_figure(tex_path, match, prepend_paths),
                         tex_content, flags=re.DOTALL)

    # Write the updated content back to the same file
    with open(os.path.join(tex_path, 'main.tex'), "w", encoding="utf-8") as tex_file:
        tex_file.write(tex_content)
def create_markdown(filenames, label, caption):
    escaped_caption = caption.replace('"', '\'').replace('\n', ' ').strip()
    # Check if the escaped_caption is not an empty string before manipulating it
    if escaped_caption:
        # Capitalize the first letter of the caption
        escaped_caption = escaped_caption[0].upper() + escaped_caption[1:]

    # Remove \label{...} from the caption
    escaped_caption = re.sub(r'\\label\{(.*?)\}', '', escaped_caption)

    slugified_label = ''
    if label:
        slugified_label = slugify(label)
        id_part = f'id="<br>Figure: {slugified_label}" '
    else:
        id_part = ''

    markdown_images = f'<div {id_part}class="bg-blue-100 dark:bg-darkmode-theme-light pt-4 px-6 pb-0 rounded items-center justify-center">'
    markdown_images += f'<figcaption class="text-2xl font-semibold">{escaped_caption}{slugified_label}</figcaption>\n\n' if escaped_caption else ''
    for filename in filenames:
        markdown_images += (
                '\{\{< image src="' + filename +
                '" alt="' + escaped_caption +
                '" zoomable="true" class="m-0 p-4 bg-white rounded">\}\}'
        )
    markdown_images += '</div>\n\n'
    return markdown_images


def png_filename(filepath):
    path, filename = os.path.split(filepath)
    return os.path.join(path, os.path.splitext(filename)[0] + '.png')

import os

def find_supported_file(tex_path, tex_from_img, supported_extensions, prepend_path):
    print(f"Searching for supported file for '{tex_from_img}'.")
    # If tex_from_img already has an extension, check if the file exists
    if any(tex_from_img.endswith(ext) for ext in supported_extensions):
        for path in prepend_path:
            print(f"Searching for '{tex_from_img}' in '{path}'.")
            full_path = os.path.join(tex_path, path, tex_from_img)
            if os.path.isfile(full_path):
                print(f"Found supported file (w ext) for '{tex_from_img}' in '{path}'.")
                return os.path.join(path, tex_from_img)
    else:
        # If tex_from_img doesn't have an extension, search for the matching file
        for ext in supported_extensions:
            for path in prepend_path:
                print(f"Searching for '{tex_from_img}{ext}' in '{path}'.")
                full_path = os.path.join(tex_path, path, tex_from_img + ext)
                if os.path.isfile(full_path):
                    print(f"Found supported file (woext) for '{tex_from_img}{ext}' in '{path}'.")
                    return os.path.join(path, tex_from_img + ext)
    return None



def process_figure(tex_path, match, graphics_paths):
    logging.info(f"Processing figure environment:\n{match.group(0)}")
    supported_extensions = ('.pdf', '.eps', '.svg', '.jpg', '.jpeg', '.gif', '.png')

    caption_match = re.search(r'\\caption\{((?:[^{}]|{[^{}]*})*)\}', match.group(1))
    label_match = re.search(r'\\label\{(.*?)\}', match.group(1))

    # Find all includegraphics within the figure environment
    includegraphics = re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', match.group(1))

    if includegraphics:
        image_filenames = []
        for tex_from_img in includegraphics:
            found_file = find_supported_file(tex_path, tex_from_img, supported_extensions, graphics_paths)

            if not found_file:
                logging.error(f"Error: No supported file found for '{tex_from_img}'.")
                print(f"Error: No supported file found for '{tex_from_img}'.")
                return match.group(0)  # Return the original match if no supported file is found

            tex_dest_img = os.path.join('images-preprocess/', png_filename(found_file))
            fs_from_img = os.path.join(tex_path, found_file)
            fs_dest_img = os.path.join(tex_path, 'images-preprocess/', png_filename(found_file))

            logging.info('\ntex_from_img:\t%s\n'
                         'tex_dest_img:\t%s\n'
                         'fs_from_img:\t%s\n'
                         'fs_dest_img:\t%s\n'
                         'lbl_match:\t%s\n'
                         'cap_match:\t%s\n',
                         tex_from_img, tex_dest_img, fs_from_img, fs_dest_img,
                         label_match.group(1) if label_match else "",
                         caption_match.group(1) if caption_match else "")

            image_filenames.append(tex_dest_img)
            filesystem_operation(fs_from_img, fs_dest_img)

        markdown = create_markdown(image_filenames, label_match.group(1) if label_match else "",
                                   caption_match.group(1) if caption_match else "")
        return markdown
    else:
        logging.error(f"Error: No image found in figure environment.")
        return match.group(0)
