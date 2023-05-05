import pytest
from text_extractor import TextExtractor
from fuzzywuzzy import fuzz


text_extractor = TextExtractor()
file_names = ["env1","env2","env4","env5","env6","env7"]
company_names = ["XALES FORMATIONS","la maison du japon",  "ferbat", "l'atelier d'haritza", "Art de poser","ma vie pratique"]
cleaned_text = [[["xales formations"]], [["la maison du japon"]],[["s.a.s. ferbat"]],[["l'atelier d'haritza"]],[["monsieur mehdi belhachemi"],["art de poser"]], [["ma vie pratique - olivia licoys"]]]


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
    assert text_extractor.line_is_valid(line) == True
    
def test_line_is_deleted_if_contains_braquet():
    line = "this is [ invalid]\n this is valid"
    assert text_extractor.clean_text_output_lines(line)[0] == "this is valid"
    
def test_line_

def test_check_if_line_is_valid_reject_on_empty_line():
    line = ""
    assert text_extractor.line_is_valid(line) == False
    
def test_ckeck_if_line_is_valid_reject_on_line_with_only_spaces():
    line = "    "
    assert text_extractor.line_is_valid(line) == False

def test_check_if_line_is_valid_rejects_line_with_only_numbers():
    line = "123456"
    assert text_extractor.line_is_valid(line) == False
    
def test_check_if_line_is_valid_reject_on_line_with_date():
    line = "This line is invalid 12/12/2012"
    assert text_extractor.line_is_valid(line) == False
    
def test_check_if_line_is_valid_reject_on_line_containing_braquet():
    line = "This line is invalid ["
    assert text_extractor.line_is_valid(line) == False
    
def test_line_contain_a_banned_word_rejects_line_containing_a_banned_word():
    line = "This line contains a banned word rue de conde"
    assert text_extractor.line_contain_a_banned_word(line) == True
    
def test_line_contain_a_banned_word_accepts_line_not_containing_a_banned_word():
    line = "This line does not contain a banned word"
    assert text_extractor.line_contain_a_banned_word(line) == False
    
def test_return_modified_et_lines_return_modified_line():
    line = "This line contains &"
    assert text_extractor.return_modified_et_lines(line) == "This line contains et"
    
def test_return_the_line_without_legal_status_with_points():
    line = "This line contains s.a.s s.a.r.l s.a.s.u s.a s.c.i s.c s.n.c e.i.r.l e.u.r.l"
    assert text_extractor.return_the_line_without_legal_status(line) == "This line contains"
    
def test_return_the_line_without_legal_status():
    line = "This line contains sas sarl sasu sa sci sc snc eirl eurl"
    assert text_extractor.return_the_line_without_legal_status(line) == "This line contains"
    
def test_return_the_line_without_legal_status_uppercase():
    line = "This line contains SAS SARL SASU SA SCI SC SNC EIRL EURL"
    assert text_extractor.return_the_line_without_legal_status(line) == "This line contains"
    
def test_dont_remove_if_part_of_a_name():
    line = "This line contains pasas ferbat pasarl pasasu pasa pasci pasc pasnc paseirl paseurl"
    assert text_extractor.return_the_line_without_legal_status(line) == "This line contains pasas ferbat pasarl pasasu pasa pasci pasc pasnc paseirl paseurl"