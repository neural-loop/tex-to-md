import os
import shutil
import logging

def setup_filenames(input_dir, exclude_file="commands.tex"):
    # Check for main.tex
    main_tex_path = os.path.join(input_dir, "main.tex")
    if os.path.exists(main_tex_path):
        # logging.info("main.tex found.")
        return

    # Check for .bbl file
    bbl_files = [file for file in os.listdir(input_dir) if file.lower().endswith('.bbl')]

    if bbl_files:
        # Use the first .bbl file found to infer the corresponding .tex file
        base_name = os.path.splitext(bbl_files[0])[0]
        tex_file = base_name + '.tex'

        if os.path.exists(os.path.join(input_dir, tex_file)):
            # Rename the .tex file to main.tex
            shutil.move(os.path.join(input_dir, tex_file), main_tex_path)
            # logging.info(f"Renamed {tex_file} to main.tex based on {bbl_files[0]}")

            # Rename the .bbl file to main.bbl
            main_bbl_path = os.path.join(input_dir, "main.bbl")
            shutil.move(os.path.join(input_dir, bbl_files[0]), main_bbl_path)
            # logging.info(f"Renamed {bbl_files[0]} to main.bbl")

            return

    tex_files = [file for file in os.listdir(input_dir) if file.lower().endswith('.tex') and file != exclude_file]

    if len(tex_files) == 1:
        # Rename the single .tex file to main.tex
        shutil.move(os.path.join(input_dir, tex_files[0]), main_tex_path)
        # logging.info(f"Renamed {tex_files[0]} to main.tex")
    elif len(tex_files) > 1:
        logging.error("Multiple .tex files found. Please ensure there is only one main.tex or provide it explicitly.")
    else:
        logging.error(f"main.tex not found, and no .tex files (excluding {exclude_file}) are available.")
