from pytesseract import Output
import pytesseract

class ImageAnalyser:
    def __init__(self):
        pass
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
        return pytesseract.image_to_string(image, output_type=Output.DICT)
    
    def get_text_data_from_image(self, image):
        return pytesseract.image_to_data(image, output_type=Output.DICT)
    
    def check_if_text_is_in_image(self, image, searched_text):
        text = self.get_text_from_image(image)
        if searched_text in text:
            return True
        return False