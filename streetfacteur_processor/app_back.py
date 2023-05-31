import traceback
import cv2
import threading
import time
import numpy as np
import logging
import pytesseract
from streetfacteur_processor.app_constants import *
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
        self.image_acquisition = ImageAcquisition()
        self.image_formatter = ImageFormatter()
        self.text_cleaner = TextCleaner()
        self.matching_results = []
        self.valid_lines_found = False
        self.show_csv_popup = False
        
        self.init_csv()
        
    
    def init_csv(self):
        
        try :
            self.show_csv_popup = PopupStatus.CSV_POPUP
            time.sleep(5)
            csv_file_name = self.csv_manager.get_latest_csv_file()
            self.csv_manager.open_csv_file(csv_file_name)
            
            logging.info("Loaded csv file : " + csv_file_name)
            logging.info("Csv file columns : " + str(self.csv_manager.dataframe.columns))
            logging.info("Csv file number of rows : " + str(self.csv_manager.dataframe.shape[0]))
            
            clients_data_dictionary = self.csv_manager.get_clients_data_dictionnary()
            self.match_analyser = MatchAnalyser(clients_data_dictionary)

        except NoCsvFileFound:
            self.show_csv_popup = PopupStatus.NO_CSV_FILE_POPUP
            self.match_analyser = MatchAnalyser({})
            logging.error("No csv file found")
        
        except FileNotFoundError:
            self.init_csv()
            
        
    def show_correct_display_depending_on_results(self):
        self.app_gui.clear_result_widget()
        
        if self.valid_lines_found:
            if self.client_match_found():
                for client_match_result in self.matching_results:
                    self.app_gui.insert_a_match_in_txt_result_widget(client_match_result.matching_string, client_match_result.status, client_match_result.match_ratio)
                    self.app_gui.insert_a_separator_in_matching_text_widget()
            else :
                self.app_gui.show_no_match_found_display()
        else :
            self.app_gui.show_no_text_found_display()
            

    def get_display_status(self):
        
        if self.client_match_found():
            
            all_the_results_are_subscribed = True
            all_the_results_are_unsubscribed = True
            index = 0
            
            while (all_the_results_are_subscribed or all_the_results_are_unsubscribed) and index < len(self.matching_results):
                if(self.matching_results[index].status == SUBSCRIBED):
                    all_the_results_are_unsubscribed = False
                else:
                    all_the_results_are_subscribed = False
                index += 1
        
            if(all_the_results_are_subscribed and self.first_result_have_valid_match_ratio()):
                return DisplayStatus.VALID
            if all_the_results_are_unsubscribed:
                return DisplayStatus.INVALID
            else:
                return DisplayStatus.WARNING
        else:
            logging.info("No matching results")
            return DisplayStatus.INVALID
                
                
    def show_status_icon(self, display_status):
        if (display_status == DisplayStatus.VALID):
            self.app_gui.show_valid_display()
        elif (display_status == DisplayStatus.INVALID):
            self.app_gui.show_invalid_display()
        elif (display_status == DisplayStatus.WARNING):
            self.app_gui.show_warning_display()
            

    def client_match_found(self):
        if(self.matching_results != [] and len(self.matching_results) > 0):
            return True
        return False
    
                
    def first_result_have_valid_match_ratio(self):
        if(self.matching_results):
            if(self.get_first_result().match_ratio >= self.config_importer.get_image_valid_threshold()):
                return True
        return False

            
    def reset_ocr_results(self):
        self.matching_results = []


    def get_first_result(self):
        return self.matching_results[0]
    
    
    def add_matching_results_from_cleaned_lines(self, cleaned_lines_array):
        logging.info("Total cleaned text : " + str(cleaned_lines_array))

        matching_result_threads = []

        for line in cleaned_lines_array:
            thread_line_matching = threading.Thread(target=self.add_matching_result_for_a_line, args=(line,))
            thread_line_matching.start()
            matching_result_threads.append(thread_line_matching)

        # Wait for all threads to complete
        for thread in matching_result_threads:
            thread.join()
        
        
    def add_matching_result_for_a_line(self, line):
        matching_line_results = self.match_analyser.return_the_top_three_matches_for_a_line(line)
        for match in matching_line_results:
            logging.info("Matching result : " + str(match))
            self.matching_results.append(match)    
    
    
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
                self.valid_lines_found = True
                logging.info("Found a line which is valid : " + cleaned_line)
                word_boxes = []
                
                for left, top, width, height in words_per_line[["left", "top", "width", "height"]].values:
                    word_boxes.append((left, top))
                    word_boxes.append((left + width, top + height))

                x, y, w, h = cv2.boundingRect(np.array(word_boxes))
                x = x + RECTANGLE_START_POINT[0]
                y = y + RECTANGLE_START_POINT[1]
                
                captured_image = self.image_formatter.add_rectangles_and_text_from_ocr(captured_image, x, y, w, h, cleaned_line)
                
                cleaned_ocr_text.append(cleaned_line)
        self.add_matching_results_from_cleaned_lines(cleaned_ocr_text)

        return captured_image

    def remove_duplicate_matching_results(self):
        logging.info("Removing duplicate matching results")
        
        self.matching_results.sort(key=lambda x: x.match_ratio, reverse=False)
        currated_matching_results = self.matching_results.copy()
        
        for index in range(len(self.matching_results)-1):
            
            weak_duplicate_removed = False
            sub_index = index + 1
            while not weak_duplicate_removed and sub_index < len(self.matching_results):
                if self.is_a_weak_duplicate(index, sub_index):
                    currated_matching_results.remove(self.matching_results[index])
                    weak_duplicate_removed = True
                        
                sub_index += 1
                       
        self.matching_results = currated_matching_results.copy()
        
        
    def is_a_weak_duplicate(self, index, sub_index):
        return self.matching_results[index].client_id == self.matching_results[sub_index].client_id \
            and self.matching_results[index].match_ratio <= self.matching_results[sub_index].match_ratio
        
        
    def main(self):
        self.image_acquisition = ImageAcquisition()
        self.image_acquisition.start_camera()
        self.image_acquisition.start_movement_detection()

        image_has_been_analysed = True

        # Show the first image
        final_image = self.image_formatter.get_image_ready_for_preview_display(self.image_acquisition.last_captured_image)
        self.app_gui.update_the_camera_preview_with_last_image(final_image)

        # Start a loop to continuously update the displayed image
        while True:
            self.reset_ocr_results()

            if self.show_csv_popup != PopupStatus.NO_POPUP:
                logging.info("show_csv_popup : " + str(self.show_csv_popup))

                logging.info("Showing popup message...")
                self.app_gui.csv_popup_message(self.show_csv_popup)                
                self.show_csv_popup = PopupStatus.NO_POPUP
                    
            elif not self.app_gui.is_keyboard_mode :    
                if not image_has_been_analysed:
                    final_image = self.image_formatter.get_image_ready_for_preview_display(self.image_acquisition.last_captured_image)
                    self.app_gui.update_the_camera_preview_with_last_image(final_image)

                if self.image_acquisition.motion_detected:
                    logging.info("Mouvement détecté !")
                    image_has_been_analysed = False
                    self.valid_lines_found = False
                    self.app_gui.show_movement_detected_display()

                if self.image_acquisition.image_is_steady() and not image_has_been_analysed:
                    self.app_gui.show_loading_display()
                    self.app_gui.update_window()
                    logging.info("Analyse !")
                    try:
                        modified_image = self.apply_ocr_on_image(self.image_acquisition.last_prepared_image, self.image_acquisition.last_captured_image)
                        self.remove_duplicate_matching_results()
                        self.reorder_results_to_show_the_most_corresponding_result_first()
                        self.show_status_icon(self.get_display_status())                    
                        self.show_correct_display_depending_on_results()
                        resized_modified_image = self.image_formatter.resize_image(modified_image)
                        self.app_gui.update_the_camera_preview_with_last_image(resized_modified_image)
                        image_has_been_analysed = True
                    except:
                        logging.info("Erreur lors de l'analyse !")
                        logging.error("Unexpected error:" + str(traceback.format_exc()))
                        logging.info("Image has been analysed = " + str(image_has_been_analysed))
            elif self.app_gui.text_need_to_be_processed :
                try:
                    searched_text = self.app_gui.get_searched_text()
                    self.app_gui.text_need_to_be_processed = False
                    cleaned_searched_text = self.text_cleaner.clean_text(searched_text)
                    if cleaned_searched_text != "":
                        self.valid_lines_found = True
                    self.add_matching_results_from_cleaned_lines([cleaned_searched_text])
                    self.reorder_results_to_show_the_most_corresponding_result_first()
                    self.show_status_icon(self.get_display_status())
                    self.show_correct_display_depending_on_results()
                    self.valid_lines_found = False
                except:
                    logging.info("Erreur lors de l'analyse !")
                    logging.error("Unexpected error:" + str(traceback.format_exc()))
                    logging.info("Image has been analysed = " + str(image_has_been_analysed))
                

            # Update the window to show the new image
            self.app_gui.update_window()
