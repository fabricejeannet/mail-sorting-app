import re
from fuzzywuzzy import fuzz
from text_processor.text_constants import *

class TextCleaner:

    def __init__(self):
        pass        
        
    def contains_a_date(self, line):
        return re.search(REGEX_DATE, line) != None
    
    
    def contains_a_bracket(self, line):
        return re.search(REGEX_BRACKET,line) != None
    
    
    def contains_a_sequence_of_digits(self, line):
        return re.search(REGEX_CONSECUTIVE_NUMBERS, line) != None
    
    
    def is_valid_line(self, line):
        return not line.isspace() \
        and not len(line) <= 2 \
        and not self.contains_a_bracket(line) \
        and not self.contains_a_date(line) \
        and not self.contains_a_sequence_of_digits(line) \
        and not self.contains_a_banned_word(line)
    
    
    def contains_a_banned_word(self, line):
        banned_word_found = False
        banned_words_index = 0
        while not banned_word_found and banned_words_index < len(BANNED_WORDS_LIST):
            banned_word_found = int((fuzz.partial_ratio(line,BANNED_WORDS_LIST[banned_words_index]) + fuzz.ratio(line, BANNED_WORDS_LIST[banned_words_index]))/2) >= 90
            
            banned_words_index += 1
        return banned_word_found
    
    
    def clean_text(self, line):
        line = line.strip().lower()
        line = self.remove_legal_status(line)
        line = self.remove_gender_markers(line)
        line = self.replace_ampersand_by_et(line)
        if self.is_valid_line(line):
            return line
        return ""
    
    
    def clean_text_without_checking_validity(self, line):
        line = line.strip().lower()
        line = self.remove_legal_status(line)
        line = self.remove_gender_markers(line)
        line = self.replace_ampersand_by_et(line)
        return line
    
    
    def remove_legal_status(self, line):
        for legal_status in LEGAL_STATUS:
            line = re.sub(legal_status, "", line)    
        return line.strip()
    
    
    def remove_gender_markers(self, line):
        return re.sub(REGEX_GENDER_MARKERS, "", line).strip()
    
    def replace_ampersand_by_et(self, line):
        return line.replace("&", "et")
