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
    
    def take_and_save_picture(self):
        picam = Picamera2()
        # Démarre la prévisualisation DRM
        picam.start_preview(Preview.QT)

        # Démarre la capture d'image
        picam.start()
        # Attendre jusqu'à l'appui d'une touche
        #input("Waiting..")
        time.sleep(3)	
     
        picam.capture_file("images/captured_image.jpg")
        picam.stop()
        picam.stop_preview()

    def delete_picture(self, file_name):
        os.remove(file_name)


