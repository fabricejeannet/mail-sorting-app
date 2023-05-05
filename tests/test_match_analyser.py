from match_processor.match_analyser import MatchAnalyser
from csv_processor.csv_constants import *
from csv_processor.csv_manager import CsvManager

def test_get_best_absolute_match_ratio():
    match_analyser = MatchAnalyser(None)
    assert match_analyser.get_best_absolute_match_ratio("hello","hello") == 100
    assert match_analyser.get_best_absolute_match_ratio("hello","hello world") == 100
    assert match_analyser.get_best_absolute_match_ratio("hello","world") <= 50
    assert match_analyser.get_best_absolute_match_ratio("hello","hello world hello") == 100
    assert match_analyser.get_best_absolute_match_ratio("hello world", "world hello") == 100
    

def test_get_match_ratio():
    match_analyser = MatchAnalyser(None)
    assert match_analyser.get_match_ratio("hello","hello") == 100
    assert match_analyser.get_match_ratio("hello","world") <= THRESHOLD, "The threshold is too low"
    

def test_get_match_ratio_for_names():
    match_analyser = MatchAnalyser(None)
    assert match_analyser.get_match_ratio_for_names("Jean Louis","Jean-Louis") == 100
    assert match_analyser.get_match_ratio_for_names("Jean Louis","Jean Louis") == 100
    assert match_analyser.get_match_ratio_for_names("Jean Louis","Jean Louis Dupont") == 100
    assert match_analyser.get_match_ratio_for_names("Jean Louis","Louis Jean") == 100


def test_get_match_ratio_for_company_names():
    match_analyser = MatchAnalyser(None)
    assert match_analyser.get_match_ratio_for_company_names("t d express", "t d express tetd express TETD EXPRESS") > 70
    assert match_analyser.get_match_ratio_for_company_names("cottonwood","cottrwood") > 80
    assert match_analyser.get_match_ratio_for_company_names("hello","world") <= THRESHOLD, "The threshold is too low"
    assert match_analyser.get_match_ratio_for_company_names("emotional damage","em") < 50
    assert match_analyser.get_match_ratio_for_company_names("em","emotional") < 50


def test_get_average_match_ratio():
    match_analyser = MatchAnalyser(None)
    assert match_analyser.get_average_match_ratio("hello","hello") == 100
    assert match_analyser.get_average_match_ratio("t d express", "t d express tetd express TETD EXPRESS") > 70
    assert match_analyser.get_average_match_ratio("cottonwood","cottrwood") > 80
    assert match_analyser.get_average_match_ratio("hello","world") <= THRESHOLD, "The threshold is too low"
    assert match_analyser.get_average_match_ratio("em","emotional damage") < 50
    assert match_analyser.get_average_match_ratio("em","emotional") < 50
    
    
def test_return_the_top_three_matches_for_a_line():
    csv_manager = CsvManager()
    csv_manager.open_csv_file("tests/test.csv")
    mock_clients = csv_manager.get_clients_data_dictionnary()
    match_analyser = MatchAnalyser(mock_clients)
    results = match_analyser.return_the_top_three_matches_for_a_line("paul durant")
    assert results[0].matching_string == "paul durand"
    assert results[0].correspondance_ratio > 90
    assert results[1].matching_string == "paul dupont"
    assert results[1].correspondance_ratio > 80
    assert results[2].matching_string == "paule martin"
    assert results[2].correspondance_ratio > 50
    results = match_analyser.return_the_top_three_matches_for_a_line("cottonwood")
    assert results[0].matching_string == "cottonwood"
    assert results[0].correspondance_ratio > 90
    assert results[1].matching_string == "cottrwood"
    assert results[1].correspondance_ratio > 80
    assert results[2].matching_string == "cottrwood inc"
    assert results[2].correspondance_ratio > 50
    results = match_analyser.return_the_top_three_matches_for_a_line("td express")
    print(results)
    assert results[1].matching_string == "t d express"
    assert results[0].correspondance_ratio >= 90
    assert results[0].matching_string == "t d express tetd express tetd express"
    assert results[1].correspondance_ratio > 80
    assert results[2].correspondance_ratio > 50
    
    