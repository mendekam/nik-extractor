import pytesseract

import numpy as np

import cv2
import os

import matplotlib.pyplot as plt

from PIL import Image

from flask import request
import re


pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

# filename = 'test.jpeg'
# # image.save(os.path.join("uploads", filename))
# # image = cv2.imread(os.path.join("uploads", filename))
# image = cv2.imread(filename)
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# filename_gray = 'gray.jpeg'.format(os.getpid())
# cv2.imwrite(filename_gray, gray)

# image_gray = Image.open(filename_gray)
# imageplot = plt.imshow(image_gray)
# plt.show()

# text = pytesseract.image_to_string(image_gray, lang='ind', config='--psm 6')
# lines = text.split('\n')
# print(lines)


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

        '?': "7",

        'e': "2"

    }


    res = ''

    for letter in word:

        if letter in word_dict:

            res += word_dict[letter]
        else:

            res += letter

    return res


def extract_nik():


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

            plt.imshow(gray)

            text = pytesseract.image_to_string(gray)


            lines = text.split('\n')

            print(lines)

            nik_output = None

            for line in lines:

                word_processed = word_to_number_converter(line)
                if "NIK" in word_processed:
                    nik = re.split("= | : | >", word_processed)
                    match = re.search(r'\d+', nik[1].replace(" ", ""))
                    print(nik[1].strip())

                    if match:
                        nik_output = match.group().strip()
                        print(nik_output)
                        break


            return {
                "nik": nik_output

            }, 200
        
        else:

            return {

                "message": "Something went wrong"

            }, 400
    
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
    
                nip_output = None
                name_output = None
    
                for line in lines:
                    s = line.replace(r'[^\w]', "")
                    text = line.replace(" ", "")
                    print(text)
                    if text.isalpha():
                        name_output = line
                        print(name_output)
                    elif line.isalnum() or line.isnumeric():
                        word_processed = word_to_number_converter(line)
                        nip_output = word_processed.strip()
    
    
                return {
                    "name": name_output,
                    "nip": nip_output
    
                }, 200
            
            else:
    
                return {
    
                    "message": "Something went wrong"
    
                }, 400


