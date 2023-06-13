import cv2
import pytesseract
import numpy as np
import logging
from image_processor.image_constants import RECTANGLE_START_POINT, RECTANGLE_END_POINT, RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT
from image_processor.image_constants import RECTANGLE_START_POINT, RECTANGLE_END_POINT

class ImageFormatter:
    
    def __init__(self):
        pass
    
    
    def get_grayscaled_image(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    
    def crop_image(self, image, x, y, width, height):
        return image[y:y+height, x:x+width]
    
    
    def crop_image_with_rectangle_coordinates(self,image):
        width = RECTANGLE_END_POINT[0] - RECTANGLE_START_POINT[0]
        height = RECTANGLE_END_POINT[1] - RECTANGLE_START_POINT[1]        
        return self.crop_image(image, RECTANGLE_START_POINT[0], RECTANGLE_START_POINT[1], width, height)
    
    
    def draw_rectangle_with_coordinates(self,image):
        cv2.rectangle(image, RECTANGLE_START_POINT, RECTANGLE_END_POINT, (0, 255, 0), 2)
        return image
    
    
    def get_noise_removed_image(self, image):
        return cv2.medianBlur(image,1)
    
    
    def get_image_ready_for_text_detection(self, image):
        grayscaled_image = self.get_grayscaled_image(image)
        noise_removed_image = self.get_noise_removed_image(grayscaled_image)
        return self.crop_image_with_rectangle_coordinates(noise_removed_image)
    
    
    def get_image_ready_for_preview_display(self,image):
        self.draw_rectangle_with_coordinates(image)
        return self.resize_image(image)
    
    
    def resize_image(self, image):
        return cv2.resize(image, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))
    

    def add_rectangles_and_text_from_ocr(self,image,x,y,w,h,text):
        cv2.rectangle(image, (x, y), (x + w, y + h), color=(255, 0, 255), thickness=3)
        cv2.putText(img=image, text=text, org=(x, y), fontFace=cv2.FONT_HERSHEY_COMPLEX,
                    fontScale=0.6, color=(0, 0, 255), thickness=1)
        return image