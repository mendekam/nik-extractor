import pytesseract

import numpy as np

import cv2
import os

import matplotlib.pyplot as plt

from PIL import Image

from flask import request
import re


pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'


def allowed_image(filename):

    allow = ["JPEG", "JPG", "PNG"]

    if not "." in filename:

        return False


    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in allow:

        return True
    else:

        return False


def word_to_number_converter(word):

    word_dict = {

        "L": "1",

        'l': "1",

        'O': "0",

        'o': "0",

        '?': "7"

    }


    res = ''

    for letter in word:

        if letter in word_dict:

            res += word_dict[letter]
        else:

            res += letter

    return res


def extract_nip():


    if request.method == "POST":

        image = request.files["image"]


        if image.filename == "":

            return {

                "message": "No image"

            }, 400
        

        if not allowed_image(image.filename):

            return {

                "message": "Allowed image extensions are: JPEG, JPG, PNG"

            }, 400
        

        if allowed_image(image.filename):

            filename = image.filename

            image.save(os.path.join("uploads", filename))

            image = cv2.imread(os.path.join("uploads", filename))

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            gray = cv2.medianBlur(gray, 3)


            text = pytesseract.image_to_string(gray)


            lines = text.split('\n')

            print(lines)

            nik = None

            for line in lines:

                word_processed = word_to_number_converter(line)
                if "NIK" in word_processed:
                    nik = re.split("= | :", word_processed)
                    match = re.search(r'\d+', nik[1].replace(" ", ""))
                    print(nik[1].strip())

                    if match:
                        nik_output = match.group().strip()
                        print(nik_output)
                        break

                


            print("NIK:", nik_output)


            return {
                "nik": nik_output

            }, 200
        
        else:

            return {

                "message": "Something went wrong"

            }, 400
    



