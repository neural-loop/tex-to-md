import os
import shutil
import argparse
import logging

def setup_filenames(input_dir):
    # Check for main.tex
    main_tex_path = os.path.join(input_dir, "main.tex")
    if not os.path.exists(main_tex_path):
        tex_files = [file for file in os.listdir(input_dir) if file.lower().endswith('.tex')]

        if len(tex_files) == 1:
            # Rename the single .tex file to main.tex
            shutil.move(os.path.join(input_dir, tex_files[0]), main_tex_path)
            logging.info(f" Renamed {tex_files[0]} to main.tex")
        elif len(tex_files) > 1:
            logging.error("Multiple .tex files found. Please ensure there is only one main.tex or provide it explicitly.")
        else:
            logging.error("main.tex not found, and no .tex files are available.")