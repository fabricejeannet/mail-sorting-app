from fuzzywuzzy.fuzz import ratio, token_set_ratio, token_sort_ratio, partial_ratio
from match_processor.matching_result import MatchingResult
from text_processor.text_cleaner import TextCleaner
from csv_processor.csv_constants import COMPANY_NAME, ID, STATUS, TRADEMARK_NAME, DIRECTOR_NAME, LEGAL_REPRESENTATIVE
from config_processor.config_importer import ConfigImporter
import logging

class MatchAnalyser:
    
    def __init__(self, clients_data_dictionary):
        self.text_cleaner = TextCleaner()
        self.clients_data_dictionary = clients_data_dictionary
        self.config_importer = ConfigImporter()
        self.threshold = self.config_importer.get_image_minimum_threshold()
        self.result_dictionnary = {}
        self.perfect_match_counter = 0
        

    def reset_match_results(self):
        self.result_dictionnary = {}
        self.perfect_match_counter = 0
        

    def get_match_ratio(self, line, searched_string):
        return ratio(line, searched_string)


    def get_match_ratio_for_names(self, line, searched_string):
        return int((token_set_ratio(line, searched_string) + token_sort_ratio(line, searched_string)) / 2)


    def get_average_match_ratio(self, line, searched_string):
        return int(
            (self.get_match_ratio(line, searched_string) + partial_ratio(line, searched_string) + 2 * token_set_ratio(line, searched_string)) / 4)


    def find_the_best_results(self, line):
        self.get_matching_companies(line)
        self.get_matching_directors_names(line)
        self.result_dictionnary = dict(
            sorted(self.result_dictionnary.items(), key=lambda item: item[1].get_max_match_ratio(), reverse=True))


    def get_matching_results(self):
        return list(self.result_dictionnary.values())[:5]


    def get_matching_companies(self, line):
        
        companies = self.clients_data_dictionary[COMPANY_NAME]
        trade_marks = self.clients_data_dictionary[TRADEMARK_NAME]

        cleaned_companies = (self.text_cleaner.clean_text_without_checking_validity(str(company)) for company in companies)
        cleaned_trade_marks = (self.text_cleaner.clean_text_without_checking_validity(str(trade_mark)) for trade_mark in trade_marks)

        for index, (company_name, trade_mark) in enumerate(zip(cleaned_companies, cleaned_trade_marks)):
            if trade_mark == "nan":
                trade_mark = None
                
            company_name_match_ratio = self.get_average_match_ratio(line, company_name)
            trade_mark_match_ratio = self.get_average_match_ratio(line, trade_mark)

            client_id = self.clients_data_dictionary[ID][index]

            max_match_ratio = max(company_name_match_ratio, trade_mark_match_ratio)
            most_corresponding_name = company_name if company_name_match_ratio > trade_mark_match_ratio else trade_mark

            if max_match_ratio >= self.threshold:
                if max_match_ratio == 100:
                    self.perfect_match_counter += 1

                if client_id not in self.result_dictionnary:
                    self.result_dictionnary[client_id] = MatchingResult(matching_company=most_corresponding_name,
                                                                       company_match_ratio=max_match_ratio,
                                                                       status=self.clients_data_dictionary[STATUS][index])
                else:
                    result = self.result_dictionnary[client_id]
                    if not result.company_match_ratio or result.company_match_ratio < max_match_ratio:
                        
                        result.company_match_ratio = max_match_ratio
                        result.matching_company = most_corresponding_name


    def get_matching_directors_names(self, line):
        
        director_names = self.clients_data_dictionary[DIRECTOR_NAME]
        legal_representatives = self.clients_data_dictionary[LEGAL_REPRESENTATIVE]

        cleaned_director_names = (self.text_cleaner.clean_text_without_checking_validity(str(director_name)) for director_name in director_names)
        cleaned_legal_representatives = (self.text_cleaner.clean_text_without_checking_validity(str(legal_representative)) for legal_representative in legal_representatives)

        for index, (director_name, legal_representative) in enumerate(zip(cleaned_director_names, cleaned_legal_representatives)):
            
            director_name_match_ratio = self.get_match_ratio_for_names(line, director_name)
            legal_representative_match_ratio = self.get_match_ratio_for_names(line, legal_representative)

            client_id = self.clients_data_dictionary[ID][index]

            max_match_ratio = max(director_name_match_ratio, legal_representative_match_ratio)
            most_corresponding_name = director_name if director_name_match_ratio > legal_representative_match_ratio else legal_representative

            if max_match_ratio > self.threshold:
                if client_id not in self.result_dictionnary:
                    self.result_dictionnary[client_id] = MatchingResult(matching_person=most_corresponding_name,
                                                                       person_match_ratio=max_match_ratio,
                                                                       status=self.clients_data_dictionary[STATUS][
                                                                           index])
                else:
                    result = self.result_dictionnary[client_id]
                    if not result.person_match_ratio or result.person_match_ratio < max_match_ratio:
                        
                        result.person_match_ratio = max_match_ratio
                        result.matching_person = most_corresponding_name
