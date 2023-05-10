from fuzzywuzzy import fuzz
from match_processor.matching_result import MatchingResult
from text_processor.text_cleaner import TextCleaner
from csv_processor.csv_constants import *

class MatchAnalyser:
    
    def __init__(self, clients_data_dictionary):
        self.text_cleaner = TextCleaner()
        self.clients_data_dictionary = clients_data_dictionary
    
    
    def get_best_absolute_match_ratio(self,line,searched_string):
        return max([fuzz.ratio(line, searched_string),fuzz.partial_ratio(line, searched_string),fuzz.token_sort_ratio(line, searched_string),fuzz.token_set_ratio(line, searched_string)])
    
    
    def get_match_ratio(self,line,searched_string):
        return fuzz.ratio(line, searched_string)
    
    
    def get_match_ratio_for_names(self,line,searched_string):
        return max([fuzz.token_set_ratio(line, searched_string),fuzz.token_sort_ratio(line, searched_string)])
    
    
    def get_match_ratio_for_company_names(self,line,company_name):
        if len(line.split()) > 1 and len(company_name) > 2:
            return max([fuzz.ratio(line, company_name),fuzz.partial_ratio(line, company_name)])
        return self.get_match_ratio(line,company_name)
    
    
    def get_average_match_ratio(self,line,searched_string):
        return int((self.get_match_ratio(line,searched_string) + self.get_match_ratio_for_names(line,searched_string)) / 2)
    
    
    def return_the_top_three_matches_for_a_line(self,line):
        result_list = self.add_matching_company_names_to_result_list([], line)
        result_list.sort(key=lambda x: x.correspondance_ratio, reverse=True)
        if result_list == [] or result_list[0].correspondance_ratio <= 90:
            result_list = self.add_matching_directors_names_to_result_list(result_list, line)
            result_list.sort(key=lambda x: x.correspondance_ratio, reverse=True)
        return result_list[:3]
    
    
    def add_matching_company_names_to_result_list(self, result_list, line):
        all_research_fields_for_company = [self.clients_data_dictionary[COMPANY_NAME],self.clients_data_dictionary[TRADEMARK_NAME]]
        for research_field in all_research_fields_for_company:
            for index in range(len(research_field)):
                company_name = str(research_field[index]).lower().strip()
                company_name = self.text_cleaner.remove_legal_status(company_name)
                correspondance_ratio = self.get_match_ratio_for_company_names(line,company_name)
                if (correspondance_ratio > THRESHOLD):
                    matching_result = MatchingResult(company_name, correspondance_ratio, self.clients_data_dictionary[STATUS][index])
                    result_list.append(matching_result)
        return result_list


    def add_matching_directors_names_to_result_list(self, result_list, line):
        all_research_fields_for_directors = [self.clients_data_dictionary[DIRECTOR_NAME],self.clients_data_dictionary[LEGAL_REPRESENTATIVE]]
        for research_field in all_research_fields_for_directors:
            for index in range(len(research_field)):
                director_name = str(research_field[index]).lower().strip()
                correspondance_ratio = self.get_match_ratio_for_names(line,director_name)
                if (correspondance_ratio > THRESHOLD):
                    matching_result = MatchingResult(director_name, correspondance_ratio, self.clients_data_dictionary[STATUS][index])
                    result_list.append(matching_result)
        return result_list