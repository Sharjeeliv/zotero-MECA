# This file is used to tests the other functionalities
# It will be replaced with a gui controller
from src.utils import search_pdfs, move_pdf
from src.text_extraction import text_extract, ocr_extract
from src.data_verification import get_crossref_work
from zotero_entry import create_zotero_entry
from params import general

import time
import concurrent.futures
import sys


def extract_doi_from_pdf(pdf):
    doi = text_extract(pdf)
    return ocr_extract(pdf) if not doi else doi, pdf


def doi_extraction(pdfs):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(extract_doi_from_pdf, pdfs)
        return results


def filter_extractions(pdf_data):
    doi, pdf_path = pdf_data
    if doi is not None: return True
    #move_pdf(pdf_path)
    print("\nINVALID AT FILTER\n")
    return False


def api(files: list):
    start = time.time()
    pdfs_data = filter(lambda result: filter_extractions(result), doi_extraction(files))
    pdfs_metadata = [get_crossref_work(pdf_data) for pdf_data in pdfs_data]  # Iterator object
    [create_zotero_entry(pdf_metadata) for pdf_metadata in pdfs_metadata]
    end = time.time()
    print(f"Time to complete: {round(end - start, 2)}s")



def app():
    # Dynamic way to input all credentials and then store them, CR key, Zotero address, pdf path, tesseract path
    # input_path = sys.argv[1]
    # print(input_path)

    start = time.time()
    pdfs = search_pdfs(
        '/Users/sharjeelmustafa/Documents/02 Work/01 Research/Y2-2022-W/Articles/00 - TEAMS/0 - 0 Team (Multilevel) Foundation _ Reviews')
    pdfs_data = filter(lambda result: filter_extractions(result), doi_extraction(pdfs))
    pdfs_metadata = [get_crossref_work(pdf_data) for pdf_data in pdfs_data]  # Iterator object
    [create_zotero_entry(pdf_metadata) for pdf_metadata in pdfs_metadata]
    end = time.time()
    print(f"Time to complete: {round(end - start, 2)}s")


if __name__ == '__main__':
    app()
