from text_processor.text_cleaner import TextCleaner
from text_processor.text_constants import *
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
    text_cleaner.text_to_clean ="my first line\nAnother line containing a date 20/10/1980"
    cleaned_text = text_cleaner.clean_text() 
    assert len(cleaned_text) == 1
    assert cleaned_text[0] == "my first line"
    
    
def test_can_find_a_bracket_in_a_string():
    assert text_cleaner.contains_a_bracket("This line doesn't contain a bracket") == False
    assert text_cleaner.contains_a_bracket("This line contains a bracket [") == True    


def test_removes_lines_containing_brackets():
    text_cleaner.text_to_clean ="my first line\nAnother line containing a bracket ["
    cleaned_text = text_cleaner.clean_text() 
    assert len(cleaned_text) == 1
    assert cleaned_text[0] == "my first line"
    text_cleaner.text_to_clean = "bracket ["
    cleaned_text = text_cleaner.clean_text()
    assert len(cleaned_text) == 0


def test_can_find_a_sequence_of_digits():
    assert text_cleaner.contains_a_sequence_of_digits("This line doesn't contain a series of consecutive numbers") == False
    assert text_cleaner.contains_a_sequence_of_digits("26/05/1980") == False
    assert text_cleaner.contains_a_sequence_of_digits("123456789") == True
    assert text_cleaner.contains_a_sequence_of_digits("This line contains a series of consecutive numbers 123456789") == True
    
    
def test_removes_lines_containing_a_sequence_of_digits():
    text_cleaner.text_to_clean ="my first line\nAnother line containing a series of consecutive numbers 123456789"
    cleaned_text = text_cleaner.clean_text()
    assert len(cleaned_text) == 1
    assert cleaned_text[0] == "my first line"
    text_cleaner.text_to_clean = "123456789"
    cleaned_text = text_cleaner.clean_text()
    assert len(cleaned_text) == 0
    
    
def test_can_find_a_valid_line():
    line_with_three_chars = "abc"
    assert text_cleaner.is_valid_line("This line is valid") == True
    assert text_cleaner.is_valid_line("This line contains a date 26/05/1980") == False
    assert text_cleaner.is_valid_line("This line contains a series of consecutive streak of digits 123456789") == False
    assert text_cleaner.is_valid_line("This line contains a bracket [") == False
    assert text_cleaner.is_valid_line("This line contains a bracket [26/05/1980]") == False
    assert text_cleaner.is_valid_line("") == False
    assert text_cleaner.is_valid_line(" ") == False
    assert text_cleaner.is_valid_line(line_with_three_chars) == True
    
    
def test_removes_invalid_lines():
    text_cleaner.text_to_clean ="my first line\nAnother line containing a series of consecutive numbers 123456789\nThis line contains a bracket [\n1\na"
    cleaned_text = text_cleaner.clean_text()
    assert len(cleaned_text) == 1
    assert cleaned_text[0] == "my first line"
    
    
def test_removes_legal_status():
    assert text_cleaner.remove_legal_status("My company SARL SAS SASU EURL SCI SNC EI EIRL") == "My company"
    
    
def test_doesnt_mistake_names_with_legal_status():
    assert text_cleaner.remove_legal_status("totosarl sarl") == "totosarl"
    
    
def test_can_find_a_line_contains_a_banned_word():
    assert text_cleaner.contains_a_banned_word("This line doesn't contain a banned word") == False
    for word in BANNED_WORDS_LIST:
        assert text_cleaner.contains_a_banned_word(word) == True

        
def test_removes_lines_containing_banned_words():
    for index in range(len(BANNED_WORDS_LIST)):
        text_cleaner.text_to_clean ="my first line\n" + BANNED_WORDS_LIST[index]
        cleaned_text = text_cleaner.clean_text()
        assert len(cleaned_text) == 1
        assert cleaned_text[0] == "my first line"
        
    
    
def test_return_modified_et_lines():
    assert text_cleaner.replace_ampersand_by_et("This line contains an &") == "This line contains an et"
    
    
def test_add_a_modified_et_line_if_contains_ampersand():
    text_cleaner.text_to_clean ="my first line\nAnother line containing an &"
    cleaned_text = text_cleaner.clean_text()
    assert len(cleaned_text) == 3
    assert cleaned_text[0] == "my first line"
    assert cleaned_text[1] == "another line containing an &"
    assert cleaned_text[2] == "another line containing an et"
    
    
def test_remove_bordeaux_line():
    text_cleaner.text_to_clean ="my first line\n33000 Bordeaux"
    cleaned_text = text_cleaner.clean_text()
    assert len(cleaned_text) == 1
    assert cleaned_text[0] == "my first line"


def test_remove_rue_de_conde_line():
    text_cleaner.text_to_clean ="my first line\n9 rue de conde"
    cleaned_text = text_cleaner.clean_text()
    assert len(cleaned_text) == 1
    assert cleaned_text[0] == "my first line"


def test_remove_the_adress():
    text_cleaner.text_to_clean ="my first line\n9 rue de conde\n33000 Bordeaux"
    cleaned_text = text_cleaner.clean_text()
    assert len(cleaned_text) == 1
    assert cleaned_text[0] == "my first line"
    

def test_remove_caps_lock_adress():
    text_cleaner.text_to_clean ="my first line\n9 RUE DE CONDE\n33000 BORDEAUX"
    cleaned_text = text_cleaner.clean_text()
    assert len(cleaned_text) == 1
    assert cleaned_text[0] == "my first line"
    
    
def test_remove_france_but_not_company_name_with_france():
    text_cleaner.text_to_clean ="my first line\n9 RUE DE CONDE\n33000 BORDEAUX\nMy company France"
    cleaned_text = text_cleaner.clean_text()
    assert len(cleaned_text) == 2
    assert cleaned_text[0] == "my first line"
    assert cleaned_text[1] == "my company france"
    text_cleaner.text_to_clean = "Les compagnons de France \n 9 RUE DE CONDE\n33000 BORDEAUX\n France"
    cleaned_text = text_cleaner.clean_text()
    assert len(cleaned_text) == 1
    assert cleaned_text[0] == "les compagnons de france"