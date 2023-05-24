from image_processor.image_constants import *
from tkinter import Tk, Label, Frame, Button, Text,  Y, END, LEFT, messagebox
from PIL import ImageTk, Image
import tkinter as tk
import logging


logging.basicConfig(level=logging.INFO, filename="app.log", filemode="w")
logging.debug('Log Start')

class AppGui:
    
    def __init__(self):
        self.create_the_app_window()
        logging.info("App window created")

        
    def create_the_app_window(self):
        self.window = Tk()
        self.window.title("Street Facteur")
        self.window.geometry("800x480")
        self.window.attributes('-fullscreen', True)

        self.window.resizable(width=False, height=False)
        self.window.configure(background='gray')
        
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
        self.matching_text_widget.tag_configure("correspondance_rate", font=("Times", 12, "italic"), justify="right")
        self.matching_text_widget.tag_configure("separator", foreground='gray' , justify="center")
        self.matching_text_widget.tag_configure("bold", font=("TkDefaultFont", 12, "bold"))


    def create_the_camera_frame(self):
        self.camera_frame = Frame(self.window, width=550, height=405)
        self.camera_frame.pack()
        self.camera_frame.place(relx=.01, y=5)


    def popup_message(self):
        messagebox.showinfo("Changement du CSV", "Le fichier CSV a été changé par l'utilisateur, l'application peut rencontrer des problèmes durant les prochaines secondes.")


    def create_the_pop_up(self):
        popup_button = tk.Button(self.window, text="Afficher la pop-up", command=self.popup_message)
        popup_button.pack()


    def create_the_camera_preview_zone(self):
        self.camera_preview_zone = Label(self.camera_frame)
        self.camera_preview_zone.pack()


    def create_the_readed_line_frame(self):
        self.readed_line_frame = Frame(self.window, width=550, height=50)
        self.readed_line_frame.pack()
        self.readed_line_frame.place(relx=.01, rely=.88)


    def create_the_readed_line_widget(self):
        self.read_line_widget = Text(self.readed_line_frame, width = 68, height=3)
        self.read_line_widget.pack(side=LEFT, fill=Y)
        self.read_line_widget.tag_configure("blue", foreground="blue")
        self.read_line_widget.tag_configure("bold", font=("TkDefaultFont", 12, "bold"))


    def create_the_result_logo_frame(self):
        self.result_logo_frame = Frame(self.window, width=150, height=100)
        self.result_logo_frame.pack()
        self.result_logo_frame.place(relx=.75, rely=.65)


    def create_the_result_logo_widget(self):
        self.result_logo_widget = Label(self.result_logo_frame)
        self.result_logo_widget.pack()


    def insert_a_separator_in_matching_text_widget(self):
        self.matching_text_widget.insert(END, "---------------------\n", "separator")
  
  
    def insert_a_match_in_txt_result_widget(self, company_name, status, correspondance_rate):
        self.matching_text_widget.insert(END, company_name + "\n", "nom")
        self.matching_text_widget.insert(END, status + "\n", "statut_valide" if status == "ABONNE" else "statut_invalide")
        self.matching_text_widget.insert(END, "Correspondance : ")
        self.matching_text_widget.insert(END, str(correspondance_rate) + "%\n", "correspondance_rate")


    def insert_a_separator_in_matching_text_widget(self):
        self.matching_text_widget.insert(END, "---------------------\n", "separator")


    def show_waiting_display(self):
        self.window['bg'] = 'gray'
        self.remove_text_from_text_widgets()
        self.matching_text_widget.insert(END, "Attente avant analyse !\n",('bold','colored'))
        self.show_loading_image()
        
        
    def show_movement_detected_display(self):
        self.window['bg'] = 'gray'
        self.remove_text_from_text_widgets()
        self.matching_text_widget.insert(END, "Mouvement détecté !\n",('bold','colored'))
        self.show_shaking_image()


    def show_analysed_lines(self, analysed_lines):
        self.remove_text_from_analysed_lines_widget()
        self.read_line_widget.insert(END, "Lignes analysées : \n",('bold','blue'))
        for analysed_line in analysed_lines:
            self.read_line_widget.insert(END, analysed_line + " , ", "blue")
            
            
    def remove_text_from_text_widgets(self):
        self.matching_text_widget.replace('1.0', END, "")
        self.read_line_widget.replace('1.0', END, "")
        
        
    def remove_text_from_result_widget(self):
        self.matching_text_widget.replace('1.0', END, "")
        
    
    def remove_text_from_analysed_lines_widget(self):
        self.read_line_widget.replace('1.0', END, "")
            

    def show_warning_image(self):
        image = Image.open(WARNING_IMAGE_PATH)
        resized_image = image.resize((150, 150))
        self.update_result_logo_image(resized_image)


    def show_invalid_display(self):
        self.window['bg'] = 'red'
        self.show_invalid_image()
        
    
    def show_valid_display(self):
        self.window['bg'] = 'light green'
        self.show_valid_image()
        
    
    def show_no_text_found_display(self):
        self.window['bg'] = 'red'
        self.remove_text_from_text_widgets()
        self.show_invalid_image()
        self.matching_text_widget.insert(END, "Aucun texte détecté !\n",('bold','colored'))   
    
    
    def show_no_match_found_display(self):
        self.window['bg'] = 'red'
        self.remove_text_from_result_widget()
        self.show_invalid_image()
        self.matching_text_widget.insert(END, "Aucune correspondance trouvée !\n",('bold','colored'))    
    
    def show_warning_display(self):
        self.window['bg'] = 'orange'
        self.show_warning_image()


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
        
        
    def show_shaking_image(self):
        image = Image.open(SHAKING_IMAGE_PATH)
        resized_image = image.resize((150, 150))
        self.update_result_logo_image(resized_image)


    def update_result_logo_image(self, resized_image):
        self.result_logo_widget.image = ImageTk.PhotoImage(resized_image)
        self.result_logo_widget.configure(image=self.result_logo_widget.image)
   
   
    def update_the_camera_preview_with_last_image(self, image_to_display):
        # Capture the actual image
        # Convert the captured image to a Tkinter compatible format
        final_image = Image.fromarray(image_to_display)
        final_image = ImageTk.PhotoImage(final_image)
        # Update the image displayed in the Label Widget
        self.camera_preview_zone.configure(image=final_image)
        self.camera_preview_zone.image = final_image   
        
    
    def update_window(self):
        self.window.update()
        
            
    


