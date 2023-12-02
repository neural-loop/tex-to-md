import os
import argparse
import yaml  # Add this import for YAML parsing

def read_metadata(index_md_path):
    metadata = {}
    with open(index_md_path, 'r', encoding='utf-8') as index_md:
        lines = index_md.readlines()

    in_front_matter = False
    for line in lines:
        if line.strip() == '---':
            in_front_matter = not in_front_matter
            continue

        if in_front_matter:
            key, value = map(str.strip, line.split(':', 1))
            metadata[key] = value.strip('"')  # Strip quotes from the value

    return metadata

def generate_markdown(metadata):
    # Update Attribution section
    short_id = metadata.get('get_short_id', '')
    attribution = f"[arXiv:{short_id}]({metadata.get('entry_id', '')}) [{metadata.get('primary_category', '')}]"
    return f"\n\n## Attribution\n\n{attribution}<br>License: {metadata.get('license', '')}-4.0"

def append_to_index_md(index_md_path, markdown_content):
    with open(index_md_path, 'a', encoding='utf-8') as index_md:
        index_md.write(markdown_content)

def post_attribution(input_path):
    index_md_path = os.path.join(input_path, 'index.md')

    if not os.path.exists(index_md_path):
        print(f"Index.md file not found: {index_md_path}")
        return

    metadata = read_metadata(index_md_path)
    markdown_content = generate_markdown(metadata)

    if markdown_content:
        append_to_index_md(index_md_path, markdown_content)
        print("Markdown content appended successfully.")
    else:
        print("No valid short_id found in metadata.")

if __name__ == "__main__":
    main()
