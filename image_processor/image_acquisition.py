import cv2
from picamera2 import Picamera2, Preview
import os
import time

class ImageAcquisition:
    
    def __init__(self, camera):
        self.camera = camera


    def get_image(self):
        return self.camera.get_image()