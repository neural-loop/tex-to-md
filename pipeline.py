import os
import logging
import traceback

logging.basicConfig(filename='app.log', filemode='w', format='%(filename)-25s|%(levelname)s|%(message)s', level=logging.INFO)

from steps.pre.move_files import move_files
from steps.pre.setup_filenames import setup_filenames
from steps.pre.clean_string_replace import clean_string_replace
from steps.pre.clean_pattern_replace import clean_pattern_replace
from steps.tex_refs import tex_refs
from steps.tex_itemize import tex_itemize
from steps.tex_fig import tex_fig
from steps.tex_tables import tex_tables
from steps.pre.tex_input import tex_input
from steps.tex_bibliography import tex_bibliography
from steps.tex_to_md import tex_to_md
from steps.post.post_md_clean import post_md_clean
from steps.post.frontmatter import frontmatter
from steps.pre.clean_comments import clean_comments
from steps.post.copy_images import copy_images
from steps.post.copy_pdf import copy_pdf
from steps.tex_labels import tex_labels
from steps.tex_mdframed import tex_mdframed
from steps.post.post_attribution import post_attribution
from steps.pre.pre_remove_formula import pre_remove_formula
from steps.post.post_clean_string_replace import post_clean_string_replace
from steps.pre.pre_tex_to_md import pre_tex_to_md

def preprocess_directories(input_path, preprocess_path, nogo_path, equations_path):
    if os.path.exists(preprocess_path):
        os.system('rm -rf ' + preprocess_path)
    os.mkdir(preprocess_path)
    if not os.path.exists(nogo_path):
        os.mkdir(nogo_path)

    directories = [d for d in os.listdir(input_path) if os.path.isdir(os.path.join(input_path, d))]

    for docname in directories:
        logging.info(f"Preprocessing: {docname}")
        print(f"Preprocessing: {docname}")
        current_input_path = os.path.join(input_path, docname)
        current_preprocess_path = os.path.join(preprocess_path, docname)

        move_files(current_input_path, current_preprocess_path)
        setup_filenames(current_preprocess_path)
        error_code = pre_remove_formula(current_preprocess_path)
        if error_code != 2:
            error_code = pre_tex_to_md(current_preprocess_path)

        if error_code == 0:
            logging.info(f"Preprocessing complete. Output written to {current_preprocess_path}")
        if error_code == 1:
            logging.error(f"Preprocessing failed. Output written to {current_preprocess_path}")
            destination_path = os.path.join(nogo_path, docname)
            if not os.path.exists(destination_path):
                os.rename(current_input_path, destination_path)
                logging.info(f"File moved to {destination_path}")
            else:
                logging.warning(f"File already exists in {destination_path}. Skipping move.")
        if error_code == 2:
            logging.error(f"Preprocessing failed. Output written to {current_preprocess_path}")
            destination_path = os.path.join(equations_path, docname)
            if not os.path.exists(destination_path):
                os.rename(current_input_path, destination_path)
                logging.info(f"File moved to {destination_path}")
            else:
                logging.warning(f"File already exists in {destination_path}. Skipping move.")

    return directories

def process_directories(input_path, preprocess_path, output_path, nogo_path, equations_path, directories):
    if os.path.exists(preprocess_path):
        os.system('rm -rf ' + preprocess_path)
    os.mkdir(preprocess_path)
    if os.path.exists(output_path):
        os.system('rm -rf ' + output_path)
    os.mkdir(output_path)
    if not os.path.exists(nogo_path):
        os.mkdir(nogo_path)

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

            tex_fig(current_preprocess_path)
            tex_tables(current_preprocess_path)
            tex_mdframed(current_preprocess_path)
            tex_refs(current_preprocess_path)
            tex_itemize(current_preprocess_path)
            tex_labels(current_preprocess_path)

                # tex_citations(current_preprocess_path)
                # tex_citations_group(current_preprocess_path+'/main.tex', current_preprocess_path+'/main.bib', current_preprocess_path+'/main.tex'),

            # tex_getbody(current_preprocess_path)
            tex_to_md(current_preprocess_path, current_output_path)

            post_md_clean(current_output_path+'/index.md')
            post_clean_string_replace(current_output_path+'/index.md')
            frontmatter(current_preprocess_path+'/meta/', current_output_path)
            tex_bibliography(current_preprocess_path, current_output_path)
            post_attribution(current_output_path)
            copy_pdf(current_preprocess_path+'/meta/', current_output_path)
            copy_images(current_preprocess_path+'/images-preprocess', current_output_path+'/images-preprocess')

        except Exception as e:
            logging.error(f"Error processing {docname}: {str(e)}")
            traceback.print_exc()  # Add this line to print the full stack trace
            # os.rename(current_input_path, os.path.join(nogo_path, docname))
            # continue
            break

    logging.shutdown()

# Define paths
input_path = 'inputs/source'
preprocess_path = input_path + '-preprocess'
output_path = '/home/iguana/WebstormProjects/website/content/english/neuromorphic/papers'
failed_nogo = 'inputs/failed'
failed_equation = 'inputs/failed/equations'
debugrun = 'neuromorphic-analog-circuits-robust-on-chip-always-on-learning-spiking-neural-networks'


# Preprocess directories
# directories = preprocess_directories(input_path, preprocess_path, failed_nogo, failed_equation)

# Process directories
if debugrun:
    # Only process the specified directory when debugrun is set
        process_directories(input_path, preprocess_path, output_path, failed_nogo, failed_equation, [debugrun])
else:
    # Process all directories
    process_directories(input_path, preprocess_path, output_path, failed_nogo, failed_equation, directories)
