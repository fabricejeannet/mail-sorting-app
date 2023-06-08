from match_processor.match_analyser import MatchAnalyser
from csv_processor.csv_manager import CsvManager
from config_processor.config_importer import ConfigImporter

THRESHOLD = ConfigImporter().get_image_minimum_threshold()
csv_manager = CsvManager()
csv_manager.open_csv_file("tests/test.csv")

def test_get_match_ratio():
    match_analyser = MatchAnalyser(None)
    assert match_analyser.get_match_ratio("hello","hello") == 100
    assert match_analyser.get_match_ratio("hello","world") <= THRESHOLD, "The threshold is too low"
    

def test_get_match_ratio_for_names():
    match_analyser = MatchAnalyser(None)
    assert match_analyser.get_match_ratio_for_names("Jean Louis","Jean-Louis") == 100
    assert match_analyser.get_match_ratio_for_names("Jean Louis","Jean Louis") == 100
    assert match_analyser.get_match_ratio_for_names("Jean Louis","Jean Louis Dupont") >= 85
    assert match_analyser.get_match_ratio_for_names("Jean Louis","Louis Jean") == 100


def test_get_match_ratio_for_company_names():
    match_analyser = MatchAnalyser(None)
    assert match_analyser.get_average_match_ratio("t d express", "t d express tetd express TETD EXPRESS") > 70
    assert match_analyser.get_average_match_ratio("cottonwood","cottrwood") > 80
    assert match_analyser.get_average_match_ratio("hello","world") <= THRESHOLD, "The threshold is too low"
    assert match_analyser.get_average_match_ratio("emotional damage","em") < THRESHOLD, "The threshold is too low"
    assert match_analyser.get_average_match_ratio("em","emotional") < THRESHOLD, "The threshold is too low"


def test_get_average_match_ratio():
    match_analyser = MatchAnalyser(None)
    assert match_analyser.get_average_match_ratio("hello","hello") == 100
    assert match_analyser.get_average_match_ratio("t d express", "t d express tetd express TETD EXPRESS") > 70
    assert match_analyser.get_average_match_ratio("cottonwood","cottrwood") > 80
    assert match_analyser.get_average_match_ratio("hello","world") <= THRESHOLD, "The threshold is too low"
    assert match_analyser.get_average_match_ratio("em","emotional damage") < THRESHOLD, "The threshold is too low"
    assert match_analyser.get_average_match_ratio("em","emotional") < THRESHOLD, "The threshold is too low"
    
    
def test_return_the_top_five_matches_for_a_line():
    mock_clients = csv_manager.get_clients_data_dictionnary()
    match_analyser = MatchAnalyser(mock_clients)
    match_analyser.reset_match_results()
    match_analyser.find_the_best_results("paul durant")
    results = match_analyser.get_matching_results()
    assert results[0].matching_person == "paul durand"
    assert results[0].person_match_ratio > 90
    assert results[1].matching_person == "paul dupont"
    assert results[1].person_match_ratio > 80
    match_analyser.reset_match_results()
    match_analyser.find_the_best_results("cottonwood")
    results = match_analyser.get_matching_results()
    assert results[0].matching_company == "cottonwood"
    assert results[0].company_match_ratio > 90
    assert results[1].matching_company == "cottrwood"
    assert results[1].company_match_ratio > 80
    match_analyser.reset_match_results()
    match_analyser.find_the_best_results("td express")
    results = match_analyser.get_matching_results()
    assert results[0].matching_company == "t d express"
    assert results[0].company_match_ratio >= 85
    assert results[2].matching_company == "t d express tetd express tetd express"
    assert results[2].company_match_ratio > THRESHOLD
    
    
def test_if_check_all_columns_for_matching():
    mock_clients = csv_manager.get_clients_data_dictionnary()
    match_analyser = MatchAnalyser(mock_clients)
    match_analyser.reset_match_results()
    match_analyser.find_the_best_results("paul durant")
    assert match_analyser.get_matching_results()[0].matching_person == "paul durand"
    match_analyser.reset_match_results()
    match_analyser.find_the_best_results("victorien clemence")
    assert match_analyser.get_matching_results()[0].matching_person == "victorien clemence"
    
    
def test_aeg():
    mock_clients = csv_manager.get_clients_data_dictionnary()
    match_analyser = MatchAnalyser(mock_clients)
    match_analyser.reset_match_results()
    match_analyser.find_the_best_results("aeg")
    assert match_analyser.get_matching_results()[0].matching_company == "aeg"
    
    
def test_di():
    mock_clients = csv_manager.get_clients_data_dictionnary()
    match_analyser = MatchAnalyser(mock_clients)
    match_analyser.reset_match_results()
    match_analyser.find_the_best_results("di.")
    assert len(match_analyser.get_matching_results()) == 0
    

def test_mp():
    mock_clients = csv_manager.get_clients_data_dictionnary()
    match_analyser = MatchAnalyser(mock_clients)
    match_analyser.reset_match_results()
    match_analyser.find_the_best_results("mp")
    assert len(match_analyser.get_matching_results()) == 1
    assert match_analyser.get_matching_results()[0].matching_company == "mp emergence"