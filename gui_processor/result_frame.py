from tkinter import Frame, Label, LEFT, BOTTOM, RIGHT, BOTH, TOP
from PIL import ImageTk, Image

from csv_processor.csv_constants import SUBSCRIBED

class ResultFrame:
    
    def __init__(self, matching_result_widget, client_match_result, image):
        
        if client_match_result.status == SUBSCRIBED:
            self.result_frame = Frame(matching_result_widget, bg="lightgreen", border=1, relief="solid", width=200, height=90)
        else:
            self.result_frame = Frame(matching_result_widget, bg="red", border=1, relief="solid", width=200, height=90)
            
        #Image de personnage à gauche du texte prenant environ 1/5 de la largeur
        result_icon = Label(self.result_frame, image=image, bg=self.result_frame['bg'])
        
        result_icon.image = image
        result_icon.configure(image=image)
        result_icon.pack(side=LEFT)

        company_name_label = Label(self.result_frame, text=client_match_result.matching_string , font=("TkDefaultFont", 10, "bold"), bg=self.result_frame['bg'], wraplength=150)
        correspondance_rate_label = Label(self.result_frame, text=str(client_match_result.match_ratio )+ "%", font=("Times", 14, "italic"), bg=self.result_frame['bg'])
        company_name_label.pack(side=TOP)
        correspondance_rate_label.pack(side=BOTTOM)
        
    def get_result_frame(self):
        return self.result_frame