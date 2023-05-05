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
        self.analyse_keyword_target = "33000"
        self.image_manager = ImageManager()
        self.image_analyser = ImageAnalyser()
        self.image_formatter = ImageFormatter()
        self.regex_sas = r'\b[sS]?[.]?[aA]?[.]?[sS]?[.]?\b'
        self.regex_sarl = r'\b[sS]?[.]?[aA]?[.]?[rR]?[.]?[lL]?[.]?\b'
        self.regex_sasu = r'\b[sS]?[.]?[aA]?[.]?[sS]?[.]?[uU]?\b'
        self.regex_eurl = r'\b[eE]?[.]?[uU]?[.]?[rR]?[.]?[lL]?\b'
        self.regex_sci = r'\b[sS]?[.]?[cC]?[.]?[iI]?\b'
        self.regex_snc = r'\b[sS]?[.]?[nN]?[.]?[cC]?\b'
        self.regex_ei = r'\b[eE]?[.]?[iI]?\b'
        self.regex_eirl = r'\b[eE]?[.]?[iI]?[.]?[rR]?[.]?[lL]?\b'     
        
        self.banned_words_list = ["33000 bordeaux", "9 rue de conde", "rue de conde","9 rue conde","titulaire du compte", "representant legal", "facture n" , "retour à" ,"destinataire lettre","bureau 3", "destinataire", "numero de tva", "numero de siret", "ecopli", "etage 3", "niveau de garantie", "numero de police", "numero de contrat", "numero de telephone", "numero de fax", "numero de compte", "numero de client", "numero de facture", "numero de commande", "numero de dossier"]
        
    
    def get_cleaned_ocr_text_from_image(self, cropped_image):
        # Converting image to text with pytesseract
        ocr_output = pytesseract.image_to_string(cropped_image, lang='fra')
        ocr_output_lowered = ocr_output.lower()
        cleaned_ocr_output = self.clean_text_output_lines(ocr_output_lowered)
        return (cleaned_ocr_output)
        
        
    def check_if_there_is_a_date_in_text_line(self, line):
        #Return True if there is a date in the line, False otherwise
        return re.search(r"\b(0?[1-9]|[12][0-9]|3[01])[./-](0?[1-9]|1[0-2])[./-](\d{2}|\d{4})\b",line) != None
    
    
    def check_if_there_is_a_braquet_in_text_line(self, line):
        #Return True if there is a braquet in the line
        return re.search(r"\[|\]",line) != None
    
    
    def check_if_the_line_contains_a_sequence_of_numbers(self,line):
        return re.search(r'\d\s*\d\s*\d\s*\d\s*\d\s*\d(?:\s*\d)*', line) != None
       
    
    def line_is_valid(self, line):
        return not self.check_if_there_is_a_braquet_in_text_line(line) and not self.check_if_there_is_a_date_in_text_line(line) and not self.check_if_the_line_contains_a_sequence_of_numbers(line) and not line.isspace() and not len(line) < 2
    
    
    def clean_text_output_lines(self,ocr_output):
        #No need to analyse an output if empty
        if(ocr_output != ""):    
            splitted_ocr_lines = ocr_output.splitlines()
            valid_lines = []
            for line in splitted_ocr_lines:
                if not self.line_contain_a_banned_word(line) and self.line_is_valid(line):
                    line_witouht_legal_status = self.return_the_line_without_legal_status(line)
                    line_witouht_legal_status = line_witouht_legal_status.strip()
                    valid_lines.append(line_witouht_legal_status)
                    if('&' in line_witouht_legal_status):
                        valid_lines.append(self.return_modified_et_lines(line_witouht_legal_status))
        return valid_lines    
    
    
    def line_contain_a_banned_word(self, line):
        banned_word_found = False
        banned_words_index = 0
        while not banned_word_found and banned_words_index < len(self.banned_words_list):
            banned_word_found = max(fuzz.partial_ratio(line,self.banned_words_list[banned_words_index]),fuzz.ratio(line, self.banned_words_list[banned_words_index])) >= 90
            banned_words_index += 1
        return banned_word_found
    
    
    def return_modified_et_lines(self, line):
        return line.replace('&','et')


    def return_the_line_without_legal_status(self, line):
        cleaned_line = re.sub(self.regex_sas, "", line)
        cleaned_line = re.sub(self.regex_sarl, "", cleaned_line)
        cleaned_line = re.sub(self.regex_sasu, "", cleaned_line)
        cleaned_line = re.sub(self.regex_eurl, "", cleaned_line)
        cleaned_line = re.sub(self.regex_sci, "", cleaned_line)
        cleaned_line = re.sub(self.regex_snc, "", cleaned_line)
        cleaned_line = re.sub(self.regex_ei, "", cleaned_line)
        cleaned_line = re.sub(self.regex_eirl, "", cleaned_line)
        return cleaned_line.strip()
        
        