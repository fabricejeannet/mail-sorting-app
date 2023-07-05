from tkinter import Frame, Label, LEFT, BOTTOM, RIGHT, BOTH, TOP, X
from PIL import ImageTk, Image

from csv_processor.csv_constants import SUBSCRIBED
from config_processor.config_importer import ConfigImporter
import logging

class ResultFrame:
    
    def __init__(self, matching_result_widget, client_match_result):
        self.config_importer = ConfigImporter()
        if client_match_result.matching_company and client_match_result.matching_person :
            logging.info("Creating a company and a person result frame")
            self.create_a_company_and_person_result_frame(matching_result_widget, client_match_result)
        else :
            logging.info("Creating a single result frame")
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
            self.result_frame = Frame(matching_result_widget, bg="lightgreen", border=1, relief="solid", width=200, height=80, pady=4)
        else:
            self.result_frame = Frame(matching_result_widget, bg="red", border=1, relief="solid", width=200, height=80, pady=4)
        
        domiciliation_agent_label = Label(self.result_frame, text=client_match_result.domiciliation_agent, font=("TkDefaultFont", 12, "bold"), bg=self.result_frame['bg'])
        
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

    def create_a_company_and_person_result_frame(self, matching_result_widget, client_match_result):
        image = Image.open(self.config_importer.get_human_icon_path())
        image = image.resize((40, 40))  
        human_icon = ImageTk.PhotoImage(image)
        
        image = Image.open(self.config_importer.get_company_icon_path())
        image = image.resize((40, 40))  
        company_icon = ImageTk.PhotoImage(image)
        
        if client_match_result.status == SUBSCRIBED:
            self.result_frame = Frame(matching_result_widget, bg="lightgreen", border=1, relief="solid", width=200, height=80, pady=4)
        else:
            self.result_frame = Frame(matching_result_widget, bg="red", border=1, relief="solid", width=200, height=80, pady=4)
            
        domiciliation_agent_label = Label(self.result_frame, text=client_match_result.domiciliation_agent, font=("TkDefaultFont", 12, "bold"), bg=self.result_frame['bg'])
            
        # Première ligne pour la compagnie
        company_frame = Frame(self.result_frame, bg=self.result_frame['bg'])
        company_frame.pack(side=TOP, fill=X)
        
        company_icon_label = Label(company_frame, image=None, bg=company_frame['bg'])
        company_icon_label.image = company_icon
        company_icon_label.configure(image=company_icon)
        company_icon_label.pack(side=LEFT)
        
        company_name_label = Label(company_frame, text=client_match_result.matching_company , font=("TkDefaultFont", 12, "bold"), bg=company_frame['bg'], wraplength=120)
        company_name_label.pack(side=LEFT)
        
        company_correspondance_rate_label = Label(company_frame, text=str(client_match_result.company_match_ratio) + "%", font=("Times", 14, "italic bold"), bg=company_frame['bg'])
        company_correspondance_rate_label.pack(side=RIGHT)
        
        # Deuxième ligne pour la personne
        person_frame = Frame(self.result_frame, bg=self.result_frame['bg'])
        person_frame.pack(side=BOTTOM, fill=X)
        
        person_icon_label = Label(person_frame, image=None, bg=person_frame['bg'])
        person_icon_label.image = human_icon
        person_icon_label.configure(image=human_icon)
        person_icon_label.pack(side=LEFT)
        
        person_name_label = Label(person_frame, text=client_match_result.matching_person, font=("TkDefaultFont", 12, "bold"), bg=person_frame['bg'], wraplength=120)
        person_name_label.pack(side=LEFT)
        
        person_correspondance_rate_label = Label(person_frame, text=str(client_match_result.person_match_ratio) + "%", font=("Times", 14, "italic bold"), bg=person_frame['bg'])
        person_correspondance_rate_label.pack(side=RIGHT)
