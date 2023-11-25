import os
import shutil
import logging

def copy_images(input_path, output_path):
    # Check if input directory exists
    if not os.path.exists(input_path):
        logging.warning(f"Input directory '{input_path}' does not exist. Skipping image copy.")
        return

    # Check if output directory exists, if not, create it
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Iterate over all files in the input directory
    for filename in os.listdir(input_path):
        # Check if the file is an image
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg')):
            # Construct full file paths
            source = os.path.join(input_path, filename)
            destination = os.path.join(output_path, filename)
            # Copy the file
            shutil.copy2(source, destination)
            logging.debug(f"Copied image {filename}")

    logging.info("Copied all images")

