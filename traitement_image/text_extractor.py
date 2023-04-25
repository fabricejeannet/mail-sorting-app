import pytesseract
from pytesseract import Output
from image_formatter import ImageFormatter
from image_analyser import ImageAnalyser
from image_manager import ImageManager
from fuzzywuzzy import fuzz
from image_constants import *
import cv2
import re
import time

class TextExtractor:
    
    def __init__(self):
        self.analysed_keyword_target = "33000"
        self.image_manager = ImageManager()
        self.image_analyser = ImageAnalyser()
        self.image_formatter = ImageFormatter()
        
        self.banned_words_list = ["33000 bordeaux", "9 rue de conde", "rue de conde","9 rue conde","titulaire du compte", "bureau 3", "destinataire", "numero de tva", "numero de siret", "ecopli", "etage 3"]
        
    def analyse_image_silently(self,file_name):
        analysed_image = cv2.imread("images/" + file_name + ".jpg")
        analysed_image = self.image_formatter.get_cleaned_black_and_white_image(analysed_image)
        start = time.time()
        analysed_image = self.image_formatter.crop_image_from_text(analysed_image, self.analysed_keyword_target)
        end = time.time()
        print(end-start)
        # Converting image to text with pytesseract
        start = time.time()
        ocr_output = pytesseract.image_to_string(analysed_image, lang='fra')
        end = time.time()
        print(end-start)
        # Print output text from OCR
        return(ocr_output.lower())
    
    
    def get_cleaned_ocr_text_from_image(self, black_and_white_image):
        cropped_image = self.image_formatter.crop_image_from_the_rectangle_coordinates(black_and_white_image,RECTANGLE_START_POINT,RECTANGLE_END_POINT)
        # Converting image to text with pytesseract
        ocr_output = pytesseract.image_to_string(cropped_image, lang='fra')
        ocr_output_lowered = ocr_output.lower()
        cleaned_ocr_output = self.clean_text_output_lines(ocr_output_lowered)
        return (cleaned_ocr_output)
        
        
    def split_text_into_lines_and_remove_empty_ones(self, initial_text):
        return [s for s in initial_text.split('\n') if s.strip() != '']
             
             
    def analyse_image_with_taking_picture(self):
        self.image_manager.take_and_save_picture()
        self.analyse_image("captured_image")
        
        
    def check_if_there_is_a_date_in_text_line(self, line):
        #Return True if there is a date in the line, False otherwise
        return re.search(r"\b(0?[1-9]|[12][0-9]|3[01])[./-](0?[1-9]|1[0-2])[./-](\d{2}|\d{4})\b",line) != None
    
    
    def check_if_there_is_a_braquet_in_text_line(self, line):
        #Return True if there is a braquet in the line
        return re.search(r"\[|\]",line) != None
    
    
    def check_if_the_line_contains_a_sequence_of_numbers(self,line):
        return re.search(r'\d\s*\d\s*\d\s*\d\s*\d\s*\d(?:\s*\d)*', line) != None
    
    def check_if_there_is_empty_line_on_the_top(self, ocr_output):
        #Return True if there is an empty line on the top of the lines
        return ocr_output.splitlines()[0] == ""
    
    def check_if_there_is_empty_line_on_the_bottom(self, ocr_output):
        lines = ocr_output.splitlines()
        #Return True if there is an empty line on the bottom of the lines
        return lines[len(lines)] == ""
    
    def check_if_line_is_valid(self, line):
        return not self.check_if_there_is_a_braquet_in_text_line(line) and not self.check_if_there_is_a_date_in_text_line(line) and not self.check_if_the_line_contains_a_sequence_of_numbers(line)
    
    def clean_text_output_lines(self,ocr_output):
        if(ocr_output != ""):    
            lines = self.split_text_into_lines_and_remove_empty_ones(ocr_output)
            print(lines)
            valid_lines = []
            for line in lines:
                banned_word_found = False
                banned_words_index = 0
                while not banned_word_found and banned_words_index < len(self.banned_words_list):
                    banned_word_found = fuzz.partial_ratio(line,self.banned_words_list[banned_words_index]) > 90
                    banned_words_index += 1
                if not banned_word_found and self.check_if_line_is_valid(line):
                    valid_lines.append([line])
                    if('&' in line):
                        valid_lines.append(self.return_modified_et_lines(line))
        return valid_lines    
    
    def return_modified_et_lines(self, line):
        return line.replace('&','et')

        