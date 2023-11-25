import arxiv
import requests
from bs4 import BeautifulSoup
import os
import tarfile
from slugify import slugify as standard_slugify
import shutil
import logging, arxiv

# logging.basicConfig(level=logging.DEBUG)

stopwords = [
    'a', 'an', 'the', 'and', 'but', 'or', 'nor', 'so', 'yet', 'at',
    'by', 'for', 'in', 'of', 'on', 'to', 'with', 'up', 'as', 'it',
    'I', 'you', 'he', 'she', 'we', 'they', 'me', 'him', 'her', 'us',
    'them', 'my', 'your', 'his', 'its', 'our', 'their', 'mine', 'yours',
    'hers', 'ours', 'theirs', 'whose', 'this', 'that', 'these', 'those',
    'which', 'who', 'whom', 'what', 'whose', 'where', 'when', 'why', 'how',
    'all', 'any', 'both', 'each', 'either', 'every', 'few', 'more', 'most',
    'neither', 'none', 'some', 'such', 'several', 'many', 'enough', 'fewer',
    'little', 'lot', 'lots', 'much', 'several', 'too', 'very', 'as', 'about',
    'above', 'after', 'before', 'between', 'during', 'without', 'through',
    'over', 'under', 'below', 'beneath', 'beside', 'along', 'around', 'among',
    'throughout', 'upon', 'with', 'within', 'amongst', 'toward', 'towards',
    'afterwards', 'backward', 'backwards', 'behind', 'forward', 'forwards',
    'elsewhere', 'here', 'there', 'everywhere', 'nowhere', 'somewhere'
]

def custom_slugify(text, stopwords=None):
    if stopwords:
        words = [word for word in text.split() if word.lower() not in stopwords]
        return standard_slugify(" ".join(words))
    else:
        return standard_slugify(text)

def handle_http_errors(response):
    if response.status_code != 200:
        raise Exception(f"HTTP request failed with status code {response.status_code}")

def get_license_type(license_href):
    license_mappings = {
        "http://arxiv.org/licenses/nonexclusive-distrib/1.0/": "other",
        "http://creativecommons.org/licenses/by/4.0/": "cc-by",
        "http://creativecommons.org/licenses/by-nc/4.0/": "cc-by-nc",
        "http://creativecommons.org/licenses/by-nc-nd/4.0/": "other",
        "http://creativecommons.org/licenses/by-nc-sa/4.0/": "cc-by-nc-sa",
        "http://creativecommons.org/licenses/by-nd/4.0/": "other",
        "http://creativecommons.org/licenses/by-sa/4.0/": "cc-by-sa",
    }
    return license_mappings.get(license_href, "other")

def search_arxiv(query):
    client = arxiv.Client()
    search = arxiv.Search(query=query, max_results=50, sort_by=arxiv.SortCriterion.SubmittedDate)
    return list(client.results(search))

def print_results(results):
    for idx, result in enumerate(results, start=1):
        print(dir(result))
        fields = ['title', 'entry_id', 'get_short_id', 'published', 'authors', 'primary_category', 'journal_ref']

        # Check if the directory already exists
        extract_directory = os.path.join("inputs", custom_slugify(result.title, stopwords=stopwords))
        if os.path.exists(extract_directory):
            print(f"Directory already exists, skipping download: {extract_directory}")
            continue  # Skip to the next result if the directory exists

        for field in fields:
            value = getattr(result, field, None)
            print(f"{field.capitalize()}: {value}")

        # Extract and print authors as a comma-delimited string
        authors = ', '.join(author.name for author in result.authors)
        print(f"Authors: {authors}")

        pageUrl = result.entry_id.replace("http:", "https:")
        response = requests.get(pageUrl)
        handle_http_errors(response)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        abs_license_div = soup.find('div', class_='abs-license')
        license_href = abs_license_div.find('a')['href']
        license_type = get_license_type(license_href)
        print(f"License: {license_type}")

        if license_type != "other":
            os.makedirs(extract_directory, exist_ok=True)

            # Download the source tarfile using the default filename
            tar_file_path = result.download_source(dirpath=extract_directory)

            with tarfile.open(tar_file_path, 'r:gz') as tar:
                tar.extractall(path=extract_directory)

            print(f"Downloaded and extracted: {tar_file_path} to {extract_directory}")

            # Check if the directory contains a .tex file
            if not any(filename.endswith(".tex") for filename in os.listdir(extract_directory)):
                print(f"Removing directory as it doesn't contain a .tex file: {extract_directory}")
                shutil.rmtree(extract_directory)
                continue  # Skip to the next result if the directory doesn't contain a .tex file
            else:
                print(f"Directory contains a .tex file.")

            metadata_path = os.path.join(extract_directory, 'meta', 'metadata.txt')
            # Create the metadata directory if it doesn't exist
            os.makedirs(os.path.dirname(metadata_path), exist_ok=True)

            # Download pdf to the meta folder using standard slugify
            result.download_pdf(dirpath=os.path.join(extract_directory, 'meta'),
                                filename=standard_slugify(result.title) + ".pdf")
            # Write the metadata to the metadata.txt file with quotes and escaped quotes
            with open(metadata_path, 'w') as metadata_file:
                title_safe = result.title.replace('"', '\\"')
                authors_safe = authors.replace('"', '\\"')

                metadata_file.write(f"title: \"{title_safe}\"\n")
                metadata_file.write(f"title_slug: \"{custom_slugify(result.title, stopwords=['a', 'an', 'the'])}\"\n")
                metadata_file.write(f"license: \"{license_type}\"\n")
                metadata_file.write(f"published: \"{result.published}\"\n")
                metadata_file.write(f"entry_id: \"{result.entry_id}\"\n")
                metadata_file.write(f"author: \"{authors_safe}\"\n")  # Write the authors string
                metadata_file.write(f"pdf: \"{standard_slugify(result.title)}.pdf\"\n")
                metadata_file.write(f"primary_category: \"{result.primary_category}\"\n")
                metadata_file.write(f"journal_ref: \"{result.journal_ref}\"\n")
                metadata_file.write(f"get_short_id: \"{result.get_short_id()}\"\n")
                metadata_file.write(f"cite: \"{result.entry_id}\ [{result.primary_category}]\"\n")
            os.remove(tar_file_path)
            print(f"Removed original tar.gz file: {tar_file_path}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Search arXiv articles.")
    parser.add_argument("query", nargs="?", help="Search query")

    args = parser.parse_args()

    if args.query:
        query = args.query
    else:
        query = input("Enter your search query: ")

    results = search_arxiv(query)

    if results:
        print_results(results)
    else:
        print("No results found.")
