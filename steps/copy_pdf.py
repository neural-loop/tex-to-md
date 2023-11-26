import os
import shutil
import logging


def copy_pdf(input_path, output_path):
    # input_path + /meta/*.pdf
    # output_path + /*.pdf
    # copy all pdfs from input_path to output_path
    pdfs = [f for f in os.listdir(input_path) if f.endswith(".pdf")]
    for pdf in pdfs:
        shutil.copy2(os.path.join(input_path, pdf), output_path)


logging.info("Copied all images")
