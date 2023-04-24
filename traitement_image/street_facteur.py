import pytesseract
from pytesseract import Output
from text_extractor import TextExtractor
from image_formatter import ImageFormatter
from image_constants import *
from libcamera import controls
from data_analyser import DataAnalyser
import cv2
import pandas
from picamera2 import *
import numpy as np
import time
import threading


class StreetFacteur :
    
    def __init__(self):        
        self.image_formatter = ImageFormatter()
        self.text_extractor = TextExtractor()
        self.data_analyser = DataAnalyser()
        self.last_image_time = time.time()
        self.last_mouvement_time = time.time()
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_preview_configuration(main={"format": 'RGB888', "size": (1280, 720)}))
        self.picam2.start_preview()
        self.picam2.start()
        
        
    def is_there_movement_on_frame(self):   
        frame_count = 0
        previous_frame = None
        
        while True:
            frame_count += 1

            # 1. Load image; convert to RGB
            img_brg = self.picam2.capture_array()
            img_rgb = cv2.cvtColor(src=img_brg, code=cv2.COLOR_BGR2RGB)

            if ((frame_count % 2) == 0):

                # 2. Prepare image; grayscale and blur
                prepared_frame = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
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
                kernel = np.ones((5, 5))
                diff_frame = cv2.dilate(diff_frame, kernel, 1)

                # 5. Only take different areas that are different enough (>20 / 255)
                thresh_frame = cv2.threshold(src=diff_frame, thresh=20, maxval=255, type=cv2.THRESH_BINARY)[1]

                contours, _ = cv2.findContours(image=thresh_frame, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)

                contours, _ = cv2.findContours(image=thresh_frame, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
                for contour in contours:
                    if cv2.contourArea(contour) < 50:
                        # too small: skip!
                        continue
                    return True
                return False
        



    def show_camera_preview_detect_movement_and_analyse_text(self):
        analysed = True
        while True:
            im = self.picam2.capture_array()
            has_moved = self.is_there_movement_on_frame()
            if (has_moved):
                self.last_mouvement_time = time.time()
                analysed = False
            if (time.time() - self.last_mouvement_time > 2 and not analysed):
                analysed = True
                print("analysing")
                t2 = threading.Thread(target=self.analyse_text)
                t2.start()
            cv2.rectangle(im, RECTANGLE_START_POINT, RECTANGLE_END_POINT, (0, 255, 0))
            im = cv2.resize(im, (600,450))
            cv2.imshow("Camera", im)
            if (cv2.waitKey(30) == 27):
                break

    def analyse_text(self) :
        im = self.picam2.capture_array()
        self.last_image_time = time.time()
        analysed_image = self.image_formatter.get_cleaned_black_and_white_image(im)
        # Get all OCR output information from pytesseract
        ocr_results = (self.text_extractor.analyse_image_without_preview_with_image(analysed_image))
        for line in ocr_results:
            print(self.data_analyser.print_top_n_matches_with_process(line, 3))


    def press_space_bar_2_seconds_then_scan(self):
        print("launched")
        im = self.picam2.capture_array()
        im = cv2.resize(im, (600,450))
        cv2.imshow("Camera", im)
        while True :
            k = cv2.waitKey(0)
            print("waiting for key space")
            if ( k == -1):
                continue
            else : print(k)
            if (k == 32): 
                self.last_image_time = time.time()
                analysed = False
                while True:
                    im = self.picam2.capture_array()
                    print(time.time() - self.last_image_time)
                    if (time.time() - self.last_image_time > 5 and not analysed):
                        t2 = threading.Thread(target=self.analyse_text)
                        t2.start()
                        analysed = True
                    cv2.rectangle(im, RECTANGLE_START_POINT, RECTANGLE_END_POINT, (0, 255, 0))
                    im = cv2.resize(im, (600,450))
                    cv2.imshow("Camera", im)
                    if (cv2.waitKey(30) == 27 or time.time() - self.last_image_time > 5.1):
                        break
            elif (k == 27):
                print("in escape")
                break
        cv2.destroyAllWindows()
                   
street_facteur = StreetFacteur()
# street_facteur.press_space_bar_2_seconds_then_scan()
street_facteur.show_camera_preview_detect_movement_and_analyse_text()