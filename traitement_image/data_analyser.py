from csv_importer import CsvManager
from fuzzywuzzy import fuzz

class DataAnalyser:
    
    def __init__(self):
        csv_manager = CsvManager()

        csv_manager.open_csv("clients.csv")

        self.clients_data_list = {}
        self.clients_data_list["raison_sociale"] = (csv_manager.get_company_names())
        self.clients_data_list["director_names"] = (csv_manager.get_director_names())
        self.clients_data_list["statut"] = csv_manager.get_subscription_status()
        
    
    def return_the_top_three_matches_for_a_word(self, word):
        results = {}
        results["match"] = ["","",""]
        results["statut"] = ["","",""]
        results["rate"] = [0,0,0]
        dico = self.clients_data_list
        for i in range(len(dico["raison_sociale"])):
            company_name = dico["raison_sociale"][i].lower()
            statut = dico["statut"][i]
            rate = fuzz.ratio(word,company_name)
            for i in range(3):
                if(results["rate"][i] < rate):
                    results["rate"].pop(2)
                    results["statut"].pop(2)
                    results["match"].pop(2)
                    results["statut"].insert(i, statut)
                    results["match"].insert(i, company_name)
                    results["rate"].insert(i, rate)
                    break
        if (results["rate"][0] < 90):
            for i in range(len(dico["director_names"])):
                company_name = dico["director_names"][i].lower()
                statut = dico["statut"][i]
                rate = fuzz.ratio(word,company_name)
                for i in range(3):
                    if(results["rate"][i] < rate):
                        results["rate"].pop(2)
                        results["statut"].pop(2)
                        results["match"].pop(2)
                        results["statut"].insert(i, statut)
                        results["match"].insert(i, company_name)
                        results["rate"].insert(i, rate)
                        break
        print(results)
    