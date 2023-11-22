from rapidfuzz.fuzz import ratio, token_set_ratio, token_sort_ratio, partial_ratio
from match_processor.matching_result import MatchingResult
from text_processor.text_cleaner import TextCleaner
from config_processor.config_importer import ConfigImporter

class MatchAnalyser:
    
    def __init__(self, clients_data_dictionary):
        self.text_cleaner = TextCleaner()
        self.clients_data_dictionary = clients_data_dictionary
        config_importer = ConfigImporter()
        self.threshold = config_importer.get_image_minimum_threshold()
        self.result_dictionnary = {}
        self.ID = config_importer.get_csv_id_column()
        self.COMPANY_NAME = config_importer.get_csv_company_name_column()
        self.LEGAL_REPRESENTATIVE = config_importer.get_csv_owner_column()
        self.STATUS = config_importer.get_csv_status_column()
        self.DOMICILIATION_AGENT = config_importer.get_csv_domiciliation_agent_column()
        self.TRADEMARK = config_importer.get_csv_trademark_column()
        

    def reset_match_results(self):
        self.result_dictionnary = {}
        

    def get_match_ratio(self, line, searched_string):
        return ratio(line, searched_string)


    def get_match_ratio_for_names(self, line, searched_string):
        return int((token_set_ratio(line, searched_string) + token_sort_ratio(line, searched_string)) / 2)


    def get_average_match_ratio(self, line, searched_string):
        match_ratio = self.get_match_ratio(line, searched_string)
        match_ratio_for_names = self.get_match_ratio_for_names(line, searched_string)
        return int((match_ratio + partial_ratio(line, searched_string) * 2 + match_ratio_for_names * 2) / 5)


    def find_the_best_results(self, line):
        self.get_matching_companies(line)
        self.get_matching_directors_names(line)
        self.result_dictionnary = dict(sorted(self.result_dictionnary.items(), key=lambda item: item[1].get_max_match_ratio(), reverse=True))


    def get_matching_results(self):
        return list(self.result_dictionnary.values())


    def get_matching_companies(self, line):
        companies = self.clients_data_dictionary[self.COMPANY_NAME]
        trademarks = self.clients_data_dictionary[self.TRADEMARK]
        
        clients_names = [companies[i] + ";" + trademarks[i] for i in range(len(companies))]

        #Boucle qui parcourt les noms de chaque clients ainsi que leur trademark
        for index, (company_names) in enumerate(clients_names):
            
            company_names = company_names.split(";")
            cleaned_companies = [self.text_cleaner.clean_text_without_checking_validity(str(company)) for company in company_names]

            max_match_ratio = 0
            #Boucle qui parcourt tous les noms du client
            for company_name in cleaned_companies:
        
                client_id = self.clients_data_dictionary[self.ID][index]
                company_match_ratio = self.get_average_match_ratio(line, company_name)
                
                if company_match_ratio > max_match_ratio:
                    max_match_ratio = company_match_ratio  
                    most_corresponding_name = company_name      

            if max_match_ratio >= self.threshold:
                result = self.result_dictionnary.get(client_id)

                if not result:
                    self.result_dictionnary[client_id] = MatchingResult(matching_company=most_corresponding_name,company_match_ratio=max_match_ratio, status=self.clients_data_dictionary[self.STATUS][index], domiciliation_agent=self.clients_data_dictionary[self.DOMICILIATION_AGENT][index])

                elif not result.company_match_ratio or result.company_match_ratio < max_match_ratio:
                    result.company_match_ratio = max_match_ratio
                    result.matching_company = most_corresponding_name
                        

    def get_matching_directors_names(self, line):
        legal_representatives = self.clients_data_dictionary[self.LEGAL_REPRESENTATIVE]


        #Boucle qui parcoure chaque client
        for index, (client_legal_representatives) in enumerate(legal_representatives):

            client_legal_representatives = client_legal_representatives.split(";")
            cleaned_legal_representatives = [self.text_cleaner.clean_text_without_checking_validity(str(legal_representative)) for legal_representative in client_legal_representatives]

            max_match_ratio = 0

            #Boucle qui parcoure chaque nom possibles du client
            for legal_representative in cleaned_legal_representatives:
                legal_representative_match_ratio = self.get_match_ratio_for_names(line, legal_representative)

                if legal_representative_match_ratio > max_match_ratio:
                    max_match_ratio = legal_representative_match_ratio
                    most_corresponding_name = legal_representative

            client_id = self.clients_data_dictionary[self.ID][index]
       
            if max_match_ratio > self.threshold:
                result = self.result_dictionnary.get(client_id)
                if not result:
                    self.result_dictionnary[client_id] = MatchingResult(matching_person=most_corresponding_name,person_match_ratio=max_match_ratio, status=self.clients_data_dictionary[self.STATUS][index],domiciliation_agent=self.clients_data_dictionary[self.DOMICILIATION_AGENT][index])

                elif not result.person_match_ratio or result.person_match_ratio < max_match_ratio:
                    result.person_match_ratio = max_match_ratio
                    result.matching_person = most_corresponding_name