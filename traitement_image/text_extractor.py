import pytesseract
from pytesseract import Output
from image_formatter import ImageFormatter
from image_manager import ImageManager
from image_analyser import ImageAnalyser
import cv2
import time
import picamera2

class TextExtractor:
    
    def __init__(self):
        self.image_manager = ImageManager()
        self.image_analyser = ImageAnalyser()
        self.image_formatter = ImageFormatter()
        
    def analyse_image(self, file_name):
        
        analysed_image = cv2.imread("images/" + file_name + ".jpg")
        result_image = analysed_image.copy()
        analysed_image = self.image_formatter.get_cleaned_black_and_white_image(analysed_image)
        analysed_image = self.image_formatter.crop_image_from_text_and_margin(analysed_image, "Bordeaux", 300)

        custom_config = r'--oem 3 --psm 6'

        # Get all OCR output information from pytesseract
        ocr_output_details = pytesseract.image_to_data(analysed_image, output_type = Output.DICT, lang='fra')
        # Total bounding boxes
        n_boxes = len(ocr_output_details['level'])
        
        
        # Converting image to text with pytesseract
        ocr_output = pytesseract.image_to_string(analysed_image)
        # Print output text from OCR
        print(ocr_output)
        # Print the full first line of the OCR output
        #print(ocr_output.splitlines()[2])
            
        # Extract and draw rectangles for all bounding boxes
        for i in range(n_boxes):
            if ocr_output_details['text'][i] != '' and ocr_output_details['conf'][i] > 50:
                (x, y, w, h) = (ocr_output_details['left'][i], ocr_output_details['top'][i], ocr_output_details['width'][i], ocr_output_details['height'][i])
                cv2.rectangle(analysed_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Print OCR Output kesys
        print(ocr_output_details.keys())
        
        # Show output image with bounding boxes
        cv2.imshow('Image', analysed_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def analyse_image_silently(self,file_name):
        analysed_image = cv2.imread("images/" + file_name + ".jpg")
        analysed_image = self.image_formatter.get_cleaned_black_and_white_image(analysed_image)
        analysed_image = self.image_formatter.crop_image_from_text_and_margin(analysed_image, "Bordeaux", 300)
        
        # Converting image to text with pytesseract
        ocr_output = pytesseract.image_to_string(analysed_image, lang='fra')
        # Print output text from OCR
        return(ocr_output.lower())
             
    def analyse_image_with_taking_picture(self):
        self.image_manager.take_and_save_picture()
        self.analyse_image("captured_image")
            
    def get_company_name_from_text_output():
        