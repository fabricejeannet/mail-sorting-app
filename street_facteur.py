import pytesseract
from pytesseract import Output
from traitement_image.text_extractor import TextExtractor
from traitement_image.image_formatter import ImageFormatter
import cv2
import pandas
from picamera2 import *
import numpy as np

image_formatter = ImageFormatter()
text_extractor = TextExtractor()

#Rectangle overlay variables
rectangle_start_point = (50,50)
rectangle_end_point = (600,400)

picam2 = Picamera2()
preview = picam2.start_preview()
picam2.start()

while True:
    
    im = picam2.capture_array()
    
    #Cleaning picture
    analysed_image = image_formatter.get_cleaned_black_and_white_image(im)

    custom_config = r'--oem 3 --psm 6'

    # Get all OCR output information from pytesseract
    ocr_output_details = pytesseract.image_to_data(analysed_image, output_type = Output.DICT, config=custom_config, lang='fra')
    print(ocr_output_details)
    cv2.rectangle(im, rectangle_start_point, rectangle_end_point, (0, 255, 0))
    im = cv2.resize(im, (600,450))
    cv2.imshow("Camera", im)
    
    if (cv2.waitKey(30) == 27):
            break