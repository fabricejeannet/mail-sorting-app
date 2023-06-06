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

    
def test_can_find_a_bracket_in_a_string():
    assert text_cleaner.contains_a_bracket("This line doesn't contain a bracket") == False
    assert text_cleaner.contains_a_bracket("This line contains a bracket [") == True    


def test_can_find_a_sequence_of_digits():
    assert text_cleaner.contains_a_sequence_of_digits("This line doesn't contain a series of consecutive numbers") == False
    assert text_cleaner.contains_a_sequence_of_digits("26/05/1980") == False
    assert text_cleaner.contains_a_sequence_of_digits("123456789") == True
    assert text_cleaner.contains_a_sequence_of_digits("This line contains a series of consecutive numbers 123456789") == True
    
    
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
    cleaned_text = text_cleaner.clean_text("my first line")
    assert len(cleaned_text) != 0   
    assert cleaned_text == "my first line"
    cleaned_text = text_cleaner.clean_text("this line contains a date 26/05/1980")
    assert len(cleaned_text) == 0
    cleaned_text = text_cleaner.clean_text("this line contains a series of consecutive streak of digits 123456789")
    assert len(cleaned_text) == 0
    cleaned_text = text_cleaner.clean_text("this line contains a bracket [")
    assert len(cleaned_text) == 0
    cleaned_text = text_cleaner.clean_text("this line contains a bracket [26/05/1980]")
    assert len(cleaned_text) == 0
    cleaned_text = text_cleaner.clean_text("")
    assert len(cleaned_text) == 0
    cleaned_text = text_cleaner.clean_text(" ")
    assert len(cleaned_text) == 0
    
    
def test_remove_full_legal_status_and_points():
    assert text_cleaner.remove_legal_status("My company S.A.R.L. S.A.S. S.A.S.U. E.U.R.L. S.C.I. S.N.C. E.I. E.I.R.L.") == "My company"
    
    
def test_removes_legal_status():
    assert text_cleaner.remove_legal_status("My company SARL SAS SASU EURL SCI SNC EI EIRL") == "My company"
    

def test_removes_legal_status_and_points():
    assert text_cleaner.remove_legal_status("My company SARL. SAS. SASU. EURL. SCI. SNC. EI. EIRL.") == "My company"
    
    
def test_dont_remove_legal_status_in_words():
    assert text_cleaner.remove_legal_status("My company sarla sasla sasula eurla scila sncla eila eirla") == "My company sarla sasla sasula eurla scila sncla eila eirla"


def test_remove_gender_markers():
    assert text_cleaner.remove_gender_markers("My company m. mme. mme m mr mr.") == "My company"
    assert text_cleaner.remove_gender_markers("My company monsieur madame") == "My company"
    
    
def test_doesnt_mistake_names_with_legal_status():
    assert text_cleaner.remove_legal_status("totosarl sarl") == "totosarl"
    
    
def test_can_find_a_line_contains_a_banned_word():
    assert text_cleaner.contains_a_banned_word("This line doesn't contain a banned word") == False
    for word in BANNED_WORDS_LIST:
        assert text_cleaner.contains_a_banned_word(word) == True

        
def test_removes_lines_containing_banned_words():
    for index in range(len(BANNED_WORDS_LIST)):
        cleaned_text = text_cleaner.clean_text(BANNED_WORDS_LIST[index])
        assert len(cleaned_text) == 0
                
    
def test_remove_bordeaux_line():
    cleaned_text = text_cleaner.clean_text("33000 Bordeaux")
    assert len(cleaned_text) == 0


def test_remove_rue_de_conde_line():
    cleaned_text = text_cleaner.clean_text("9 rue de conde")
    assert len(cleaned_text) == 0
    

def test_remove_caps_lock_adress():
    cleaned_text = text_cleaner.clean_text("33000 BORDEAUX")
    assert len(cleaned_text) == 0    
    
    
def test_remove_france_but_not_company_name_with_france():
    cleaned_text = text_cleaner.clean_text("My company France")
    assert len(cleaned_text) != 0
    cleaned_text = text_cleaner.clean_text("France")
    assert len(cleaned_text) == 0


def test_remove_duplicated_lines():
    unique_lines = text_cleaner.remove_duplicated_lines_from_list(["My company", "My company", "My company"])
    assert len(unique_lines) == 1
    assert unique_lines[0] == "My company"
    unique_lines = text_cleaner.remove_duplicated_lines_from_list(["My company", "My company", "My company", "My company"])
    assert len(unique_lines) == 1
    assert unique_lines[0] == "My company"
    unique_lines = text_cleaner.remove_duplicated_lines_from_list(["My company"])
    assert len(unique_lines) == 1
    assert unique_lines[0] == "My company"
    