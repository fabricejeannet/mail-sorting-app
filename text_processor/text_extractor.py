import pytesseract
from pytesseract import Output
from text_processor.text_cleaner import TextCleaner
from exceptions.custom_exceptions import NoImageGiven, NoTextFoundOnPicture
import logging

class TextExtractor:
    
    
    def __init__(self):
        pass
    
    
    def get_text_from_image(self, cropped_image):
        extracted_text = pytesseract.image_to_string(cropped_image, lang='fra')
        if extracted_text == "" or extracted_text == None:
            raise NoTextFoundOnPicture()
        return extracted_text

        
    def get_cleaned_text_from_image(self, cropped_image):
        extracted_text = self.get_text_from_image(cropped_image).strip()        
        logging.info("Extracted text: " + extracted_text)
        if extracted_text == "" or extracted_text == None:
            raise NoTextFoundOnPicture()
        text_cleaner = TextCleaner()
        text_cleaner.text_to_clean = extracted_text
        return text_cleaner.clean_text()
                