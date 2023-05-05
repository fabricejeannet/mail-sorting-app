import cv2
from picamera2 import Picamera2, Preview
import os
import time

class ImageManager:
    
    def __init__(self):
        pass
    
    def open_image(self, path):
        image = cv2.imread(path)
        if image is None:
            raise FileNotFoundError("Image not found at path: " + path)
        return image
    
    def get_concat_h(im1, im2):
        dst = Image.new('RGB', (im1.width + im2.width, im1.height))
        dst.paste(im1, (0, 0))
        dst.paste(im2, (im1.width, 0))
        return dst
    
    def take_and_save_picture(self):
        picam = Picamera2()
        # Démarre la prévisualisation DRM
        picam.start_preview(Preview.QT)

        # Démarre la capture d'image
        picam.start()
        # Attendre 3 secondes
        time.sleep(3)	
     
        picam.capture_file("images/captured_image.jpg")
        picam.stop()
        picam.stop_preview()

    def delete_picture(self, file_name):
        os.remove(file_name)


