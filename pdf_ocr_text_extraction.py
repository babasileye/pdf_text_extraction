
'''
these function are developped by sileye.ba@outlook.com  to extract txt
from pdf files they might be use/copied without restriction. No warranty is
given about the way they function. Users are fully responsible of their usage.
'''

import logging
from PIL import Image as pil_image
from pytesseract import image_to_string
from pdf2image import convert_from_path

from os import listdir
from os.path import isfile, join


def text_from_pdf_file(pdf_file,resolution=100):

    logging.info("extracting text from page {}".format(pdf_file))

    pdf_pages = convert_from_path(pdf_file, resolution)
    number_of_pages = len(pdf_pages)

    document = []
    counter=1
    image_file="page.jpg"
    for page in pdf_pages:
        logging.info("extracting page {}/{} as text".format(counter, number_of_pages))
        page.save(image_file, 'JPEG')
        text = image_to_string(pil_image.open(image_file))
        document.append(text)
        counter+=1

    return document


def pdf_to_txt_file(pdf_dir,pdf_file,txt_dir="",txt_file=None,resolution=100):

    document = text_from_pdf_file(join(pdf_dir, pdf_file))

    if txt_file==None:
        txt_file = pdf_file.replace(".pdf",".txt")

    file = open(join(txt_dir,txt_file), "w+")

    for page in document:
        file.write(page)
        file.write("\n")
    file.close()


def convert_pdf_list(pdf_dir,txt_dir, resolution=100):

    pdf_file_names = [f for f in listdir(pdf_dir) if isfile(join(pdf_dir, f))].sort()
    number_of_files = len(pdf_file_names)
    counter = 1

    for pdf_file in pdf_file_names:

        logging.info("Processing file {}/{}:  {}".format(counter,number_of_files,pdf_file))

        try:

            txt_file = pdf_to_txt_file(pdf_dir=pdf_dir,pdf_file=pdf_file,txt_dir=txt_dir, resolution=resolution)

            logging.info("Created txt file: {}".forma(txt_file))

        except Exception as e:

            logging.info("Exception occurred {}".format(e))

        counter+=1


if __name__ == '__main__':

    import argparse


    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--pdf_dir", help="pdf files folder e.g. path/to/pdf/files/", type=str)
    parser.add_argument("-o", "--txt_dir", help="txt files folder e.g. path/to/txt/files/", type=str)
    parser.add_argument("-r", "--resolution", help="image resolution", type=int,default=100)
    args = parser.parse_args()

    pdf_dir = args.pdf_dir
    txt_dir = args.txt_dir
    resolution=arg.resolution

    convert_pdfs_to_txts(pdf_dir,txt_dir,resolution)
    
