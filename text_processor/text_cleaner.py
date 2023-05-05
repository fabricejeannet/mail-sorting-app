import re
from fuzzywuzzy import fuzz
from text_processor.text_constants import *

class TextCleaner:

    def __init__(self):
        self.text_to_clean = ""   
        
        
    def contains_a_date(self, line):
        return re.search(REGEX_DATE, line) != None
    
    
    def contains_a_bracket(self, line):
        return re.search(REGEX_BRACKET,line) != None
    
    
    def contains_a_sequence_of_digits(self, line):
        return re.search(REGEX_CONSECUTIVE_NUMBERS, line) != None
    
    
    def is_valid_line(self, line):
        return not self.contains_a_bracket(line) \
        and not self.contains_a_date(line) \
        and not self.contains_a_sequence_of_digits(line) \
        and not line.isspace() \
        and not len(line) < 2 \
        and not self.contains_a_banned_word(line)
    
    
    def contains_a_banned_word(self, line):
        banned_word_found = False
        banned_words_index = 0
        while not banned_word_found and banned_words_index < len(BANNED_WORDS_LIST):
            banned_word_found = max(fuzz.partial_ratio(line,BANNED_WORDS_LIST[banned_words_index]),fuzz.ratio(line, BANNED_WORDS_LIST[banned_words_index])) >= 90
            banned_words_index += 1
        return banned_word_found
    
    
    def clean_text(self):
        clean_line_array = []
        line_array = self.text_to_clean.splitlines()
        for line in line_array:
            line = line.strip()
            if self.is_valid_line(line):
                clean_line_array.append(line)
                if '&' in line:
                    clean_line_array.append(self.replace_ampersand_by_et(line))
        return clean_line_array
    
    
    def remove_legal_status(self, line):
        for legal_status in LEGAL_STATUS:
            line = re.sub(legal_status, "", line)            
        return line.strip()
    
    def replace_ampersand_by_et(self, line):
        return line.replace("&", "et")
