import os
import re
import pytesseract
import PyPDF2
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = '/usr/local/Cellar/tesseract/5.0.1/bin/tesseract'
regex = r"(10.\d{4,9}\/[-._;()\/:A-Z0-9]+|\/^10.1002\/[^\s]+$\/i)"
clean = re.compile(r"(20\d\d|[.a-z])+$", re.IGNORECASE | re.MULTILINE)


def text_extract(pdf_name):
    _, file_name = os.path.split(pdf_name)
    # print(f"\033[1;36mTXT \033[1;34m{file_name}\033[0;0m")  # For logging print name

    with open(pdf_name, "rb") as file:
        reader = PyPDF2.PdfFileReader(file, strict=False)

        try:
            first_page = reader.getPage(0)
            text = first_page.extractText()
        except Exception:
            text = ""

        return get_doi(str(text))


def clean_doi(doi):
    # print(re.search(clean, doi))
    return re.sub(clean, '', doi)


def get_doi(text):
    matches = re.search(regex, text, re.IGNORECASE | re.MULTILINE)

    if matches is None:
        # print(f"\033[1;31mNo regex match, text dump:\033[0;0m\n")
        return False

    doi = clean_doi(matches.group(0))
    # print(f"\033[1;32mRegex matches, DOI found:\033[0;0m {doi}\n")
    return doi


def ocr_extract(pdf_name):
    pdf_file = convert_from_path(pdf_name)
    # print(f"\033[1;35mOCR \033[1;34m{file_name}\033[0;0m")  # For logging print name

    page_data = pdf_file[0]
    text = pytesseract.image_to_string(page_data)
    text = re.sub("\n-", "", text)
    doi = get_doi(text)
    return doi