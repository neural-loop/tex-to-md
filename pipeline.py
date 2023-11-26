import os
from steps.move_and_resize_images import move_files
from steps.setup_filenames import setup_filenames
from steps.clean_string_replace import clean_string_replace
from steps.post_clean_string_replace import post_clean_string_replace
from steps.clean_pattern_replace import clean_pattern_replace
from steps.tex_refs import tex_refs
from steps.tex_itemize import tex_itemize
from steps.tex_figure_prep import tex_figure_prep
from steps.tex_tables import tex_tables
from steps.tex_input import tex_input
from steps.tex_figures import tex_figures
from steps.tex_to_md import tex_to_md
from steps.post_md_clean import post_md_clean
from steps.frontmatter import frontmatter
from steps.clean_comments import clean_comments
from steps.copy_images import copy_images
from steps.copy_pdf import copy_pdf
from steps.tex_labels import tex_labels
from steps.tex_mdframed import tex_mdframed
from steps.post_attribution import post_attribution
import logging

logging.basicConfig(filename='app.log', filemode='w', format='%(filename)-25s|%(levelname)s|%(message)s', level=logging.INFO)
input_path = 'inputs'
preprocess_path = input_path + '-preprocess'
output_path = '/home/iguana/WebstormProjects/website/content/english/ai-governance-organizations/papers'
# output_path = 'markdown'
nogo_path = 'failed'

if os.path.exists(preprocess_path):
    os.system('rm -rf ' + preprocess_path)
os.mkdir(preprocess_path)
if os.path.exists(output_path):
    os.system('rm -rf ' + output_path)
if not os.path.exists(nogo_path):
    os.mkdir(nogo_path)

directories = [d for d in os.listdir(input_path) if os.path.isdir(os.path.join(input_path, d))]

# Iterate through each directory
for docname in directories:
    try:
        logging.info(f"Processing {docname}")
        print(f"Processing {docname}")
        current_input_path = os.path.join(input_path, docname)
        current_preprocess_path = os.path.join(preprocess_path, docname)
        current_output_path = os.path.join(output_path, docname)

        move_files(current_input_path, current_preprocess_path)
        setup_filenames(current_preprocess_path)
        tex_input(current_preprocess_path)
        clean_comments(current_preprocess_path+'/main.tex')
        clean_string_replace(current_preprocess_path)
        clean_pattern_replace(current_preprocess_path)

        tex_figure_prep(current_preprocess_path) # run before labels
        tex_figures(current_preprocess_path)
        tex_tables(current_preprocess_path)
        tex_mdframed(current_preprocess_path)
        tex_refs(current_preprocess_path)
        tex_itemize(current_preprocess_path)
        # tex_labels(current_preprocess_path)

        tex_to_md(current_preprocess_path, current_output_path)
        post_md_clean(current_output_path+'/index.md')
        post_clean_string_replace(current_output_path+'/index.md')
        frontmatter(current_preprocess_path+'/meta/', current_output_path)
        post_attribution(current_output_path)
        copy_pdf(current_preprocess_path+'/meta/', current_output_path)
        copy_images(current_preprocess_path+'/images-preprocessed', current_output_path+'/images-preprocessed')
    except Exception as e:
        logging.error(f"Error processing {docname}: {str(e)}")
        print(f"Error processing {docname}: {str(e)}")
        # os.rename(current_input_path, os.path.join(nogo_path, docname))
        continue
