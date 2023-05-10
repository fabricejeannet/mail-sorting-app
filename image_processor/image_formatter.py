import cv2
from pyzbar import pyzbar
from image_processor.image_constants import RECTANGLE_START_POINT, RECTANGLE_END_POINT, RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT

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
    
    
    def remove_qr_codes_and_barcodes_from_image(self, image):
        detected_barcodes = pyzbar.decode(image)
        for barcode in detected_barcodes:
            (x, y, width, height) = barcode.rect
            cv2.rectangle(image, (x, y), (x + width, y + height), (255, 255, 255), -1)
        return image
    
    
    def get_noise_removed_image(self, image):
        return cv2.medianBlur(image,1)
    
    
    def get_image_ready_for_text_detection(self, image):
        grayscaled_image = self.get_grayscaled_image(image)
        noise_removed_image = self.get_noise_removed_image(grayscaled_image)
        qrcodes_less_image = self.remove_qr_codes_and_barcodes_from_image(noise_removed_image)
        return self.crop_image_with_rectangle_coordinates(qrcodes_less_image)
    
    
    def get_image_ready_for_display(self,image):
        self.draw_rectangle_with_coordinates(image)
        resized_image = cv2.resize(image, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))
        return resized_image