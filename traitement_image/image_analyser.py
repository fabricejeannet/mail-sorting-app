from pytesseract import Output
from traitement_image.line_checker import LineChecker
import pytesseract

class ImageAnalyser:
    def __init__(self):
        self.line_checker = LineChecker()
    
    def get_text_position_from_image(self, image, searched_text):
        text_data = self.get_text_data_from_image(image)
        text = text_data['text']
        left = text_data['left']
        top = text_data['top']
        width = text_data['width']
        height = text_data['height']
        for i in range(len(text)):
            if text[i].lower() == searched_text.lower():
                return (left[i], top[i], left[i] + width[i], top[i] + height[i])
        raise ValueError("Text not found in image")
        
    def get_text_from_image(self, image):
        res = pytesseract.image_to_string(image).lower()
        print(self.get_the_number_of_lines(res))
        return res
    
    def get_text_data_from_image(self, image):
        return pytesseract.image_to_data(image, output_type=Output.DICT)
    
    def check_if_text_is_in_image(self, image, searched_text):
        text = self.get_text_from_image(image)
        if searched_text in text:
            return True
        return False
    
    def get_the_number_of_lines(self, text):
        text = text.splitlines()
        index = text.index("33000 bordeaux")
        print(text)
        last_good_index = index
        for i in range(index,0,-1):
            if not self.line_checker.check_if_line_is_valid(text[i]):
                break
            last_good_index -= 1
        print(index)
        print(last_good_index)
        number_of_lines = index-last_good_index
        return min(number_of_lines,10)
        