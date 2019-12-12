# -*- coding: utf-8 -*-
# PDFMiner is a text extraction tool for PDF documents.
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer

# openpyxl is a Python library to read/write Excel files.
# progressbar is a text progress bar library for Python.
# A text progress bar is typically used to display the progress of a long-running operation, providing a visual cue that processing is underway.
from openpyxl import Workbook
from progress.bar import Bar

import os
import time

# get the current working directory and pathnames
BASE_PATH = os.getcwd()
BASE_INPUT_PATH = os.path.join(BASE_PATH, 'input_files')
BASE_OUTPUT_PATH = os.path.join(BASE_PATH, 'output_files')

# With this code, we will parse each PDF file in the folder 'input_files', looking for certain features within the PDF file
# One feature is the Provider name, such as 'ADP' or 'Paychex'
# Other features are extracted from the layout details
# The footer text is extracted and saved as a string
# The field labels are examined.  We are making a binary classification of Y (yes) or N (no) for the 'mailing' combination and the 'telephone' combination.
# If the field labels 'Mailing Address' or 'SSN' are found, the 'mailing' combination will be tagged 'Y', else 'N'.
# If the field labels 'Telephone' or 'DOB' are found, the 'telephone' combination will be tagged 'Y', else 'N'.
# We output our findings into an Excel spreadsheet in the 'output_files' folder


# parse the object
def parse_obj(lt_objs, filename):
    # loop over the object list
    current_entry = [filename]  
    # initialize the feature variables
    footer = False
    mailing = False
    telephone = False 
    footer_text = ""
    
    for ind, obj in enumerate(lt_objs):
        # if it's a textbox, print text and location
        if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
            text = obj.get_text()
            if footer:
                if not any(word in text for word in ['Mailing Address', 
                    'mailing address', 'ssn', 'SSN', 'Telephone', 
                    'telephone', 'DOB', 'dob']):
                    footer_text += text.strip('\n')
                    # bit of a hack, but Provider name is the first word of the first >50-char string
                    # so we parse that off and put it into the Provider field.  May need to revisit this with more data samples.
            elif len(text)>50:
                current_entry.append(text.split()[0])
                if any(word in text for word in ['Mailing Address', 
                    'mailing address', 'ssn', 'SSN']):
                    mailing = True
                if any(word in text for word in ['Telephone', 
                    'telephone', 'DOB', 'dob']):
                    telephone = True
                footer = True


    current_entry.append(footer_text)
    if mailing:
        current_entry.append('Y')
    else:
        current_entry.append('N')
    if telephone:
        current_entry.append('Y')
    else:
        current_entry.append('N')

    #Append the row to the excel sheet
    ws.append(current_entry)
    
if __name__ == "__main__":
    print('Processing PDF files...')

# main function begins here
# setup the Excel spreadsheet to output the feature information for each PDF file
    wb = Workbook()
    # get the active worksheet in the workbook
    ws = wb.active
    ws.append(['Original Filename','Provider', 'Footer Text', 
        'Layout has Mailing Address and SSN field labels', 
        'Layout has Telephone and DOB field labels'])


    # review each file in the input folder/directory, but only if has the PDF suffix
    all_files = os.listdir(BASE_INPUT_PATH)
    with Bar('Processing', max=len(all_files)) as bar:
        for file in all_files:
            if not file.endswith('.pdf'):
                #if the file is not a PDF, move on to the next file.
                bar.next()
                continue
            absolute_file_path = os.path.join(BASE_INPUT_PATH, file)
            # 'rb' will read the file in binary
            fp = open(absolute_file_path, 'rb')

            # Create a PDF parser object associated with the file object.
            parser = PDFParser(fp)

            # Create a PDF document object that stores the document structure.
            document = PDFDocument(parser)

            # If the document does not allow text extraction, raise the flag.
            if not document.is_extractable:
                raise PDFTextExtractionNotAllowed

            # Create a PDF resource manager object [rsrcmgr] that stores shared resources.
            rsrcmgr = PDFResourceManager()

            # BEGIN LAYOUT ANALYSIS
            # Set parameters for layout analysis [laparams].
            laparams = LAParams()

            # Create a PDF page aggregator object.
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)

            # Create a PDF interpreter object.
            interpreter = PDFPageInterpreter(rsrcmgr, device)

            for index, page in enumerate(PDFPage.create_pages(document)):
                # read the page into a layout object
                interpreter.process_page(page)
                layout = device.get_result()

                # extract text from this object
                parse_obj(layout._objs, file)
            # remember to close the file 
            fp.close()
            bar.next()
    # debugging / status
    print('Writing the excel file...')
    
    # Create output directory if it doesn't already exist
    if not os.path.exists(BASE_OUTPUT_PATH):
        os.makedirs(BASE_OUTPUT_PATH)
    timestr = time.strftime("%Y%m%d-%H%M%S")

    output_filename = os.path.join(BASE_OUTPUT_PATH, timestr + '.xlsx')
    wb.save(output_filename)








