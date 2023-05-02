from csv_importer import CsvManager
from fuzzywuzzy import fuzz
from tkinter import END

class DataAnalyser:
    
    def __init__(self):
        csv_manager = CsvManager()

        csv_manager.load_dataframe_from_csv_file("clients.csv")

        self.clients_data_list = {}
        self.clients_data_list["raison_sociale"] = csv_manager.get_company_names()
        self.clients_data_list["director_names"] = csv_manager.get_director_names()
        self.clients_data_list["id"] = csv_manager.get_ids()
        self.clients_data_list["statut"] = csv_manager.get_subscription_status()
        
        
    def return_the_top_three_matches_for_a_line(self, line):
        results = {}
        results["searched_line"] = line
        results["matching_name"] = ["","",""]
        results["statut"] = ["","",""]
        results["correspondance_rate"] = [0,0,0]
        results["id"] = [0,0,0]
        clients_data_dictionnary = self.clients_data_list
        for i in range(len(clients_data_dictionnary["raison_sociale"])):
            company_name = clients_data_dictionnary["raison_sociale"][i].lower()
            statut = clients_data_dictionnary["statut"][i]
            correspondance_rate = max(fuzz.ratio(line,company_name), fuzz.partial_ratio(line,company_name))
            for i in range(3):
                if(results["correspondance_rate"][i] < correspondance_rate and correspondance_rate >= 50):
                    results["correspondance_rate"].pop(2)
                    results["statut"].pop(2)
                    results["matching_name"].pop(2)
                    results["statut"].insert(i, statut)
                    results["matching_name"].insert(i, company_name)
                    results["correspondance_rate"].insert(i, correspondance_rate)
                    break
        if (results["correspondance_rate"][0] < 90):
            for i in range(len(clients_data_dictionnary["director_names"])):
                director_name = clients_data_dictionnary["director_names"][i].lower()
                statut = clients_data_dictionnary["statut"][i]
                correspondance_rate = max(fuzz.ratio(line,director_name), fuzz.partial_ratio(line,director_name))
                for i in range(3):
                    if(results["correspondance_rate"][i] < correspondance_rate and correspondance_rate >= 50):
                        results["correspondance_rate"].pop(2)
                        results["statut"].pop(2)
                        results["matching_name"].pop(2)
                        results["statut"].insert(i, statut)
                        results["matching_name"].insert(i, director_name)
                        results["correspondance_rate"].insert(i, correspondance_rate)
                        break
        return results
    
    def display_results(self, matching_results):
        for index in range(len(matching_results["matching_name"])):
            print("Matching name: " + matching_results["matching_name"][index] + " - Statut: " + matching_results["statut"][index] + " - Correspondance rate: " + str(matching_results["correspondance_rate"][index]))
            
