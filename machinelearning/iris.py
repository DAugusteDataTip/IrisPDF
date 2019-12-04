"""Machine Learning Classification script for PDFs"""

import io
import os
import pandas
import sklearn

import pdfminer
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

base_path = 'C:\\Users\\Tay042919\\PycharmProjects\\machinelearning\\TestPDFs\\'

files = os.listdir(base_path)
test_files = [file for file in files if '.pdf' or '.PDF' in file]


def run():
    for test_file in test_files:
        extract_text(base_path + test_file)


def extract_text(pdf_path):
    resource_manager = PDFResourceManager()
    file_handle = io.StringIO()
    converter = TextConverter(resource_manager, file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as pdftext:
        for page in PDFPage.get_pages(pdftext):
            page_interpreter.process_page(page)

        text = file_handle.getvalue()

    converter.close()
    file_handle.close()

    if text:
        print(text)


run()



