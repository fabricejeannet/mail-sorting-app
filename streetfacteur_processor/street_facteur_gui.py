from image_processor.image_formatter import ImageFormatter
from image_processor.image_acquisition import ImageAcquisition
from image_processor.image_constants import *
from text_processor.text_cleaner import TextCleaner
from text_processor.text_extractor import TextExtractor
from match_processor.match_analyser import MatchAnalyser
from csv_processor.csv_manager import CsvManager
from config_processor.config_importer import ConfigImporter
from tkinter import Tk, Label, Frame, Button, Text, BOTH, Scrollbar, RIGHT, Y, END, TOP, LEFT, X, Entry, StringVar, IntVar, OptionMenu, Menu, messagebox, filedialog, ttk
from PIL import ImageTk, Image
import cv2
import numpy as np
import time
import logging

logging.basicConfig(level=logging.INFO, filename="app.log", filemode="w")
logging.debug('Log Start')

class StreetFacteur:
    
    def __init__(self):
        self.config_importer = ConfigImporter()
        self.config_importer.import_config()
        self.image_formatter = ImageFormatter()
        self.image_acquisition = ImageAcquisition()
        self.text_cleaner = TextCleaner()
        csv_manager = CsvManager()
        csv_manager.open_csv_file(csv_manager.get_latest_csv_file())
        clients_data_dictionary = csv_manager.get_clients_data_dictionnary()
        self.text_extractor = TextExtractor()
        self.match_analyser = MatchAnalyser(clients_data_dictionary)
        self.image_acquisition.start_camera()
        self.last_movement_time = time.time()
        self.create_the_app_window()
        
        # Create a frame and a label to display the camera preview
        self.create_the_camera_frame()
        self.create_the_camera_preview_zone()
        
        #Create a text frame and a text widget to display the result of the OCR
        self.create_the_text_result_frame()
        self.create_the_text_result_widget()
        

        # Create a frame and a text widget to display the readed line 
        self.create_the_readed_line_frame()
        self.create_the_readed_line_widget()		
        
        # Create a frame and a label to display the result logo
        self.create_the_result_logo_frame()
        self.create_the_result_logo_widget()
                
    
    def create_the_app_window(self):
        self.window = Tk()
        self.window.title("Street Facteur")
        self.window.geometry("800x480")
        self.window.attributes('-fullscreen', True)

        self.window.resizable(width=False, height=False)
        self.window.configure(background='gray')
        
        
    def image_is_steady(self):
        return time.time() - self.last_movement_time > STEADY_WAIT_TIME        
        
    def create_the_text_result_frame(self):
        self.text_frame = Frame(self.window, width=150, height=200, bg="white")
        self.text_frame.pack()
        self.text_frame.place(relx=.72, rely=.012)


    def create_the_text_result_widget(self):
        # Create a Text widget
        self.matching_text_widget = Text(self.text_frame, width=25, height=18)
        self.matching_text_widget.pack(side=LEFT, fill=Y)
        self.matching_text_widget.tag_configure("blue", foreground="blue")
        self.matching_text_widget.tag_configure("red", foreground="red")
        self.matching_text_widget.tag_configure("green", foreground="green")
        self.matching_text_widget.tag_configure("nom", font=("TkDefaultFont", 12, "bold"), foreground="blue", justify="center")
        self.matching_text_widget.tag_configure("statut_valide", font=("TkDefaultFont", 12, "bold"), foreground="green", justify="center")
        self.matching_text_widget.tag_configure("statut_invalide", font=("TkDefaultFont", 12, "bold"), foreground="red", justify="center")
        self.matching_text_widget.tag_configure("correspondance_rate", font=("Times", 10, "italic"), justify="right")
        self.matching_text_widget.tag_configure("separator", foreground='gray' , justify="center")
        self.matching_text_widget.tag_configure("bold", font=("TkDefaultFont", 12, "bold"))


    def create_the_camera_frame(self):
        self.camera_frame = Frame(self.window, width=550, height=405)
        self.camera_frame.pack()
        self.camera_frame.place(relx=.01, y=5)


    def create_the_camera_preview_zone(self):
        self.camera_preview_zone = Label(self.camera_frame)
        self.camera_preview_zone.pack()


    def create_the_readed_line_frame(self):
        self.readed_line_frame = Frame(self.window, width=550, height=50)
        self.readed_line_frame.pack()
        self.readed_line_frame.place(relx=.01, rely=.88)


    def create_the_readed_line_widget(self):
        self.readed_line_widget = Text(self.readed_line_frame, width = 68, height=3)
        self.readed_line_widget.pack(side=LEFT, fill=Y)
        self.readed_line_widget.tag_configure("blue", foreground="blue")
        self.readed_line_widget.tag_configure("bold", font=("TkDefaultFont", 12, "bold"))


    def create_the_result_logo_frame(self):
        self.result_logo_frame = Frame(self.window, width=150, height=100)
        self.result_logo_frame.pack()
        self.result_logo_frame.place(relx=.75, rely=.65)

    def create_the_result_logo_widget(self):
        self.result_logo_widget = Label(self.result_logo_frame)
        self.result_logo_widget.pack()
        
        
    def reset_ocr_results(self):
        self.matching_results = []


    def insert_a_separator_in_matching_text_widget(self):
        self.matching_text_widget.insert(END, "---------------------\n", "separator")
  
  
    def insert_a_match_in_txt_result_widget(self, company_name, status, correspondance_rate):
        self.matching_text_widget.insert(END, company_name + "\n", "nom")
        self.matching_text_widget.insert(END, status + "\n", "statut_valide" if status == "ABONNE" else "statut_invalide")
        self.matching_text_widget.insert(END, str(correspondance_rate) + "%\n", "correspondance_rate")


    def insert_a_separator_in_matching_text_widget(self):
        self.matching_text_widget.insert(END, "---------------------\n", "separator")


    def remove_text_from_text_widgets(self):
        self.matching_text_widget.replace('1.0', END, "")
        self.readed_line_widget.replace('1.0', END, "")
    

    def show_warning_image(self):
        image = Image.open(WARNING_IMAGE_PATH)
        resized_image = image.resize((150, 150))
        self.update_result_logo_image(resized_image)


    def show_loading_image(self):
        image = Image.open(LOADING_IMAGE_PATH)
        resized_image = image.resize((150, 150))
        self.update_result_logo_image(resized_image)


    def show_valid_image(self):
        image = Image.open(VALID_IMAGE_PATH)
        resized_image = image.resize((150, 150))
        self.update_result_logo_image(resized_image)


    def show_invalid_image(self):
        image = Image.open(INVALID_IMAGE_PATH)
        resized_image = image.resize((150, 150))
        self.update_result_logo_image(resized_image)


    def update_result_logo_image(self, resized_image):
        self.result_logo_widget.image = ImageTk.PhotoImage(resized_image)
        self.result_logo_widget.configure(image=self.result_logo_widget.image)
   
   
    def has_detected_a_movement(self):   
        frame_count = 0
        previous_frame = None

        while True:
            frame_count += 1

            # 1. Load image; convert to RGB
            image_brg = self.image_acquisition.get_image()
            image_rgb = cv2.cvtColor(src=image_brg, code=cv2.COLOR_BGR2RGB)

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
                kernel = np.ones((5, 5))
                diff_frame = cv2.dilate(diff_frame, kernel, 1)

                # 5. Only take different areas that are different enough (>20 / 255)
                thresh_frame = cv2.threshold(src=diff_frame, thresh=21, maxval=255, type=cv2.THRESH_BINARY)[1]

                contours, _ = cv2.findContours(image=thresh_frame, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)

                contours, _ = cv2.findContours(image=thresh_frame, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
                for contour in contours:
                    if cv2.contourArea(contour) < 60:
                        # too small: skip!
                        continue
                    return True
                return False
            
            
    def add_result_to_tkinter_text(self):
        self.remove_text_from_text_widgets()
        self.readed_line_widget.insert(END, "Lignes analysées : \n",('bold','blue'))
        for analysed_line in self.analysed_lines:
            self.readed_line_widget.insert(END, str(analysed_line) + "\n")
        for analysed_line_matchs in self.matching_results:
            for index in range(len(analysed_line_matchs)):
                if(analysed_line_matchs[index].matching_string != ""):
                    self.insert_a_match_in_txt_result_widget(analysed_line_matchs[index].matching_string, analysed_line_matchs[index].status, analysed_line_matchs[index].correspondance_ratio)
                    self.insert_a_separator_in_matching_text_widget()


    def show_the_good_image_depending_on_the_result(self):
        logging.info("show_the_good_image_depending_on_the_result")
        if(self.matching_results != []):
            all_the_results_are_subscribed = True
            for analysed_line_matchs in self.matching_results:
                logging.info(analysed_line_matchs[0].status)
                if(analysed_line_matchs[0].status != "ABONNE"):
                    all_the_results_are_subscribed = False
                    break
            all_the_results_are_unsubscribed = True
            for analysed_line_matchs in self.matching_results:
                if(analysed_line_matchs[0].status == "ABONNE"):
                    all_the_results_are_unsubscribed = False
                    break
            if(all_the_results_are_subscribed and self.check_if_the_first_result_have_a_good_correspondance_rate()):
                self.show_valid_image()
            if(all_the_results_are_unsubscribed or not self.check_if_the_first_result_have_a_minimum_correspondance_rate()):
                self.show_invalid_image()
            else:
                self.show_warning_image()
        else:
            logging.info("No matching results")
            self.show_invalid_image()
                
                
    def check_if_the_first_result_have_a_good_correspondance_rate(self):
        if(self.matching_results):
            if(self.get_first_analysed_line_results()[0].correspondance_ratio >= CORRESPONDANCE_RATE_THRESHOLD):
                return True
        return False
    
    
    def check_if_the_first_result_have_a_minimum_correspondance_rate(self):
        if(self.matching_results):
            if(self.get_first_analysed_line_results()[0].correspondance_ratio >= MINIMUM_CORRESPONDANCE_RATE_THRESHOLD):
                return True
        return False


    def get_first_analysed_line_results(self):
        return self.matching_results[0]
    
    
    def add_matching_results_from_cleaned_ocr_result(self, cleaned_ocr_result):
        logging.info("cleaned_ocr_result : " + str(cleaned_ocr_result))
        self.analysed_lines = cleaned_ocr_result
        for line in cleaned_ocr_result:
            logging.info("line : " + str(line))
            matching_line_results = self.match_analyser.return_the_top_three_matches_for_a_line(line)
            logging.info("matching_line_results : " + str(matching_line_results))
            self.matching_results.append(matching_line_results)
            if self.matching_results and self.matching_results[0][0].correspondance_ratio == 100:
                break
            
            
    def apply_ocr_on_image(self):
        self.reset_ocr_results()
        image_to_analyse = self.image_formatter.get_image_ready_for_text_detection(self.image_acquisition.get_image())
        cleaned_ocr_text = self.text_extractor.get_cleaned_text_from_image(image_to_analyse)
        self.add_matching_results_from_cleaned_ocr_result(cleaned_ocr_text)
            
            
    def main(self):		
        image_has_been_analysed = True

        # Start a loop to continuously update the displayed image
        while True:
            escape_key_pressed = False
            if not image_has_been_analysed:
                logging.info("Attente d'une seconde avant analyse !")
                self.remove_text_from_text_widgets()
                self.matching_text_widget.insert(END, "Attente d'une seconde avant analyse !\n",('bold','colored'))
                self.show_loading_image()

            if (self.has_detected_a_movement()):
                logging.info("Mouvement détecté !")
                self.remove_text_from_text_widgets()
                self.matching_text_widget.insert(END, "Mouvement détecté !\n",('bold','colored'))
                self.last_movement_time = time.time()
                image_has_been_analysed = False
            
                
            if (self.image_is_steady() and not image_has_been_analysed):
                logging.info("Image stable, analyse !")
                try:
                    self.apply_ocr_on_image()
                    self.show_the_good_image_depending_on_the_result()
                    image_has_been_analysed = True
                    self.add_result_to_tkinter_text()
                except:
                    logging.info("Erreur lors de l'analyse !")

            # Capture the actual image
            final_image = self.image_formatter.get_image_ready_for_display(self.image_acquisition.get_image())
            # Convert the captured image to a Tkinter compatible format
            final_image = Image.fromarray(final_image)
            final_image = ImageTk.PhotoImage(final_image)
            # Update the image displayed in the Label Widget
            self.camera_preview_zone.configure(image=final_image)
            self.camera_preview_zone.image = final_image
            # Update the window to show the new image
            self.window.update()
        