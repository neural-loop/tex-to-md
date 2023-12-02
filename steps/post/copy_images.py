import os
import shutil
import logging

def copy_images(input_dir, output_dir):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Walk through the input directory and copy files and directories
    for root, dirs, files in os.walk(input_dir):
        # Create corresponding directories in the output directory
        for dir_name in dirs:
            input_path = os.path.join(root, dir_name)
            output_path = os.path.join(output_dir, os.path.relpath(input_path, input_dir))
            if not os.path.exists(output_path):
                os.makedirs(output_path)

        # Copy files to the output directory
        for file_name in files:
            input_path = os.path.join(root, file_name)
            output_path = os.path.join(output_dir, os.path.relpath(input_path, input_dir))
            shutil.copy2(input_path, output_path)
