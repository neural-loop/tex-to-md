import re
import sys


def replace_figure(match):
    figure_content = match.group(1)
    # Use regular expressions to extract the image filename, caption, and label
    caption_match = re.search(r'\\caption{([^{}]*(?:{[^{}]*}[^{}]*)*)}', figure_content)
    includegraphics_match = re.search(r'\\includegraphics\{([^}]+)\}', figure_content)
    label_match = re.search(r'\\label{([^}]+)}', figure_content)

    if caption_match and includegraphics_match and label_match:
        caption = caption_match.group(1)
        image_filename = includegraphics_match.group(1)
        label = label_match.group(1)
        label = label.casefold().replace('fig:', '')
        # Construct the Markdown image syntax with the Fig value as the ID
        image_filename = image_filename.replace('.pdf', '.png')
        image_filename = image_filename.replace('figures/', 'images/')
        markdown_image = (f'<div id="{label.lower()}" class="flex items-center justify-center">'
                          '{{< image src="' + image_filename + '" caption="' + caption + '" zoomable="true" >}}'
                          f'</div>\n')
        return markdown_image
    elif caption_match and includegraphics_match:
        caption = caption_match.group(1)
        image_filename = includegraphics_match.group(1)
        # Construct the Markdown image syntax with the Fig value as the ID
        image_filename = image_filename.replace('.pdf', '.png')
        image_filename = image_filename.replace('figures/', 'images/')
        markdown_image = (f'<div id="{label.lower()}" class="flex items-center justify-center">'
                          '{{< image src="' + image_filename + '" caption="' + caption + '" zoomable="true" >}}'
                          f'</div>\n')
        return markdown_image
    else:
        return match.group(1) + f"<br>{caption_match}"  # Include the <br> for wrapfigure



def process_figures(input_path, output_path):
    # Read the input .tex file
    with open(input_path, "r", encoding="utf-8") as tex_file:
        tex_content = tex_file.read()

    # Replace LaTeX figure and wrapfigure environments with Markdown image syntax
    tex_content = re.sub(r'\\begin{figure}(.*?)\\end{figure\*?}', replace_figure, tex_content, flags=re.DOTALL)
    tex_content = re.sub(r'\\begin{wrapfigure}(.*?)\\end{wrapfigure}', replace_figure, tex_content, flags=re.DOTALL)
    tex_content = re.sub(r'\\begin{wrapfigure}(.*?)\\end{wrapfigure}<br>', replace_figure, tex_content,
                         flags=re.DOTALL)

    with open(output_path, "w", encoding="utf-8") as md_file:
        md_file.write(tex_content)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python process_figures.py <input_file_path> <output_file_path>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    process_figures(input_file_path, output_file_path)
