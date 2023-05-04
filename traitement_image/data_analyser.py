from csv_importer import CsvManager
from fuzzywuzzy import fuzz
from tkinter import END
from csv_constants import *
from matching_result import MatchingResult

class DataAnalyser:
    
    def __init__(self, clients_data_dictionnary):
        self.clients_data_dictionnary = clients_data_dictionnary
        
        
    def return_the_top_three_matches_for_a_line(self, line):
        results = []

        for index in range(len(self.clients_data_dictionnary[RAISON_SOCIALE])):
            company_name = self.clients_data_dictionnary[RAISON_SOCIALE][index].lower()
            correspondance_rate = max(fuzz.ratio(line,company_name), fuzz.partial_ratio(line,company_name))
            if (correspondance_rate > THRESHOLD):
                matching_result = MatchingResult(company_name, correspondance_rate, self.clients_data_dictionnary[STATUT][index])
                results.append(matching_result)
        results.sort(key=lambda x: x.correspondance_rate, reverse=True)
        results = results[:3]
        return results
    
   
   
   
   
   
   
   
   
   
    # def return_the_top_three_matches_for_a_line(self, line):
    #     results = {}
    #     results["searched_line"] = line
    #     results["matching_name"] = ["","",""]
    #     results["statut"] = ["","",""]
    #     results["correspondance_rate"] = [0,0,0]
    #     results["id"] = [0,0,0]
    #     clients_data_dictionnary = self.clients_data_list
    #     for i in range(len(clients_data_dictionnary["raison_sociale"])):
    #         company_name = clients_data_dictionnary["raison_sociale"][i].lower()
    #         statut = clients_data_dictionnary["statut"][i]
    #         correspondance_rate = max(fuzz.ratio(line,company_name), fuzz.partial_ratio(line,company_name))
    #         for i in range(3):
    #             if(results["correspondance_rate"][i] < correspondance_rate and correspondance_rate >= 50):
    #                 results["correspondance_rate"].pop(2)
    #                 results["statut"].pop(2)
    #                 results["matching_name"].pop(2)
    #                 results["statut"].insert(i, statut)
    #                 results["matching_name"].insert(i, company_name)
    #                 results["correspondance_rate"].insert(i, correspondance_rate)
    #                 break
    #     if (results["correspondance_rate"][0] < 90):
    #         for i in range(len(clients_data_dictionnary["director_names"])):
    #             director_name = clients_data_dictionnary["director_names"][i].lower()
    #             statut = clients_data_dictionnary["statut"][i]
    #             correspondance_rate = max(fuzz.ratio(line,director_name), fuzz.partial_ratio(line,director_name))
    #             for i in range(3):
    #                 if(results["correspondance_rate"][i] < correspondance_rate and correspondance_rate >= 50):
    #                     results["correspondance_rate"].pop(2)
    #                     results["statut"].pop(2)
    #                     results["matching_name"].pop(2)
    #                     results["statut"].insert(i, statut)
    #                     results["matching_name"].insert(i, director_name)
    #                     results["correspondance_rate"].insert(i, correspondance_rate)
    #                     break
    #     if (results["correspondance_rate"][0] < 95):
    #         for index in range(len(clients_data_dictionnary["marque_commerciale"])):
    #             trademark_name = str(clients_data_dictionnary["marque_commerciale"][index]).lower()
    #             statut = clients_data_dictionnary["statut"][index]
    #             correspondance_rate = max(fuzz.ratio(line,trademark_name), fuzz.partial_ratio(line,trademark_name))
    #             for sort_index in range(3):
    #                 if(results["correspondance_rate"][sort_index] < correspondance_rate and correspondance_rate >= 50):
    #                     results["correspondance_rate"].pop(2)
    #                     results["statut"].pop(2)
    #                     results["matching_name"].pop(2)
    #                     results["statut"].insert(sort_index, statut)
    #                     results["matching_name"].insert(sort_index, trademark_name)
    #                     results["correspondance_rate"].insert(sort_index, correspondance_rate)
    #                     break
    #     return results
   
   
   
    def display_results(self, matching_results):
        for index in range(len(matching_results["matching_name"])):
            print("Matching name: " + matching_results["matching_name"][index] + " - Statut: " + matching_results["statut"][index] + " - Correspondance rate: " + str(matching_results["correspondance_rate"][index]))
            
