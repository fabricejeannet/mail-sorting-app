import pytest
from text_extractor import TextExtractor
from fuzzywuzzy import fuzz


text_extractor = TextExtractor()
file_names = ["env1","env2","env4","env5","env6","env7"]
company_names = ["XALES FORMATIONS","la maison du japon",  "ferbat", "l'atelier d'haritza", "Art de poser","ma vie pratique"]
cleaned_text = [[["xales formations"]], [["la maison du japon"]],[["s.a.s. ferbat"]],[["l'atelier d'haritza"]],[["monsieur mehdi belhachemi"],["art de poser"]], [["ma vie pratique - olivia licoys"]]]

def test_recupere_correctement_sur_enveloppe_standard():
    for index in range(len(file_names)):
        extracted_text = text_extractor.analyse_image_silently(file_names[index])
        print(extracted_text)
        assert fuzz.partial_ratio(extracted_text,company_names[index].lower()) > 90

def test_split_text_in_lines_and_remove_empty_ones():
    initial_text = "line1\nline2\n\nline3"
    assert text_extractor.split_text_into_lines_and_remove_empty_ones(initial_text) == ["line1","line2","line3"]
    
def test_check_if_there_is_a_date_in_text_line():
    line = "line1\nline2\n\nline3"
    assert text_extractor.check_if_there_is_a_date_in_text_line(line) == False
    line = "line1\nline2\n\nline3 12/12/2012"
    assert text_extractor.check_if_there_is_a_date_in_text_line(line) == True
    
def test_check_if_there_is_a_braquet_in_text_line():
    line = "line1\nline2\n\nline3"
    assert text_extractor.check_if_there_is_a_braquet_in_text_line(line) == False
    line = "line1\nline2\n\nline3 ["
    assert text_extractor.check_if_there_is_a_braquet_in_text_line(line) == True
    
def test_check_if_the_line_contains_a_sequence_of_numbers():
    line = "line1\nline2\n\nline3"
    assert text_extractor.check_if_the_line_contains_a_sequence_of_numbers(line) == False
    line = "line1\nline2\n\nline3 123456"
    assert text_extractor.check_if_the_line_contains_a_sequence_of_numbers(line) == True
    
def test_check_if_line_is_valid_accept_valid_line():
    line = "This is a valid line"
    assert text_extractor.check_if_line_is_valid(line) == True


def test_check_if_line_is_valid_reject_on_empty_line():
    line = ""
    assert text_extractor.check_if_line_is_valid(line) == False
    
def test_ckeck_if_line_is_valid_reject_on_line_with_only_spaces():
    line = "    "
    assert text_extractor.check_if_line_is_valid(line) == False

def test_check_if_line_is_valid_rejects_line_with_only_numbers():
    line = "123456"
    assert text_extractor.check_if_line_is_valid(line) == False
    
def test_check_if_line_is_valid_reject_on_line_with_date():
    line = "This line is invalid 12/12/2012"
    assert text_extractor.check_if_line_is_valid(line) == False
    
def test_check_if_line_is_valid_reject_on_line_containing_braquet():
    line = "This line is invalid ["
    assert text_extractor.check_if_line_is_valid(line) == False
    
def test_line_contain_a_banned_word_rejects_line_containing_a_banned_word():
    line = "This line contains a banned word rue de conde"
    assert text_extractor.line_contain_a_banned_word(line) == True
    
def test_line_contain_a_banned_word_accepts_line_not_containing_a_banned_word():
    line = "This line does not contain a banned word"
    assert text_extractor.line_contain_a_banned_word(line) == False
    
def test_return_modified_et_lines_return_modified_line():
    line = "This line contains &"
    assert text_extractor.return_modified_et_lines(line) == "This line contains et"