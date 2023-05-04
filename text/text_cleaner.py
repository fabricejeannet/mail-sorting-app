import re

class TextCleaner:

    def __init__(self):
        self.text_to_clean = ""
        self.REGEX_DATE = r"\b(0?[1-9]|[12][0-9]|3[01])[./-](0?[1-9]|1[0-2])[./-](\d{2}|\d{4})\b"
        self.REGEX_BRACKET = r"\[|\]"
        self.REGEX_CONSECUTIVE_NUMBERS = r'\d\s*\d\s*\d\s*\d\s*\d\s*\d(?:\s*\d)*'
        self.REGEX_SAS = r'\b[sS]?[.]?[aA]?[.]?[sS]?[.]?\b'
        self.REGEX_SARL = r'\b[sS]?[.]?[aA]?[.]?[rR]?[.]?[lL]?[.]?\b'
        self.REGEX_SASU = r'\b[sS]?[.]?[aA]?[.]?[sS]?[.]?[uU]?\b'
        self.REGEX_EURL = r'\b[eE]?[.]?[uU]?[.]?[rR]?[.]?[lL]?\b'
        self.REGEX_SCI = r'\b[sS]?[.]?[cC]?[.]?[iI]?\b'
        self.REGEX_SNC = r'\b[sS]?[.]?[nN]?[.]?[cC]?\b'
        self.REGEX_EI = r'\b[eE]?[.]?[iI]?\b'
        self.REGEX_EIRL = r'\b[eE]?[.]?[iI]?[.]?[rR]?[.]?[lL]?\b'   
        
        
    def contains_a_date(self, line):
        return re.search(self.REGEX_DATE, line) != None
    
    
    def contains_a_bracket(self, line):
        return re.search(self.REGEX_BRACKET,line) != None
    
    
    def contains_a_series_of_consecutive_numbers(self, line):
        return re.search(self.REGEX_CONSECUTIVE_NUMBERS, line) != None
    
    
    def is_valid_line(self, line):
        return not self.contains_a_bracket(line) and not self.contains_a_date(line) and not self.contains_a_series_of_consecutive_numbers(line) and not line.isspace() and not len(line) < 2
    
    
    def clean_text(self):
        clean_line_array = []
        line_array = self.text_to_clean.splitlines()
        for line in line_array:
            line = line.strip()
            if self.is_valid_line(line):
                clean_line_array.append(line)
        return clean_line_array
    
    def remove_sas(self, line):
        return re.sub(self.REGEX_SAS, "", line)
    
    def remove_sarl(self, line):
        return re.sub(self.REGEX_SARL, "", line)
    
    def remove_sasu(self, line):    
        return re.sub(self.REGEX_SASU, "", line)
    
    def remove_eurl(self, line):
        return re.sub(self.REGEX_EURL, "", line)
    
    def remove_sci(self, line):
        return re.sub(self.REGEX_SCI, "", line)
    
    def remove_snc(self, line):
        return re.sub(self.REGEX_SNC, "", line)
    
    def remove_ei(self, line):
        return re.sub(self.REGEX_EI, "", line)
    
    def remove_eirl(self, line):
        return re.sub(self.REGEX_EIRL, "", line)
    
    def remove_legal_status(self, line):
        line = self.remove_sas(line)
        line = self.remove_sarl(line)
        line = self.remove_sasu(line)
        line = self.remove_eurl(line)
        line = self.remove_sci(line)
        line = self.remove_snc(line)
        line = self.remove_ei(line)
        line = self.remove_eirl(line)
        return line.strip()