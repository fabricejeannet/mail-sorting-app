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
        csv_manager = CsvManager()

        csv_manager.load_dataframe_from_csv_file("clients.csv")
        self.data_analyser = DataAnalyser(csv_manager.get_clients_data_dictionnary())
        
        self.last_movement_time = time.time()
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_preview_configuration(main={"format": 'RGB888', "size": (1280, 720)}))
        self.picam2.start_preview()
        self.picam2.start()
        self.captured_image = self.picam2.capture_array()
        
        
    def has_detected_a_movement(self):   
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


    def main(self):
        image_has_been_analysed = True
        escape_key_pressed = False
        
        while not escape_key_pressed:
            self.captured_image = self.picam2.capture_array()
            
            if (self.has_detected_a_movement()):
                self.last_movement_time = time.time()
                image_has_been_analysed = False
                
            if (self.image_is_steady() and not image_has_been_analysed):
                print("analysing")
                apply_ocr_on_image_thread = threading.Thread(target=self.apply_ocr_on_image)
                apply_ocr_on_image_thread.start()
                image_has_been_analysed = True
                
            self.show_image_preview(self.captured_image)
            escape_key_pressed = cv2.waitKey(30) == 27
            
            
    def show_image_preview(self, captured_image):
        cv2.rectangle(captured_image, RECTANGLE_START_POINT, RECTANGLE_END_POINT, (0, 255, 0))
        captured_image = cv2.resize(captured_image, (600,450))
        cv2.imshow("Camera", captured_image)


    def image_is_steady(self):
        return time.time() - self.last_movement_time > STEADY_WAIT_TIME


    def apply_ocr_on_image(self) :
        self.image_formatter = ImageFormatter()

        black_and_white_image = self.image_formatter.get_cleaned_black_and_white_image(self.captured_image)
        cropped_image = self.image_formatter.crop_image_with_rectangle_coordinates(black_and_white_image,RECTANGLE_START_POINT,RECTANGLE_END_POINT)

        self.text_extractor = TextExtractor()

        cleaned_ocr_results = (self.text_extractor.get_cleaned_ocr_text_from_image(cropped_image))
        for line in cleaned_ocr_results:
            matching_line_results = self.data_analyser.return_the_top_three_matches_for_a_line(line)
            self.data_analyser.display_results(matching_line_results)

                   
street_facteur = StreetFacteur()
street_facteur.main()
