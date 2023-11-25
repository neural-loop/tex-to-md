import os
import shutil
import argparse
import logging

def move_files(input_dir, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Walk through the input directory
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            # Convert filename to lowercase
            lower_file = file.lower()

            input_path = os.path.join(root, file)
            output_path = os.path.join(output_dir, os.path.relpath(input_path, input_dir))

            # Ensure the output directory structure exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Use the lowercase filename
            shutil.copy2(input_path, os.path.join(os.path.dirname(output_path), lower_file))

