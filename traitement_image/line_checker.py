import re

class LineChecker:
    
    def __init__(self):
        pass
    
    def check_if_there_is_a_date_in_text_line(self, line):
        #Return True if there is a date in the line, False otherwise
        return re.search(r"\b(0?[1-9]|[12][0-9]|3[01])[./-](0?[1-9]|1[0-2])[./-](\d{2}|\d{4})\b",line) != None
    
    def check_if_there_is_a_braquet_in_text_line(self, line):
        #Return True if there is a braquet in the line
        return re.search(r"\[|\]",line) != None
    
    def check_if_the_line_contains_a_sequence_of_numbers(self,line):
        return re.search(r'\d\s*\d\s*\d\s*\d\s*\d\s*\d(?:\s*\d)*', line) != None
    
    def check_if_there_is_empty_line_on_the_top(self, ocr_output):
        #Return True if there is an empty line on the top of the lines
        return ocr_output.splitlines()[0] == ""
    
    def check_if_there_is_empty_line_on_the_bottom(self, ocr_output):
        lines = ocr_output.splitlines()
        #Return True if there is an empty line on the bottom of the lines
        return lines[len(lines)] == ""
    
    def check_if_line_is_valid(self, line):
        return not self.check_if_there_is_a_braquet_in_text_line(line) and not self.check_if_there_is_a_date_in_text_line(line) and not self.check_if_the_line_contains_a_sequence_of_numbers(line)
    