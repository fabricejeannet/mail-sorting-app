from image_processor.image_constants import *
from config_processor.config_importer import ConfigImporter
from gui_processor.result_frame import ResultFrame
from tkinter import Tk , Button, Label, Frame, Entry, PanedWindow, END, LEFT, VERTICAL, RIGHT, BOTH, Text, Scrollbar, Y, X, BOTTOM, TOP, Canvas
from PIL import ImageTk, Image
import tkinter as tk
import logging
from streetfacteur_processor.app_constants import *


logging.basicConfig(level=logging.INFO, filename="app.log", filemode="w")
logging.debug('Log Start')

class AppGui:
    
    def __init__(self):
        self.config_importer = ConfigImporter()
        self.popup = None
        self.is_keyboard_mode = False
        self.text_need_to_be_processed = False
        logging.info("App window created")        
        
        self.create_the_app_window()
        self.user_entry.bind('<Return>', lambda event: self.process_text_of_user_entry())
        self.window.bind("<F1>", lambda event: self.switch_frame())


    def create_the_app_window(self):
        self.window = Tk()
        self.window.title("Street Facteur")
        self.window.geometry("800x480")
        self.window.attributes('-fullscreen', True)

        self.window.resizable(width=False, height=False)
        self.window.configure(background='gray')        

        image = Image.open(self.config_importer.get_camera_icon_path())
        image = image.resize((55, 55))  
        self.camera_icon = ImageTk.PhotoImage(image)
        
        image = Image.open(self.config_importer.get_keyboard_icon_path())
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
        
        self.user_entry = Entry(self.keyboard_frame,bg="white",width=35, borderwidth=5, font=('Helvetica', 20), justify='center', relief='sunken', highlightthickness=2, highlightcolor="black", highlightbackground="black")
        self.user_entry.pack()
        self.user_entry.focus_set()
        self.user_entry.place(relx=0.05, rely=0.2, width=500, height=80)

        button_frame = Frame(self.keyboard_frame)
        button_frame.pack()
        # Création des widgets dans la sous-frame du clavier
        search_button = Button(self.keyboard_frame, text="Recherche", command=self.process_text_of_user_entry)
        search_button.pack()
        search_button.place(relx=0.4, rely=0.4, width=150, height=80)

        clear_button = Button(self.keyboard_frame, text="Effacer", command=self.clean_text_of_user_entry)
        clear_button.pack()
        clear_button.place(relx=0.1, rely=0.4, width=150, height=80)
        
        self.create_switch_button_frame(self.keyboard_frame)
        self.create_keyboard_switch_button()
        

    def create_the_camera_frame(self):
        self.camera_frame = Frame(self.window)
        # Configurer la frame de la caméra
        self.camera_frame.pack(fill='both', expand=True)


    def create_switch_button_frame(self, frame):
        button_frame = Frame(frame)
        button_frame.pack()
        button_frame.place(relx=0.01, rely=0.867)
        self.switch_button_frame = button_frame
        
    
    def process_text_of_user_entry(self):
        if self.is_keyboard_mode:
            logging.info("Texte de l'utilisateur: " + self.get_searched_text())
            self.show_loading_display()
            self.text_need_to_be_processed = True
        
        
    def get_searched_text(self):
        return self.user_entry.get()
    
    
    def create_keyboard_switch_button(self):        
        button = Button(self.switch_button_frame, command=self.show_camera_frame, image=self.camera_icon)
        button.pack()
        
    
    def create_camera_switch_button(self):
        # Resizing image to fit on button
        button = Button(self.switch_button_frame, command=self.show_keyboard_frame, image=self.keyboard_icon)
        button.pack()


    def create_the_camera_frame_widgets(self):
        self.create_the_camera_preview_zone()
        
        self.create_text_result(self.camera_frame)

        self.create_switch_button_frame(self.camera_frame)
        self.create_camera_switch_button()
        
        self.create_the_result_analyser_frame(self.camera_frame)
        self.create_the_result_analyser_widgets()
        
    
    def switch_frame(self):
        if self.is_keyboard_mode:
            self.show_camera_frame()
        else :
            self.show_keyboard_frame()


    def show_keyboard_frame(self):
        self.camera_frame.pack_forget()
        self.create_text_result(self.keyboard_frame)
        self.create_the_result_analyser_frame(self.keyboard_frame)
        self.create_the_result_analyser_widgets()
        self.user_entry.configure(state='normal')
        self.is_keyboard_mode = True
        self.keyboard_frame.pack(fill='both', expand=True)


    def show_camera_frame(self):
        self.keyboard_frame.pack_forget()
        self.create_text_result(self.camera_frame)
        self.create_the_result_analyser_frame(self.camera_frame)
        self.create_the_result_analyser_widgets()
        self.is_keyboard_mode = False
        self.user_entry.configure(state='disabled')
        self.camera_frame.pack(fill='both', expand=True)


    def create_text_result(self, frame):
        self.create_the_text_result_frame(frame)
        self.create_the_text_result_widget()

        
    def create_the_text_result_frame(self,frame):
        self.text_frame = Frame(frame, border=1, relief="solid")
        self.text_frame.pack()
        self.text_frame.place(relx=.71, rely=.012, width=228, height=465)
        
        
    def create_the_result_analyser_widgets(self):
        self.result_analyser_icon = Label(self.result_analyser_frame, image=self.camera_icon)
        self.result_analyser_icon.pack(side=LEFT)

        if self.is_keyboard_mode:
            text = self.config_importer.get_keyboard_input_message()
        else:
            text = self.config_importer.get_camera_input_message()
            
        self.result_analyser_text = Label(self.result_analyser_frame, text=text, justify=LEFT, font=('Helvetica', 16), wraplength=420)
        self.result_analyser_text.pack(side=RIGHT, fill=BOTH, expand=True)
                
                
    def create_the_result_analyser_frame(self, frame):
        self.result_analyser_frame = Frame(frame, border=1, relief="solid")
        self.result_analyser_frame.pack()
        self.result_analyser_frame.place(relx=.1, rely=.868, width=480, height=55)
        
        
    def clean_text_of_user_entry(self):
        self.user_entry.delete(0, END)
        

    def create_the_text_result_widget(self):
        # Create a Text widget
        self.matching_result_widget = Frame(self.text_frame)
        self.matching_result_widget.pack(expand=True, fill=BOTH)
        vertical_scrollbar = Scrollbar(self.matching_result_widget)
        vertical_scrollbar.pack(side=RIGHT, fill=Y)


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
        self.camera_preview_zone = Label(self.camera_frame, width=550, height=400, bg="black")
        self.camera_preview_zone.pack()
        self.camera_preview_zone.place(relx=.01, y=5)

        
    def insert_a_match_in_txt_result_widget(self, client_match_result):
        
        result_frame = ResultFrame(self.matching_result_widget, client_match_result).get_result_frame()
        
        result_frame.pack(fill=X, expand=False)


    def show_loading_display(self):
        self.clear_result_widget()
        self.set_result_analyser_text(self.config_importer.get_analysing_message())
        self.show_loading_image()
        
        
    def show_movement_detected_display(self):
        self.clear_result_widget()
        self.set_result_analyser_text(self.config_importer.get_movement_detected_message())
        self.show_shaking_image()
        self.reset_result_analyser_color()
                   
        
    def clear_result_widget(self):
        self.matching_result_widget.destroy()
        self.create_the_text_result_widget()


    def show_invalid_display(self, message):
        self.show_invalid_image()
        self.set_result_analyser_text(message)
        self.set_result_analyser_color_to_red()

        
    def show_warning_display(self, message):
        self.show_warning_image()
        self.set_result_analyser_text(message)
        self.set_result_analyser_color_to_orange()
        
    
    def show_valid_display(self, message):
        self.show_valid_image()
        self.set_result_analyser_text(message)
        self.set_result_analyser_color_to_green()
        
    
    def set_result_analyser_text(self, message):
        self.result_analyser_text.config(text=message)
        
        
    def set_result_analyser_color_to_red(self):
        self.result_analyser_text.config(bg="red")
        self.result_analyser_icon.config(bg="red")
        
    
    def set_result_analyser_color_to_green(self):
        self.result_analyser_text.config(bg="lightgreen")
        self.result_analyser_icon.config(bg="lightgreen")
        
    
    def set_result_analyser_color_to_orange(self):
        self.result_analyser_text.config(bg="orange")
        self.result_analyser_icon.config(bg="orange")
        
        
    def reset_result_analyser_color(self):
        self.result_analyser_text.config(bg="lightgray")
        self.result_analyser_icon.config(bg="lightgray")
        
    
    def show_no_text_found_display(self):
        self.clear_result_widget()
        self.show_invalid_image()
        self.set_result_analyser_text(NO_TEXT_FOUND)


    def show_loading_image(self):
        image = Image.open(self.config_importer.get_loading_icon_path())
        resized_image = image.resize((55, 55))
        self.update_result_logo_image(resized_image)


    def show_valid_image(self):
        image = Image.open(self.config_importer.get_valid_icon_path())
        resized_image = image.resize((55, 55))
        self.update_result_logo_image(resized_image)


    def show_warning_image(self):
        image = Image.open(self.config_importer.get_warning_icon_path())
        resized_image = image.resize((55, 55))
        self.update_result_logo_image(resized_image)
        

    def show_invalid_image(self):
        image = Image.open(self.config_importer.get_invalid_icon_path())
        resized_image = image.resize((55, 55))
        self.update_result_logo_image(resized_image)
        
        
    def show_shaking_image(self):
        image = Image.open(self.config_importer.get_shaking_camera_icon_path())
        resized_image = image.resize((55, 55))
        self.update_result_logo_image(resized_image)


    def update_result_logo_image(self, resized_image):
        self.result_analyser_icon.image = ImageTk.PhotoImage(resized_image)
        self.result_analyser_icon.configure(image=self.result_analyser_icon.image)
   
   
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
        
            
    


