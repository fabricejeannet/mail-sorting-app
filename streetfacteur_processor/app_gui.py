from image_processor.image_constants import *
from config_processor.config_importer import ConfigImporter
from tkinter import Tk , Button, Label, Frame, Entry, Text, END, LEFT, Y
from PIL import ImageTk, Image
import tkinter as tk
import logging
from streetfacteur_processor.app_constants import *


logging.basicConfig(level=logging.INFO, filename="app.log", filemode="w")
logging.debug('Log Start')

class AppGui:
    
    def __init__(self):
        config_importer = ConfigImporter()
        self.popup = None
        self.is_keyboard_mode = False
        self.text_need_to_be_processed = False
        logging.info("App window created")
        
        self.camera_image_path = config_importer.get_camera_icon_path()
        
        
        self.keyboard_image_path = config_importer.get_keyboard_icon_path()
        
        
        self.create_the_app_window()

        
    def create_the_app_window(self):
        self.window = Tk()
        self.window.title("Street Facteur")
        self.window.geometry("800x480")
        self.window.attributes('-fullscreen', True)

        self.window.resizable(width=False, height=False)
        self.window.configure(background='gray')
        
        image = Image.open(self.camera_image_path)
        image = image.resize((55, 55))  
        self.camera_icon = ImageTk.PhotoImage(image)
        
        image = Image.open(self.keyboard_image_path)
        image = image.resize((55, 55))  
        self.keyboard_icon = ImageTk.PhotoImage(image)
        
        self.create_the_camera_frame()
        self.create_the_camera_frame_widgets()
        
        self.create_the_keyboard_frame()
        self.create_the_keyboard_widgets()
        
        self.show_camera_frame()
        
    
    def create_the_keyboard_frame(self):
        self.keyboard_frame = Frame(self.window)
        # Configurer la frame du clavier
        self.keyboard_frame.pack(fill='both', expand=True)
        
        
    def create_the_keyboard_widgets(self):
        # Création de sous-frames à l'intérieur de la frame clavier
        search_frame = Frame(self.keyboard_frame)
        search_frame.pack()
        
        self.user_entry = Entry(search_frame,bg="white",width=35, borderwidth=5, font=('Helvetica', 20), justify='center', relief='sunken', highlightthickness=2, highlightcolor="black", highlightbackground="black")
        self.user_entry.pack()
        self.user_entry.focus_set()

        button_frame = Frame(self.keyboard_frame)
        button_frame.pack()
        # Création des widgets dans la sous-frame du clavier
        search_button = Button(search_frame, text="Recherche", command=self.process_text_of_user_entry)
        search_button.pack()
        search_frame.place(relx=0.02, rely=0.1)

        clear_button = Button(search_frame, text="Effacer", command=self.clean_text_of_user_entry)
        clear_button.pack(side="left")
        
        self.create_switch_button_frame(self.keyboard_frame)
        self.create_keyboard_switch_button()


    def create_the_camera_frame(self):
        self.camera_frame = Frame(self.window)
        # Configurer la frame de la caméra
        self.camera_frame.pack(fill='both', expand=True)


    def create_switch_button_frame(self, frame):
        button_frame = Frame(frame)
        button_frame.pack()
        button_frame.place(relx=0.01, rely=0.87)
        self.switch_button_frame = button_frame
        
    
    def process_text_of_user_entry(self):
        self.text_need_to_be_processed = True
        
        
    def get_searched_text(self):
        return self.user_entry.get()
    
    
    def create_keyboard_switch_button(self):        
        # Resizing image to fit on button
        button = Button(self.switch_button_frame, command=self.show_camera_frame, image=self.camera_icon)
        button.pack()
        
    
    def create_camera_switch_button(self):
        # Resizing image to fit on button
        button = Button(self.switch_button_frame, command=self.show_keyboard_frame, image=self.keyboard_icon)
        button.pack()


    def create_the_camera_frame_widgets(self):
        self.create_the_camera_preview_zone()
        
        self.create_text_result(self.camera_frame)
        readed_line_frame = self.create_the_readed_line_frame(self.camera_frame)
        self.create_the_readed_line_widget(readed_line_frame)
        self.create_the_result_logo_frame(self.camera_frame)
        self.create_the_result_logo_widget()
        
        self.create_switch_button_frame(self.camera_frame)
        self.create_camera_switch_button()


    def show_keyboard_frame(self):
        self.camera_frame.pack_forget()
        self.create_text_result(self.keyboard_frame)
        self.is_keyboard_mode = True
        
        self.create_the_result_logo_frame(self.keyboard_frame)
        self.create_the_result_logo_widget()
        self.keyboard_frame.pack(fill='both', expand=True)


    def show_camera_frame(self):
        self.keyboard_frame.pack_forget()
        self.create_text_result(self.camera_frame)
        self.is_keyboard_mode = False
        
        self.create_the_result_logo_frame(self.camera_frame)
        self.create_the_result_logo_widget()
        self.camera_frame.pack(fill='both', expand=True)


    def create_text_result(self, frame):
        self.create_the_text_result_frame(frame)
        self.create_the_text_result_widget()

        
    def create_the_text_result_frame(self,frame):
        self.text_frame = Frame(frame, width=150, height=200, bg="white")
        self.text_frame.pack()
        self.text_frame.place(relx=.72, rely=.012)
        
        
    def clean_text_of_user_entry(self):
        self.user_entry.delete(0, END)

    def create_the_text_result_widget(self):
        # Create a Text widget
        self.matching_text_widget = Text(self.text_frame, width=25, height=18)
        self.matching_text_widget.pack(side=LEFT, fill=Y)
        self.matching_text_widget.tag_configure("blue", foreground="blue")
        self.matching_text_widget.tag_configure("red", foreground="red")
        self.matching_text_widget.tag_configure("green", foreground="green")
        self.matching_text_widget.tag_configure("nom", font=("TkDefaultFont", 14, "bold"), foreground="blue", justify="center")
        self.matching_text_widget.tag_configure("statut_valide", font=("TkDefaultFont", 14, "bold"), foreground="green", justify="center")
        self.matching_text_widget.tag_configure("statut_invalide", font=("TkDefaultFont", 14, "bold"), foreground="red", justify="center")
        self.matching_text_widget.tag_configure("correspondance_rate", font=("Times", 14, "italic"), justify="right")
        self.matching_text_widget.tag_configure("separator", foreground='gray' , justify="center")
        self.matching_text_widget.tag_configure("bold", font=("TkDefaultFont", 14, "bold"))


    def csv_popup_message(self, popup_status):
        self.close_popup_message()
        self.popup = tk.Toplevel(self.window)
        self.popup.title("Changement du CSV")
        self.popup.attributes('-fullscreen', True)
        self.center_window(self.popup)
        if popup_status == PopupStatus.CSV_POPUP:
            self.popup_label = tk.Label(self.popup, text=CSV_POPUP_MESSAGE, wraplength=400, justify="center", font=("TkDefaultFont", 22, "bold"))
            self.window.after(5500, self.close_popup_message)
        else :
            self.popup_label = tk.Label(self.popup, text=NO_CSV_FILE_POPUP_MESSAGE, wraplength=400, justify="center", font=("TkDefaultFont", 22, "bold"))
        self.popup_label.pack(pady=20)



    def close_popup_message(self):
        if self.popup is not None:
            self.popup.destroy()


    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")


    def create_the_camera_preview_zone(self):
        self.camera_preview_zone = Label(self.camera_frame, width=550, height=405, bg="black")
        self.camera_preview_zone.pack()
        self.camera_preview_zone.place(relx=.01, y=5)


    def create_the_readed_line_frame(self, frame):
        readed_line_frame = Frame(frame, width=550, height=50)
        readed_line_frame.pack()
        readed_line_frame.place(relx=.1, rely=.88)
        return readed_line_frame


    def create_the_readed_line_widget(self, frame):
        self.read_line_widget = Text(frame, width = 60, height=3)
        self.read_line_widget.pack(side=LEFT, fill=Y)
        self.read_line_widget.tag_configure("normal", font=("TkDefaultFont", 14, "normal"))
        self.read_line_widget.tag_configure("bold", font=("TkDefaultFont", 14, "bold"))


    def create_the_result_logo_frame(self, frame):
        self.result_logo_frame = Frame(frame, width=150, height=100)
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


    def show_loading_display(self):
        self.window['bg'] = 'gray'
        self.remove_text_from_text_widgets()
        self.matching_text_widget.insert(END, ANALYSING_TEXT,('bold','colored'))
        self.show_loading_image()
        
        
    def show_movement_detected_display(self):
        self.window['bg'] = 'gray'
        self.remove_text_from_text_widgets()
        self.matching_text_widget.insert(END, MOTION_DETECTED,('bold','colored'))
        self.show_shaking_image()


    def show_analysed_lines(self, analysed_lines):
        self.remove_text_from_analysed_lines_widget()
        self.read_line_widget.insert(END, "Lignes analysées : ",('bold','blue'))
        for analysed_line in analysed_lines:
            self.read_line_widget.insert(END, analysed_line + "\n", "normal")
            
            
    def remove_text_from_text_widgets(self):
        self.matching_text_widget.replace('1.0', END, "")
        self.read_line_widget.replace('1.0', END, "")
        
        
    def clear_result_widget(self):
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
        self.matching_text_widget.insert(END, "Pas de texte valide détécté !\n",('bold','colored'))   
    
    
    def show_no_match_found_display(self):
        self.window['bg'] = 'red'
        self.clear_result_widget()
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
        self.update_window() 
        
    
    def update_window(self):
        self.window.update()
        
            
    


