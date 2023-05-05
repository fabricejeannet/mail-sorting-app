import cv2
import numpy as np
from pyzbar import pyzbar
from image_analyser import ImageAnalyser

class ImageFormatter:
    def __init__(self):
        self.image_analyser = ImageAnalyser()        
        
    # Niveaux de gris
    def get_grayscaled_image(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    
    # Réduction de bruits
    def get_noise_removed_image(self, image):
        return cv2.medianBlur(image,1)
    
    
    # Seuillage
    def get_thresholded_image(self, image):
        return cv2.threshold(image, 200, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
      

    def crop_image(self, image, x, y, width, height):
        return image[y:y+height, x:x+width]
    
    
    def remove_qrcodes_and_barcode_from_gray_image(self, gray_image):
        detected_barcodes = pyzbar.decode(gray_image)
        for barcode in detected_barcodes:
            (x, y, width, height) = barcode.rect
            cv2.rectangle(gray_image, (x, y), (x + width, y + height), (255, 255, 255), -1)
        return gray_image
    
    
    def crop_image_around_text(self, image, text):
        text_position_coordinates = self.image_analyser.get_text_position_coordinates_from_image(image, text)
        height = text_position_coordinates[3]- text_position_coordinates[1]
        width = text_position_coordinates[2] - text_position_coordinates[0]
        return self.crop_image(image, max(text_position_coordinates[0]-10,0), max(text_position_coordinates[1] - 8*height,0), 6*width, round(9.2*height))
        
        
    def draw_rectangle_around_text(self, image, text):
        text_position_coordinates = self.image_analyser.get_text_position_coordinates_from_image(image, text)
        return cv2.rectangle(image, (text_position_coordinates[0], text_position_coordinates[1]), (text_position_coordinates[2], text_position_coordinates[3]), (0, 255, 0), 2)
        
        
    def crop_image_with_rectangle_coordinates(self, image, rectangle_start_point, rectangle_end_point):
        width = rectangle_end_point[0] - rectangle_start_point[0]
        height = rectangle_end_point[1] - rectangle_start_point[1]
        return self.crop_image(image, rectangle_start_point[0],rectangle_start_point[1], width, height)
    

    def get_black_and_white_image(self, image):
        gray_image = self.get_grayscaled_image(image)
        return self.get_thresholded_image(gray_image)


    def get_cleaned_black_and_white_image(self, image):
        cleaned_image = self.get_noise_removed_image(image)
        gray_image = self.get_grayscaled_image(cleaned_image)
        barcode_less_image = self.remove_qrcodes_and_barcode_from_gray_image(gray_image)
        return barcode_less_image #self.get_thresholded_image(barcode_less_image)
    