import logging

import arxiv
import argparse

logging.basicConfig(level=logging.DEBUG)

def search_arxiv(query):
    client = arxiv.Client()
    search = arxiv.Search(query=query, max_results=5, sort_by=arxiv.SortCriterion.SubmittedDate)
    return list(client.results(search))

def write_abstracts_to_file(results, filename='result.txt'):
    with open(filename, 'w', encoding='utf-8') as file:
        for idx, result in enumerate(results, start=1):
            file.write(f"\nPaper {idx}:\n")
            file.write(f"Title: {result.title}\n")
            file.write(f"Authors: {', '.join(author.name for author in result.authors)}\n")
            file.write(f"Published: {result.published}\n")
            file.write(f"Abstract:\n{result.summary}\n\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search arXiv articles.")
    parser.add_argument("query", nargs="?", help="Search query")

    args = parser.parse_args()

    if args.query:
        query = args.query
    else:
        query = input("Enter your search query: ")

    results = search_arxiv(query)

    if results:
        write_abstracts_to_file(results)
        print("Results written to 'result.txt'.")
    else:
        print("No results found.")
