import cv2
from picamera2 import Picamera2, Preview
from exceptions.custom_exceptions import CameraIsNotStarted
import os
import time


class ImageAcquisition:
    
    def __init__(self):
        self.camera = Picamera2()
        self.camera.configure(self.camera.create_preview_configuration(main={"format": 'RGB888', "size": (1280, 720)}))
        self.is_camera_started = False
        
        
    def open_image(self, path):
        image = cv2.imread(path)
        if image is None:
            raise FileNotFoundError("Image not found at path: " + path)
        return image
        
        
    def start_camera(self):
        self.camera.start_preview()
        self.camera.start()
        self.is_camera_started = True


    def get_image(self):
        if not self.is_camera_started:
            raise CameraIsNotStarted()
        return self.camera.capture_array()