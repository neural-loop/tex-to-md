import os
import re
from slugify import slugify
import logging

def process_figures_in_file(file_content):
    figure_pattern = r'\\begin\{figure\}(.*?)\\end\{figure\}'
    # img_pattern = r'\\includegraphics\[.*?\]\{(.*?)\}'
    # img_pattern = r'\\includegraphics\{(.*?)\}'
    img_pattern = r'\\includegraphics(?:\[.*?\])?\{(.*?)\}'
    caption_pattern = r'\\caption\{((?:[^{}]|{[^{}]*})*)\}'
    label_pattern = r'\\label\{(.*?)\}'

    valid_extensions = ['.eps', '.svg', '.jpg', '.jpeg', '.gif', '.png', '.pdf']

    matches = re.finditer(figure_pattern, file_content, re.DOTALL)
    for match in matches:
        match_content = match.group(0)

        img_matches = re.finditer(img_pattern, match_content)
        caption_match = re.search(caption_pattern, match_content)
        label_match = re.search(label_pattern, match_content)

        image_filenames = [img_match.group(1) for img_match in img_matches] if img_matches else []
        caption = caption_match.group(1) if caption_match else ""
        label = label_match.group(1) if label_match else ""
        slugified_label = slugify(label)

        logging.info(' Match: ' + str(image_filenames))

        # Check if any image has a valid extension
        if not any(image_filename.lower().endswith(tuple(valid_extensions)) for image_filename in image_filenames):
            logging.info(f"Invalid image extension for {label}. Skipping replacement.")
            continue

        escaped_caption = caption.replace('"', '\'').replace('\n', ' ').strip()

        # remove label from caption
        caption = caption.replace(label, '')

        markdown_images = []
        for image_filename in image_filenames:
            markdown_image = (
                f'<div id="{slugified_label}" class="flex items-center justify-center">'
                '\{\{< image src="' + image_filename +
                '" caption="' + escaped_caption +
                '" zoomable="true" >\}\}'
                '</div>\n\n'
            )
            markdown_images.append(markdown_image)

        # Replace the entire figure block with the new markdown images
        new_figure_content = '\n'.join(markdown_images)
        file_content = file_content.replace(match_content, new_figure_content)

    return file_content.strip()

def tex_figures(input_path):
    file_path = os.path.join(input_path, "main.tex")

    logging.info(' TexFile: ' + file_path)
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    updated_content = process_figures_in_file(content)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)

if __name__ == "__main__":
    # Specify the input path
    input_path = "/path/to/your/project"

    # Process the LaTeX file in the specified input path
    tex_figures(input_path)
