import os
import argparse
import logging
import shutil


def frontmatter(input_path, output_path):
    # Read content from metadata.txt
    metadata_path = os.path.join(input_path, 'metadata.txt')
    with open(metadata_path, 'r') as metadata_file:
        metadata_content = metadata_file.read()

    # Read content from existing index.md
    index_path = os.path.join(output_path, 'index.md')
    with open(index_path, 'r') as index_file:
        existing_content = index_file.read()

    # Insert metadata content into the frontmatter
    new_content = f'---\n{metadata_content}pdf: main.pdf\nimage: img.png\n---\n\n{existing_content}'

    # Write the updated content back to index.md
    with open(index_path, 'w') as index_file:
        index_file.write(new_content)

    # copy from assets/img.png to output_path
    shutil.copy2(os.path.join("assets", "img.png"), output_path)

    logging.info(f"Frontmatter inserted. Output written to {index_path}")