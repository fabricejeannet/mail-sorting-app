import cv2
from picamera2 import Picamera2
import numpy as np
from image_processor.image_constants import *
from image_processor.image_formatter import ImageFormatter
from libcamera import Transform
from exceptions.custom_exceptions import CameraIsNotStarted
import threading
import time


class ImageAcquisition:
    
    def __init__(self):
        self.image_formatter = ImageFormatter()
      
        self.is_camera_started = False
        self.last_movement_time = time.time()
        self.last_captured_image = None
        self.last_prepared_image = None
        self.motion_detected = False

        
    def open_image(self, image_path):
        return cv2.imread(image_path)
        
        
    def start_camera(self):
        self.camera = Picamera2()
        self.camera.configure(self.camera.create_preview_configuration(main={"format": 'RGB888', "size": (426, 240)}, transform=Transform(hflip=1,
                                                                                                                                           vflip=1)))
        self.camera.start_preview()
        try :
            self.camera.start()
            self.is_camera_started = True
        except:
            self.is_camera_started = False
        thread_camera = threading.Thread(target=self.video_capture)
        thread_camera.start()  
        image_rgb = cv2.cvtColor(src=self.get_image(), code=cv2.COLOR_BGR2RGB)
        self.last_captured_image = image_rgb
        
        
    def start_movement_detection(self):
            thread_movement_detection = threading.Thread(target=self.motion_detection)
            thread_movement_detection.start()


    def video_capture(self):
        while True:
            image_rgb = cv2.cvtColor(src=self.get_image(), code=cv2.COLOR_BGR2RGB)
            self.last_captured_image = image_rgb
            self.last_prepared_image = self.image_formatter.get_image_ready_for_text_detection(image_rgb)
    

    def get_image(self):
        if not self.is_camera_started:
            raise CameraIsNotStarted()
        return self.camera.capture_array()
    
    
    def image_is_steady(self):
        return time.time() - self.last_movement_time > STEADY_WAIT_TIME        
            
    
    def motion_detection(self):  
        frame_count = 0
        previous_frame = None

        while True:
            frame_count += 1
            self.motion_detected = False

            # 1. Load image; convert to RGB
            image_brg = self.get_image()
            image_rgb = cv2.cvtColor(image_brg, cv2.COLOR_BGR2RGB)

            if ((frame_count % 2) == 0):

                # 2. Prepare image; grayscale and blur
                prepared_frame = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2GRAY)
                prepared_frame = cv2.GaussianBlur(src=prepared_frame, ksize=(5,5), sigmaX=0)
            
                # 3. Set previous frame and continue if there is None
                if (previous_frame is None):
                    # First frame; there is no previous one yet
                    previous_frame = prepared_frame
                    continue
                
                # calculate difference and update previous frame
                diff_frame = cv2.absdiff(src1=previous_frame, src2=prepared_frame)
                previous_frame = prepared_frame

                # 4. Dilute the image a bit to make differences more seeable; more suitable for contour detection
                kernel = np.ones((3, 3))
                diff_frame = cv2.dilate(diff_frame, kernel, 1)

                # 5. Only take different areas that are different enough (>30 / 255)
                thresh_frame = cv2.threshold(src=diff_frame, thresh=20, maxval=255, type=cv2.THRESH_BINARY)[1]

                contours, _ = cv2.findContours(image=thresh_frame, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)

                contours, _ = cv2.findContours(image=thresh_frame, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
                for contour in contours:
                    if cv2.contourArea(contour) < 50:
                        # too small: skip!
                        continue
                    self.last_movement_time = time.time()
                    self.motion_detected = True
            