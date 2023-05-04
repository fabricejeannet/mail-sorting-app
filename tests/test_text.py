from text.text_cleaner import TextCleaner
text_cleaner = TextCleaner()

def test_can_find_a_date_in_a_string():
    assert text_cleaner.contains_a_date("Pas de date") == False
    assert text_cleaner.contains_a_date("26/05/1980") == True
    assert text_cleaner.contains_a_date("26/05/80") == True
    assert text_cleaner.contains_a_date("6/05/1980") == True
    assert text_cleaner.contains_a_date("6/5/1980") == True
    assert text_cleaner.contains_a_date("6/1/80") == True
    assert text_cleaner.contains_a_date("16/1/80") == True
    assert text_cleaner.contains_a_date("26/1/1880") == True

def test_removes_lines_containing_dates():
    text_cleaner.text_to_clean ="My first line\nAnother line containing a date 20/10/1980"
    cleaned_text = text_cleaner.clean_text() 
    assert len(cleaned_text) == 1
    assert cleaned_text[0] == "My first line"
    
def test_can_find_a_bracket_in_a_string():
    assert text_cleaner.contains_a_bracket("This line doesn't contain a bracket") == False
    assert text_cleaner.contains_a_bracket("26/05/1980") == False
    assert text_cleaner.contains_a_bracket("[26/05/1980]") == True
    assert text_cleaner.contains_a_bracket("26/05/1980]") == True
    assert text_cleaner.contains_a_bracket("This line contains a bracket [") == True    

def test_removes_lines_containing_brackets():
    text_cleaner.text_to_clean ="My first line\nAnother line containing a bracket ["
    cleaned_text = text_cleaner.clean_text() 
    assert len(cleaned_text) == 1
    assert cleaned_text[0] == "My first line"
    text_cleaner.text_to_clean = "bracket ["
    cleaned_text = text_cleaner.clean_text()
    assert len(cleaned_text) == 0

def test_can_find_a_series_of_consecutive_numbers():
    assert text_cleaner.contains_a_series_of_consecutive_numbers("This line doesn't contain a series of consecutive numbers") == False
    assert text_cleaner.contains_a_series_of_consecutive_numbers("26/05/1980") == False
    assert text_cleaner.contains_a_series_of_consecutive_numbers("123456789") == True
    assert text_cleaner.contains_a_series_of_consecutive_numbers("1234567890") == True
    assert text_cleaner.contains_a_series_of_consecutive_numbers("This line contains a series of consecutive numbers 123456789") == True
    
def test_removes_lines_containing_a_series_of_consecutive_numbers():
    text_cleaner.text_to_clean ="My first line\nAnother line containing a series of consecutive numbers 123456789"
    cleaned_text = text_cleaner.clean_text()
    assert len(cleaned_text) == 1
    assert cleaned_text[0] == "My first line"
    text_cleaner.text_to_clean = "123456789"
    cleaned_text = text_cleaner.clean_text()
    assert len(cleaned_text) == 0
    
def test_can_find_a_valid_line():
    line_with_two_chars = "ab"
    assert text_cleaner.is_valid_line("This line is valid") == True
    assert text_cleaner.is_valid_line("This line contains a date 26/05/1980") == False
    assert text_cleaner.is_valid_line("This line contains a series of consecutive streak of digits 123456789") == False
    assert text_cleaner.is_valid_line("This line contains a bracket [") == False
    assert text_cleaner.is_valid_line("This line contains a bracket [26/05/1980]") == False
    assert text_cleaner.is_valid_line("") == False
    assert text_cleaner.is_valid_line(" ") == False
    assert text_cleaner.is_valid_line(line_with_two_chars) == True
    
def test_removes_invalid_lines():
    text_cleaner.text_to_clean ="My first line\nAnother line containing a series of consecutive numbers 123456789\nThis line contains a bracket [\n1\na"
    cleaned_text = text_cleaner.clean_text()
    assert len(cleaned_text) == 1
    assert cleaned_text[0] == "My first line"
    
def test_removes_legal_status():
    assert text_cleaner.remove_legal_status("SARL") == ""
    assert text_cleaner.remove_legal_status("SAS") == ""
    assert text_cleaner.remove_legal_status("SASU") == ""
    
    
    

