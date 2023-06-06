from fuzzywuzzy import fuzz
from match_processor.matching_result import MatchingResult
from text_processor.text_cleaner import TextCleaner
from csv_processor.csv_constants import *
from config_processor.config_importer import ConfigImporter
import logging

class MatchAnalyser:
    
    def __init__(self, clients_data_dictionary):
        self.text_cleaner = TextCleaner()
        self.clients_data_dictionary = clients_data_dictionary
        self.config_importer = ConfigImporter()
        self.threshold = self.config_importer.get_image_minimum_threshold()
        self.result_dictionnary = {}
    
    
    def reset_match_results(self):
        self.result_dictionnary = {}
        
    
    def get_match_ratio(self,line,searched_string):
        return fuzz.ratio(line, searched_string)
    
    
    def get_match_ratio_for_names(self,line,searched_string):
        return int((fuzz.token_set_ratio(line, searched_string) + fuzz.token_sort_ratio(line, searched_string))/2)
        
    
    def get_average_match_ratio(self,line,searched_string):
        return int((self.get_match_ratio(line,searched_string) + fuzz.partial_ratio(line,searched_string) + fuzz.token_set_ratio(line,searched_string)*2) / 4)
    
    
    def find_the_best_results(self, line):
        self.get_matching_companies(line)
        self.get_matching_directors_names(line)
        self.result_dictionnary = dict(sorted(self.result_dictionnary.items(), key=lambda item: item[1].get_max_match_ratio(), reverse=True))
    
    
    def get_matching_results(self):
        return list(self.result_dictionnary.values())[:5]
    
    
    def get_matching_companies(self, line):
        
        companies = self.clients_data_dictionary[COMPANY_NAME]
        trade_marks = self.clients_data_dictionary[TRADEMARK_NAME]
        index = 0
        
        while ( index < len(companies)):
            
            company_name = self.text_cleaner.clean_text_without_checking_validity(str(companies[index]))
            trade_mark = self.text_cleaner.clean_text_without_checking_validity(str(trade_marks[index]))
            
            company_name_match_ratio = self.get_average_match_ratio(line,company_name)
            trade_mark_match_ratio = self.get_average_match_ratio(line,trade_mark)
            
            client_id = self.clients_data_dictionary[ID][index]
            max_match_ratio = max(company_name_match_ratio, trade_mark_match_ratio)
            
            if max_match_ratio >= self.threshold:

                if client_id not in self.result_dictionnary.keys():
        
                    if company_name_match_ratio > trade_mark_match_ratio: 
                        logging.info("Added company name to result dictionnary")
                        self.result_dictionnary[client_id] = (MatchingResult(matching_company=company_name, company_match_ratio=company_name_match_ratio, status=self.clients_data_dictionary[STATUS][index], client_id=self.clients_data_dictionary[ID][index]))
                    
                    else:
                        logging.info("Added trade mark to result dictionnary")          
                        self.result_dictionnary[client_id] = (MatchingResult(matching_company=trade_mark, company_match_ratio=trade_mark_match_ratio, status=self.clients_data_dictionary[STATUS][index], client_id=self.clients_data_dictionary[ID][index]))
                    
                else:
                    
                    result = MatchingResult(self.result_dictionnary[client_id])
                    if result.company_match_ratio < max_match_ratio:
                        if company_name_match_ratio > trade_mark_match_ratio: 
                            result.company_match_ratio = company_name_match_ratio
                            result.matching_company = company_name

                        else:
                            result.company_match_ratio = trade_mark_match_ratio
                            result.matching_company = trade_mark
                        
            index += 1
        logging.info("Dictionary of results after matching companies: " + str(self.result_dictionnary))
            

    def get_matching_directors_names(self, line):

        director_names = self.clients_data_dictionary[DIRECTOR_NAME]
        legal_representatives = self.clients_data_dictionary[LEGAL_REPRESENTATIVE]
        index = 0
        
        while (index < len(director_names)):
            
            director_name = self.text_cleaner.clean_text_without_checking_validity(str(director_names[index]))
            legal_representative = self.text_cleaner.clean_text_without_checking_validity(str(legal_representatives[index]))
            
            director_name_match_ratio = self.get_match_ratio_for_names(line,director_name)
            legal_representative_match_ratio = self.get_match_ratio_for_names(line,legal_representative)
            
            client_id = self.clients_data_dictionary[ID][index]
            max_match_ratio = max(director_name_match_ratio, legal_representative_match_ratio)

            if max_match_ratio > self.threshold:
            
                if client_id not in self.result_dictionnary.keys():
                    
                    if director_name_match_ratio > legal_representative_match_ratio: 
                        logging.info("Added director name with match ratio: " + str(director_name_match_ratio) + "and client id: " + str(client_id))
                        self.result_dictionnary[client_id] = (MatchingResult(matching_person=director_name, person_match_ratio=director_name_match_ratio, status=self.clients_data_dictionary[STATUS][index], client_id=self.clients_data_dictionary[ID][index]))
                    
                    else:
                        logging.info("Added legal representative with match ratio: " + str(legal_representative_match_ratio) + "and client id: " + str(client_id))
                        self.result_dictionnary[client_id] = (MatchingResult(matching_person=legal_representative, person_match_ratio=legal_representative_match_ratio, status=self.clients_data_dictionary[STATUS][index], client_id=self.clients_data_dictionary[ID][index]))
                    
                else:
                    
                    result = MatchingResult(self.result_dictionnary[client_id])
                    if result.person_match_ratio < max_match_ratio:
            
                        if director_name_match_ratio > legal_representative_match_ratio: 
                            result.person_match_ratio = director_name_match_ratio
                            result.matching_person = director_name

                        else:
                            result.person_match_ratio = legal_representative_match_ratio
                            result.matching_person = legal_representative
            
            index += 1
        logging.info("Dictionary of results after matching directors: " + str(self.result_dictionnary))
