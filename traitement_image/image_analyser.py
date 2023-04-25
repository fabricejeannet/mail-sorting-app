from pytesseract import Output
from custom_exceptions import NoTextFoundOnPicture
import pytesseract

class ImageAnalyser:
    
    def __init__(self):
        pass
    
    
    def get_text_position_from_image(self, image, searched_text):
        text_data_of_image = self.get_text_data_from_image(image)
        text = text_data_of_image['text']
        left_point_of_text = text_data_of_image['left']
        top_point_of_text = text_data_of_image['top']
        width_of_text = text_data_of_image['width']
        height_of_text = text_data_of_image['height']
        for index in range(len(text)):
            if text[index].lower() == searched_text.lower():
                return (left_point_of_text[i], top_point_of_text[i], left_point_of_text[i] + width_of_text[i], top_point_of_text[i] + height_of_text[i])
        raise NoTextFoundOnPicture()
        
        
    def get_text_from_image(self, image):
        return pytesseract.image_to_string(image).lower()
    
    
    def get_text_data_from_image(self, image):
        return pytesseract.image_to_data(image, output_type=Output.DICT)
    
    
    def check_if_text_is_in_image(self, image, searched_text):
        image_text = self.get_text_from_image(image)
        if searched_text in image_text:
            return True
        return False
           