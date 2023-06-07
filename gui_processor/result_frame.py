from tkinter import Frame, Label, LEFT, BOTTOM, RIGHT, BOTH, TOP
from PIL import ImageTk, Image

from csv_processor.csv_constants import SUBSCRIBED
from config_processor.config_importer import ConfigImporter

class ResultFrame:
    
    def __init__(self, matching_result_widget, client_match_result):
        self.config_importer = ConfigImporter()
        # if client_match_result.matching_company and client_match_result.matching_person :
        #     pass
        # else :
        self.create_a_single_result_frame(matching_result_widget, client_match_result)
        
        
    def get_result_frame(self):
        return self.result_frame
    
    
    def create_a_single_result_frame(self, matching_result_widget, client_match_result):
        image = Image.open(self.config_importer.get_human_icon_path())
        image = image.resize((40, 40))  
        human_icon = ImageTk.PhotoImage(image)
        
        image = Image.open(self.config_importer.get_company_icon_path())
        image = image.resize((40, 40))  
        company_icon = ImageTk.PhotoImage(image)
        
        if client_match_result.status == SUBSCRIBED:
            self.result_frame = Frame(matching_result_widget, bg="lightgreen", border=1, relief="solid", width=200, height=90)
        else:
            self.result_frame = Frame(matching_result_widget, bg="red", border=1, relief="solid", width=200, height=90)
            
        #Image de personnage à gauche du texte prenant environ 1/5 de la largeur
        result_icon = Label(self.result_frame, image=None, bg=self.result_frame['bg'])
        
        if client_match_result.matching_company is not None:
            result_icon.image = company_icon
            result_icon.configure(image=company_icon)
            result_icon.pack(side=LEFT)
            company_name_label = Label(self.result_frame, text=client_match_result.matching_company , font=("TkDefaultFont", 12, "bold"), bg=self.result_frame['bg'], wraplength=150)
            correspondance_rate_label = Label(self.result_frame, text=str(client_match_result.company_match_ratio )+ "%", font=("Times", 14, "italic bold"), bg=self.result_frame['bg'])
        
        else :
            result_icon.image = human_icon
            result_icon.configure(image=human_icon)
            result_icon.pack(side=LEFT)
            company_name_label = Label(self.result_frame, text=client_match_result.matching_person , font=("TkDefaultFont", 12, "bold"), bg=self.result_frame['bg'], wraplength=150)
            correspondance_rate_label = Label(self.result_frame, text=str(client_match_result.person_match_ratio)+ "%", font=("Times", 14, "italic bold"), bg=self.result_frame['bg'])

     
        company_name_label.pack(side=TOP)
        correspondance_rate_label.pack(side=BOTTOM)