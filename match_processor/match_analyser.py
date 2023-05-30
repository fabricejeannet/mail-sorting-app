from fuzzywuzzy import fuzz
from match_processor.matching_result import MatchingResult
from text_processor.text_cleaner import TextCleaner
from csv_processor.csv_constants import *
from config_processor.config_importer import ConfigImporter

class MatchAnalyser:
    
    def __init__(self, clients_data_dictionary):
        self.text_cleaner = TextCleaner()
        self.clients_data_dictionary = clients_data_dictionary
        self.config_importer = ConfigImporter()
        self.threshold = self.config_importer.get_image_minimum_threshold()
    
    
    def get_match_ratio(self,line,searched_string):
        return fuzz.ratio(line, searched_string)
    
    
    def get_match_ratio_for_names(self,line,searched_string):
        return max([fuzz.token_set_ratio(line, searched_string),fuzz.token_sort_ratio(line, searched_string)])
    
    
    def get_match_ratio_for_company_names(self,line,company_name):
        if len(line.split()) > 1 and len(company_name) > 2:
            return max([fuzz.ratio(line, company_name),fuzz.partial_ratio(line, company_name)])
        return self.get_match_ratio(line,company_name)
    
    
    def get_average_match_ratio(self,line,searched_string):
        return int((self.get_match_ratio(line,searched_string) + fuzz.partial_ratio(line,searched_string) ) / 2)
    
    
    def return_the_top_three_matches_for_a_line(self, line):
        result_list = self.get_matching_companies(line)
        result_list.sort(key=lambda x: x.match_ratio, reverse=True)
        if result_list == [] or result_list[0].match_ratio < 90:
            result_list += self.get_matching_directors_names(line)
            result_list.sort(key=lambda x: x.match_ratio, reverse=True)
        return result_list[:3]
    
    
    def get_matching_companies(self, line):
        
        match_list = []
        companies = self.clients_data_dictionary[COMPANY_NAME]
        trade_marks = self.clients_data_dictionary[TRADEMARK_NAME]
        index = 0
        while ( index < len(companies)):
            company_name = self.text_cleaner.clean_text_without_checking_validity(str(companies[index]))
            trade_mark = self.text_cleaner.clean_text_without_checking_validity(str(trade_marks[index]))
            
            company_name_match_ratio = self.get_average_match_ratio(line,company_name)
            trade_mark_match_ratio = self.get_average_match_ratio(line,trade_mark)
            
            if (company_name_match_ratio > self.threshold):         
                match_list.append(MatchingResult(company_name, company_name_match_ratio, self.clients_data_dictionary[STATUS][index], self.clients_data_dictionary[ID][index]))
            elif (trade_mark_match_ratio > self.threshold):
                match_list.append(MatchingResult(trade_mark, trade_mark_match_ratio, self.clients_data_dictionary[STATUS][index], self.clients_data_dictionary[ID][index]))

            index += 1
            
        return match_list


    def get_matching_directors_names(self, line):
        match_list = []
        director_names = self.clients_data_dictionary[DIRECTOR_NAME]
        legal_representatives = self.clients_data_dictionary[LEGAL_REPRESENTATIVE]
        index = 0
        while (index < len(director_names)):
            director_name = self.text_cleaner.clean_text_without_checking_validity(str(director_names[index]))
            legal_representative = self.text_cleaner.clean_text_without_checking_validity(str(legal_representatives[index]))
            
            director_name_match_ratio = self.get_match_ratio_for_names(line,director_name)
            legal_representative_match_ratio = self.get_match_ratio_for_names(line,legal_representative)
            
            if (director_name_match_ratio > self.threshold):         
                match_list.append(MatchingResult(director_name, director_name_match_ratio, self.clients_data_dictionary[STATUS][index], self.clients_data_dictionary[ID][index]))
            elif (legal_representative_match_ratio > self.threshold):
                match_list.append(MatchingResult(legal_representative, legal_representative_match_ratio, self.clients_data_dictionary[STATUS][index], self.clients_data_dictionary[ID][index]))
                
            index += 1
        return match_list