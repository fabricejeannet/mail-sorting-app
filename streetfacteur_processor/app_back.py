import traceback
import cv2
import threading
import time
import numpy as np
import logging
import pytesseract
from text_processor.text_cleaner import TextCleaner
from match_processor.match_analyser import MatchAnalyser
from csv_processor.csv_manager import CsvManager
from csv_processor.csv_constants import *
from config_processor.config_importer import ConfigImporter
from exceptions.custom_exceptions import *
from image_processor.image_formatter import ImageFormatter
from image_processor.image_acquisition import ImageAcquisition
from image_processor.image_constants import *


class AppBack:
    
    def __init__(self, app_gui):
        self.app_gui = app_gui
        self.config_importer = ConfigImporter()
        self.csv_manager = CsvManager()
        self.image_formatter = ImageFormatter()
        self.text_cleaner = TextCleaner()
        self.matching_results = []
        self.movement_detected = False
        self.text_found = False
        self.last_captured_image = None
        self.last_prepared_image = None
     
        self.init_csv(False)
        
    
    def init_csv(self, show_popup=True):
        if show_popup:
            self.app_gui.popup_message()
        time.sleep(5)
        csv_file_name = self.csv_manager.get_latest_csv_file()
        self.csv_manager.open_csv_file(csv_file_name)
        logging.info("Loaded csv file : " + csv_file_name)
        logging.info("Csv file columns : " + str(self.csv_manager.dataframe.columns))
        logging.info("Csv file number of rows : " + str(self.csv_manager.dataframe.shape[0]))
        clients_data_dictionary = self.csv_manager.get_clients_data_dictionnary()
        self.match_analyser = MatchAnalyser(clients_data_dictionary)

    # All the following methods are camera related methods 
    
    def start_camera(self):
        self.image_acquisition = ImageAcquisition()
        self.image_acquisition.start_camera()
        self.last_movement_time = time.time()
        image_rgb = cv2.cvtColor(src=self.image_acquisition.get_image(), code=cv2.COLOR_BGR2RGB)
        self.last_captured_image = image_rgb
        thread_camera = threading.Thread(target=self.video_capture)
        thread_camera.start()    
    
    
    def video_capture(self):
        while True:
            image_rgb = cv2.cvtColor(src=self.image_acquisition.get_image(), code=cv2.COLOR_BGR2RGB)
            self.last_captured_image = image_rgb
            self.last_prepared_image = self.image_formatter.get_image_ready_for_text_detection(image_rgb)
    
    
    def movement_detection(self):  
        frame_count = 0
        previous_frame = None

        while True:
            frame_count += 1
            self.movement_detected = False

            # 1. Load image; convert to RGB
            image_brg = self.image_acquisition.get_image()
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
                    self.movement_detected = True
            
    
    def image_is_steady(self):
        return time.time() - self.last_movement_time > STEADY_WAIT_TIME        
              
              
    def start_movement_detection(self):
        thread_movement_detection = threading.Thread(target=self.movement_detection)
        thread_movement_detection.start()
        
    #All the following methods are related to the gui        
            
    def display_match_result_on_tkinter_widgets(self):
        self.app_gui.show_analysed_lines(self.analysed_lines)
        self.app_gui.remove_text_from_result_widget()
        if not self.text_found:
            self.app_gui.show_no_text_found_display()
            return
        if not self.client_match_found():
            self.app_gui.show_no_match_found_display()
            return
        for result in self.matching_results:
            self.app_gui.insert_a_match_in_txt_result_widget(result.matching_string, result.status, result.match_ratio)
            self.app_gui.insert_a_separator_in_matching_text_widget()
    

    def select_the_good_image_for_help_widget(self):
        if self.client_match_found():
            all_the_results_are_subscribed = True
            all_the_results_are_unsubscribed = True
            index = 0
            while (all_the_results_are_subscribed or all_the_results_are_unsubscribed) and index < len(self.matching_results):
                if(self.matching_results[index].status == SUBSCRIBED):
                    all_the_results_are_unsubscribed = False
                if(self.matching_results[index].status == UNSUBSCRIBED):
                    all_the_results_are_subscribed = False
                index += 1
        
            if(all_the_results_are_subscribed and self.first_result_have_valid_match_ratio()):
                return "valid"
            if(all_the_results_are_unsubscribed or not self.first_result_have_minimum_match_ratio()):
                return "invalid"
            else:
                return "warning"
        else:
            logging.info("No matching results")
            return "invalid"
                
                
    def change_the_help_widget_image(self, image_name):
        if (image_name == "warning"):
            self.app_gui.show_warning_display()
        elif (image_name == "valid"):
            self.app_gui.show_valid_display()
        elif (image_name == "invalid"):
            self.app_gui.show_invalid_display()
            
    # All the following methods are related to the ocr and the match analyser

    def client_match_found(self):
        if(self.matching_results != [] and len(self.matching_results) > 0):
            return True
        return False
    
                
    def first_result_have_valid_match_ratio(self):
        if(self.matching_results):
            if(self.get_first_result().match_ratio >= self.config_importer.get_image_valid_threshold()):
                return True
        return False
    
    
    def first_result_have_minimum_match_ratio(self):
        if(self.matching_results):
            if(self.get_first_result().match_ratio >= self.config_importer.get_image_minimum_threshold()):
                return True
        return False
            
        
    def reset_ocr_results(self):
        self.matching_results = []
        self.analysed_lines = []


    def get_first_result(self):
        return self.matching_results[0]
    
    
    def add_matching_results_from_cleaned_ocr_lines(self, cleaned_ocr_text):
        logging.info("Total cleaned ocr text : " + str(cleaned_ocr_text))
        self.analysed_lines = cleaned_ocr_text

        # List the created threads
        threads = []

        for line in cleaned_ocr_text:
            thread_line_matching = threading.Thread(target=self.add_matching_result_for_a_line, args=(line,))
            thread_line_matching.start()
            threads.append(thread_line_matching)  # Add the thread to the list

        # Wait for all threads to complete
        for thread in threads:
            thread.join()
                
                
    def add_matching_result_for_a_line(self, line):
        matching_line_results = self.match_analyser.return_the_top_three_matches_for_a_line(line)
        for element in matching_line_results:
            logging.info("element : " + str(element))
            self.matching_results.append(element)
            
    def reorder_results_to_show_the_most_corresponding_result_first(self):
        if(self.matching_results != []):
            self.matching_results.sort(key=lambda x: x.match_ratio, reverse=True)


    def check_if_the_first_result_is_a_perfect_match(self):
        if(self.matching_results):
            if(self.get_first_result().match_ratio == 100):
                return True
        return False
            
            
    def apply_ocr_on_image(self, prepared_image, captured_image):
        df = pytesseract.image_to_data(prepared_image, lang="fra", output_type=pytesseract.Output.DATAFRAME)
        cleaned_ocr_text = []
        for line_num, words_per_line in df.groupby(["block_num", "par_num", "line_num"]):
            # filter out words with a low confidence
            words_per_line = words_per_line[words_per_line["conf"] >= 5]
            if not len(words_per_line):
                continue

            words = words_per_line["text"].values
            line = " ".join(words)
            logging.info("Readed Line: " + line)
            cleaned_line = self.text_cleaner.clean_text(line)
            
            if cleaned_line != "":
                self.text_found = True
                logging.info("Found a line which is valid : " + cleaned_line)
                word_boxes = []
                
                for left, top, width, height in words_per_line[["left", "top", "width", "height"]].values:
                    word_boxes.append((left, top))
                    word_boxes.append((left + width, top + height))

                x, y, w, h = cv2.boundingRect(np.array(word_boxes))
                x = x + RECTANGLE_START_POINT[0]
                y = y + RECTANGLE_START_POINT[1]
                cv2.rectangle(captured_image, (x, y), (x + w, y + h), color=(255, 0, 255), thickness=3)
                cv2.putText(img=captured_image, text=cleaned_line, org=(x, y), fontFace=cv2.FONT_HERSHEY_COMPLEX,
                            fontScale=1, color=(0, 0, 255), thickness=2)
                cleaned_ocr_text.append(cleaned_line)
        self.add_matching_results_from_cleaned_ocr_lines(cleaned_ocr_text)

        return captured_image


    def main(self):
        self.start_camera()
        self.start_movement_detection()

        image_has_been_analysed = True

        # Show the first image
        final_image = self.image_formatter.get_image_ready_for_preview_display(self.last_captured_image)
        self.app_gui.update_the_camera_preview_with_last_image(final_image)

        # Start a loop to continuously update the displayed image
        while True:
            self.reset_ocr_results()
            
            if not image_has_been_analysed:
                final_image = self.image_formatter.get_image_ready_for_preview_display(self.last_captured_image)
                self.app_gui.update_the_camera_preview_with_last_image(final_image)

            if self.movement_detected:
                logging.info("Mouvement détecté !")
                image_has_been_analysed = False
                self.text_found = False
                self.app_gui.show_movement_detected_display()

            if self.image_is_steady() and not image_has_been_analysed:
                self.app_gui.show_waiting_display()
                self.app_gui.update_window()
                logging.info("Analyse !")
                try:
                    modified_image = self.apply_ocr_on_image(self.last_prepared_image, self.last_captured_image)
                    self.reorder_results_to_show_the_most_corresponding_result_first()
                    widget_image_name = self.select_the_good_image_for_help_widget()
                    self.change_the_help_widget_image(widget_image_name)
                    self.display_match_result_on_tkinter_widgets()
                    resized_modified_image = self.image_formatter.resize_image(modified_image)
                    self.app_gui.update_the_camera_preview_with_last_image(resized_modified_image)
                    image_has_been_analysed = True
                except:
                    logging.info("Erreur lors de l'analyse !")
                    logging.error("Unexpected error:" + str(traceback.format_exc()))
                    logging.info("Image has been analysed = " + str(image_has_been_analysed))

            # Update the window to show the new image
            self.app_gui.update_window()
