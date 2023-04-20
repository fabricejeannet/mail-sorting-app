from database.csv_importer import CsvManager
from fuzzywuzzy import fuzz

def return_the_top_three_matches_for_a_word(word, dico):
    results = {}
    results["match"] = ["","",""]
    results["statut"] = ["","",""]
    results["rate"] = [0,0,0]
    print(len(dico.items()))
    for i in range(len(dico["raison_sociale"])):
        company_name = dico["raison_sociale"][i].lower()
        statut = dico["statut"][i]
        rate = fuzz.partial_ratio(word,company_name)
        for i in range(3):
            if(results["rate"][i] < rate):
                results["statut"][i] = statut
                results["match"][i] = company_name
                results["rate"][i] = rate
                break
    print(results)
    
csv_manager = CsvManager()

csv_manager.open_csv("database/clients.csv")

clients_data_list = {}
clients_data_list["raison_sociale"] = (csv_manager.get_company_names())
clients_data_list["director_names"] = (csv_manager.get_director_names())
clients_data_list["statut"] = csv_manager.get_subscription_status()
return_the_top_three_matches_for_a_word("cottrwood",clients_data_list)