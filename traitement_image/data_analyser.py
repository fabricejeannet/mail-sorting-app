from csv_importer import CsvManager
from fuzzywuzzy import fuzz

class DataAnalyser:
    
    def __init__(self):
        csv_manager = CsvManager()

        csv_manager.load_dataframe_from_csv_file("clients.csv")

        self.clients_data_list = {}
        self.clients_data_list["raison_sociale"] = (csv_manager.get_company_names())
        self.clients_data_list["director_names"] = (csv_manager.get_director_names())
        self.clients_data_list["statut"] = csv_manager.get_subscription_status()
        
        
    def return_the_top_three_matching_namees_for_a_line(self, line):
        results = {}
        results["matching_name"] = ["","",""]
        results["statut"] = ["","",""]
        results["correspondance_rate"] = [0,0,0]
        clients_data_dictionnary = self.clients_data_list
        for i in range(len(clients_data_dictionnary["raison_sociale"])):
            company_name = clients_data_dictionnary["raison_sociale"][i].lower()
            statut = clients_data_dictionnary["statut"][i]
            correspondance_rate = max(fuzz.ratio(line,company_name), fuzz.partial_ratio(line,company_name))
            for i in range(3):
                if(results["correspondance_rate"][i] < correspondance_rate):
                    results["correspondance_rate"].pop(2)
                    results["statut"].pop(2)
                    results["matching_name"].pop(2)
                    results["statut"].insert(i, statut)
                    results["matching_name"].insert(i, company_name)
                    results["correspondance_rate"].insert(i, correspondance_rate)
                    break
        if (results["correspondance_rate"][0] < 90):
            for i in range(len(clients_data_dictionnary["director_names"])):
                company_name = clients_data_dictionnary["director_names"][i].lower()
                statut = clients_data_dictionnary["statut"][i]
                correspondance_rate = max(fuzz.ratio(word,company_name), fuzz.partial_ratio(word,company_name))
                for i in range(3):
                    if(results["correspondance_rate"][i] < correspondance_rate):
                        results["correspondance_rate"].pop(2)
                        results["statut"].pop(2)
                        results["matching_name"].pop(2)
                        results["statut"].insert(i, statut)
                        results["matching_name"].insert(i, company_name)
                        results["correspondance_rate"].insert(i, correspondance_rate)
                        break
        print(results)
    