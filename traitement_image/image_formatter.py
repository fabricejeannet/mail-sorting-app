import cv2
import numpy as np
from image_analyser import ImageAnalyser

class ImageFormatter:
    def __init__(self):
        self.image_analyser = ImageAnalyser()        
        
    # Niveaux de gris
    def grayscale(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Réduction de bruits
    def remove_noise(self, image):
        return cv2.medianBlur(image,1)
    # Seuillage
    def thresholding(self, image):
        return cv2.threshold(image, 200, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # dilation
    # Purpose: increase the size of the foreground objects
    def dilate(self, image):
        kernel = np.ones((5,5),np.uint8)
        return cv2.dilate(image, kernel, iterations = 1)

    def crop_image(self, image, x, y, w, h):
        return image[y:y+h, x:x+w]
    
    
    def get_image_coordinates(self, image):
        return image.shape[0], image.shape[1]
    
    def crop_image_from_text(self, image, text):
        text_position = self.image_analyser.get_text_position_from_image(image, text)
        height = text_position[3]- text_position[1]
        width = text_position[2] - text_position[0]
        return self.crop_image(image, max(text_position[0]-10,0), max(text_position[1] - 6*height,0), 5*width, round(7.5*height))
        
    # erosion
    # Purpose: decrease the size of the foreground objects
    def erode(self, image):
        kernel = np.ones((5,5),np.uint8)
        return cv2.erode(image, kernel, iterations = 1)

    def get_black_and_white_image(self, image):
        gray = self.grayscale(image)
        thresh = self.thresholding(gray)
        return thresh

    def get_cleaned_black_and_white_image(self, image):
        image = self.remove_noise(image)
        gray = self.grayscale(image)
        thresh = self.thresholding(gray)
        return thresh