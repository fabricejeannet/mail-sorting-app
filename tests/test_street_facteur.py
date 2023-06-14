import pytest
from streetfacteur_processor.app_back import AppBack
from match_processor.matching_result import MatchingResult
from image_processor.image_constants import *
from streetfacteur_processor.app_constants import *
from config_processor.config_importer import ConfigImporter

street_facteur = AppBack(None)
config_importer = ConfigImporter()


def test_init_csv():
    street_facteur.init_csv()
    assert street_facteur.match_analyser.clients_data_dictionary != None
    

def test_string_match_found():
    street_facteur.matching_results = ["test"]
    assert street_facteur.client_match_found() == True
    
    
def test_show_valid_image_on_full_match_with_matching_company():
    client1 = MatchingResult(matching_company="client1", company_match_ratio=100, status="ABONNE")
    client2 = MatchingResult(matching_company="client2", company_match_ratio=90, status="ABONNE")
    client3 = MatchingResult(matching_company="client3", company_match_ratio=80, status="ABONNE")
    street_facteur.matching_results = [client1, client2, client3]
    assert street_facteur.get_display_status() == DisplayStatus.VALID
    

def test_show_valid_image_on_full_match_with_matching_director():
    client1 = MatchingResult(matching_person="client1", person_match_ratio=100, status="ABONNE")
    client2 = MatchingResult(matching_person="client2", person_match_ratio=90, status="ABONNE")
    client3 = MatchingResult(matching_person="client3", person_match_ratio=80, status="ABONNE")
    street_facteur.matching_results = [client1, client2, client3]
    assert street_facteur.get_display_status() == DisplayStatus.VALID
    
    
def test_show_valid_image_on_full_match_with_matching_director_and_company():
    client1 = MatchingResult(matching_company="client1", company_match_ratio=100, matching_person="client1", person_match_ratio=100, status="ABONNE")
    client2 = MatchingResult(matching_company="client2", company_match_ratio=90, matching_person="client2", person_match_ratio=90, status="ABONNE")
    client3 = MatchingResult(matching_company="client3", company_match_ratio=80, matching_person="client3", person_match_ratio=80, status="ABONNE")
    street_facteur.matching_results = [client1, client2, client3]
    assert street_facteur.get_display_status() == DisplayStatus.VALID


def test_show_valid_on_full_match_with_mix_matching_director_and_company():
    client1 = MatchingResult(matching_company="client1", company_match_ratio=100, status="ABONNE")
    client2 = MatchingResult(matching_person="client2", person_match_ratio=90, status="ABONNE")
    client3 = MatchingResult(matching_company="client3", company_match_ratio=80, matching_person="client3", person_match_ratio=80, status="ABONNE")
    street_facteur.matching_results = [client1, client2, client3]
    assert street_facteur.get_display_status() == DisplayStatus.VALID
    
def test_show_warning_image_if_a_result_is_not_subscribed_with_matching_company():
    client1 = MatchingResult(matching_company="client1", company_match_ratio=100, status="ABONNE")
    client2 = MatchingResult(matching_company="client2", company_match_ratio=90, status="ABONNE")
    client3 = MatchingResult(matching_company="client3", company_match_ratio=80, status="DESABONNE")
    street_facteur.matching_results = [client1, client2, client3]
    assert street_facteur.get_display_status() == DisplayStatus.WARNING_STATUS
    

def test_show_warning_image_if_a_result_is_not_subscribed_with_matching_director():
    client1 = MatchingResult(matching_person="client1", person_match_ratio=100, status="ABONNE")
    client2 = MatchingResult(matching_person="client2", person_match_ratio=90, status="ABONNE")
    client3 = MatchingResult(matching_person="client3", person_match_ratio=80, status="DESABONNE")
    street_facteur.matching_results = [client1, client2, client3]
    assert street_facteur.get_display_status() == DisplayStatus.WARNING_STATUS
    

def test_show_warning_image_if_a_result_is_not_subscribed_with_mix_matching_director_and_company():
    client1 = MatchingResult(matching_company="client1", company_match_ratio=100, status="ABONNE")
    client2 = MatchingResult(matching_person="client2", person_match_ratio=90, status="ABONNE")
    client3 = MatchingResult(matching_company="client3", company_match_ratio=80, matching_person="client3", person_match_ratio=80, status="DESABONNE")
    street_facteur.matching_results = [client1, client2, client3]
    assert street_facteur.get_display_status() == DisplayStatus.WARNING_STATUS
    

def test_show_warning_if_all_valid_but_no_match_with_a_good_matching_rate_with_matching_company():
    client1 = MatchingResult(matching_company="client1", company_match_ratio=config_importer.get_image_valid_threshold() - 5, status="ABONNE")
    client2 = MatchingResult(matching_company="client2", company_match_ratio=config_importer.get_image_valid_threshold() - 10, status="ABONNE")
    client3 = MatchingResult(matching_company="client3", company_match_ratio=config_importer.get_image_valid_threshold()- 20, status="ABONNE")
    street_facteur.matching_results = [client1, client2, client3]
    assert street_facteur.get_display_status() == DisplayStatus.WARNING_CORRESPONDANCE_RATE
    

def test_show_warning_if_all_valid_but_no_match_with_a_good_matching_rate_with_matching_director():
    client1 = MatchingResult(matching_person="client1", person_match_ratio=config_importer.get_image_valid_threshold() - 5, status="ABONNE")
    client2 = MatchingResult(matching_person="client2", person_match_ratio=config_importer.get_image_valid_threshold() - 10, status="ABONNE")
    client3 = MatchingResult(matching_person="client3", person_match_ratio=config_importer.get_image_valid_threshold()- 20, status="ABONNE")
    street_facteur.matching_results = [client1, client2, client3]
    assert street_facteur.get_display_status() == DisplayStatus.WARNING_CORRESPONDANCE_RATE
    

def test_show_warning_if_all_valid_but_no_match_with_a_good_matching_rate_with_mix_matching_director_and_company():
    client1 = MatchingResult(matching_company="client1", company_match_ratio=config_importer.get_image_valid_threshold() - 5, status="ABONNE")
    client2 = MatchingResult(matching_person="client2", person_match_ratio=config_importer.get_image_valid_threshold() - 10, status="ABONNE")
    client3 = MatchingResult(matching_company="client3", company_match_ratio=config_importer.get_image_valid_threshold()- 20, matching_person="client3", person_match_ratio=config_importer.get_image_valid_threshold()- 20, status="ABONNE")
    street_facteur.matching_results = [client1, client2, client3]
    assert street_facteur.get_display_status() == DisplayStatus.WARNING_CORRESPONDANCE_RATE
    

def test_multiple_valid_results_but_differents_status_return_warning_with_company():
    client1 = MatchingResult(matching_company="client1", company_match_ratio=config_importer.get_image_valid_threshold() + 11, status="ABONNE")
    client2 = MatchingResult(matching_company="client2", company_match_ratio=config_importer.get_image_valid_threshold() + 10, status="DESABONNE")
    client3 = MatchingResult(matching_company="client3", company_match_ratio=config_importer.get_image_valid_threshold() + 5, status="RADIE")
    street_facteur.matching_results = [client1, client2, client3]
    assert street_facteur.get_display_status() == DisplayStatus.WARNING_STATUS


def test_multiple_valid_results_but_differents_status_return_warning_with_director():
    client1 = MatchingResult(matching_person="client1", person_match_ratio=config_importer.get_image_valid_threshold() + 11, status="ABONNE")
    client2 = MatchingResult(matching_person="client2", person_match_ratio=config_importer.get_image_valid_threshold() + 10, status="DESABONNE")
    client3 = MatchingResult(matching_person="client3", person_match_ratio=config_importer.get_image_valid_threshold() + 5, status="RADIE")
    street_facteur.matching_results = [client1, client2, client3]
    assert street_facteur.get_display_status() == DisplayStatus.WARNING_STATUS
    

def test_multiple_valid_results_but_differents_status_return_warning_with_mix_matching_director_and_company():
    client1 = MatchingResult(matching_company="client1", company_match_ratio=config_importer.get_image_valid_threshold() + 11, status="ABONNE")
    client2 = MatchingResult(matching_person="client2", person_match_ratio=config_importer.get_image_valid_threshold() + 10, status="DESABONNE")
    client3 = MatchingResult(matching_company="client3", company_match_ratio=config_importer.get_image_valid_threshold() + 5, matching_person="client3", person_match_ratio=config_importer.get_image_valid_threshold() + 5, status="RADIE")
    street_facteur.matching_results = [client1, client2, client3]
    assert street_facteur.get_display_status() == DisplayStatus.WARNING_STATUS
    

def test_perfect_matchs_but_at_least_one_is_valid_with_company():
    client1 = MatchingResult(matching_company="client1", company_match_ratio=100, status="ABONNE")
    client2 = MatchingResult(matching_company="client2", company_match_ratio=100, status="DESABONNE")
    client3 = MatchingResult(matching_company="client3", company_match_ratio=100, status="RADIE")
    street_facteur.matching_results = [client1, client2, client3]
    assert street_facteur.get_display_status() == DisplayStatus.WARNING_STATUS


def test_perfect_matchs_but_at_least_one_is_valid_with_director():
    client1 = MatchingResult(matching_person="client1", person_match_ratio=100, status="ABONNE")
    client2 = MatchingResult(matching_person="client2", person_match_ratio=100, status="DESABONNE")
    client3 = MatchingResult(matching_person="client3", person_match_ratio=100, status="RADIE")
    street_facteur.matching_results = [client1, client2, client3]
    assert street_facteur.get_display_status() == DisplayStatus.WARNING_STATUS
    

def test_perfect_matchs_but_at_least_one_is_valid_with_mix_matching_director_and_company():
    client1 = MatchingResult(matching_company="client1", company_match_ratio=100, status="ABONNE")
    client2 = MatchingResult(matching_person="client2", person_match_ratio=100, status="DESABONNE")
    client3 = MatchingResult(matching_company="client3", company_match_ratio=100, matching_person="client3", person_match_ratio=100, status="RADIE")
    street_facteur.matching_results = [client1, client2, client3]
    assert street_facteur.get_display_status() == DisplayStatus.WARNING_STATUS
    
    
def test_no_match_found_at_all():
    street_facteur.matching_results = []
    assert street_facteur.get_display_status() == DisplayStatus.INVALID_NO_MATCH


def test_check_if_the_first_result_have_a_good_correspondance_rate_with_matching_company():
    client1 = MatchingResult(matching_company="client1", company_match_ratio=config_importer.get_image_valid_threshold() + 1, status="ABONNE")
    client2 = MatchingResult(matching_company="client2", company_match_ratio=config_importer.get_image_valid_threshold() - 1, status="ABONNE")
    client3 = MatchingResult(matching_company="client3", company_match_ratio=config_importer.get_image_valid_threshold() - 5, status="ABONNE")
    street_facteur.matching_results = [client1, client2, client3]
    assert street_facteur.first_result_have_valid_match_ratio() == True
    client1 = MatchingResult(matching_company="client1", company_match_ratio=config_importer.get_image_valid_threshold() - 1, status="ABONNE")
    client2 = MatchingResult(matching_company="client2", company_match_ratio=config_importer.get_image_valid_threshold() - 1, status="ABONNE")
    client3 = MatchingResult(matching_company="client3", company_match_ratio=config_importer.get_image_valid_threshold() - 5, status="ABONNE")
    street_facteur.matching_results = [client1, client2, client3]
    assert street_facteur.first_result_have_valid_match_ratio() == False
    

def test_check_if_the_first_result_have_a_good_correspondance_rate_with_matching_director():
    client1 = MatchingResult(matching_person="client1", person_match_ratio=config_importer.get_image_valid_threshold() + 1, status="ABONNE")
    client2 = MatchingResult(matching_person="client2", person_match_ratio=config_importer.get_image_valid_threshold() - 1, status="ABONNE")
    client3 = MatchingResult(matching_person="client3", person_match_ratio=config_importer.get_image_valid_threshold() - 5, status="ABONNE")
    street_facteur.matching_results = [client1, client2, client3]
    assert street_facteur.first_result_have_valid_match_ratio() == True
    client1 = MatchingResult(matching_person="client1", person_match_ratio=config_importer.get_image_valid_threshold() - 1, status="ABONNE")
    client2 = MatchingResult(matching_person="client2", person_match_ratio=config_importer.get_image_valid_threshold() - 1, status="ABONNE")
    client3 = MatchingResult(matching_person="client3", person_match_ratio=config_importer.get_image_valid_threshold() - 5, status="ABONNE")
    street_facteur.matching_results = [client1, client2, client3]
    assert street_facteur.first_result_have_valid_match_ratio() == False
    
    
def test_check_if_the_first_result_have_a_good_correspondance_rate_with_mix_matching_director_and_company():
    client1 = MatchingResult(matching_company="client1", company_match_ratio=config_importer.get_image_valid_threshold() + 1, status="ABONNE")
    client2 = MatchingResult(matching_person="client2", person_match_ratio=config_importer.get_image_valid_threshold() - 1, status="ABONNE")
    client3 = MatchingResult(matching_company="client3", company_match_ratio=config_importer.get_image_valid_threshold() - 5, status="ABONNE")
    client4 = MatchingResult(matching_person="client4", person_match_ratio=config_importer.get_image_valid_threshold() - 5, status="ABONNE")
    street_facteur.matching_results = [client1, client2, client3, client4]
    assert street_facteur.first_result_have_valid_match_ratio() == True
    client1 = MatchingResult(matching_company="client1", company_match_ratio=config_importer.get_image_valid_threshold() - 1, status="ABONNE")
    client2 = MatchingResult(matching_person="client2", person_match_ratio=config_importer.get_image_valid_threshold() - 1, status="ABONNE")
    client3 = MatchingResult(matching_company="client3", company_match_ratio=config_importer.get_image_valid_threshold() - 5, status="ABONNE")
    client4 = MatchingResult(matching_person="client4", person_match_ratio=config_importer.get_image_valid_threshold() - 5, status="ABONNE")
    street_facteur.matching_results = [client1, client2, client3, client4]
    assert street_facteur.first_result_have_valid_match_ratio() == False
    
    
def test_reorder_results_to_show_the_most_corresponding_result_first_with_company_name():
    mock_clients1 = MatchingResult(matching_company="client1", company_match_ratio=config_importer.get_image_valid_threshold() + 1, status="ABONNE")
    mock_clients2 = MatchingResult(matching_company="client2", company_match_ratio=config_importer.get_image_valid_threshold() + 4, status="ABONNE")
    street_facteur.matching_results = [mock_clients1, mock_clients2]
    street_facteur.reorder_results_to_show_the_most_corresponding_result_first()
    assert street_facteur.matching_results[0].company_match_ratio == config_importer.get_image_valid_threshold() + 4
    mock_clients1 = MatchingResult(matching_company="client1", company_match_ratio=config_importer.get_image_valid_threshold() + 10, status="ABONNE")
    mock_clients2 = MatchingResult(matching_company="client2", company_match_ratio=config_importer.get_image_valid_threshold() + 4, status="ABONNE")
    street_facteur.matching_results = [mock_clients1, mock_clients2]
    street_facteur.reorder_results_to_show_the_most_corresponding_result_first()
    assert street_facteur.matching_results[0].company_match_ratio == config_importer.get_image_valid_threshold() + 10


def test_reorder_results_to_show_the_most_corresponding_result_first_with_person_name():
    mock_clients1 = MatchingResult(matching_person="client1", person_match_ratio=config_importer.get_image_valid_threshold() + 1, status="ABONNE")
    mock_clients2 = MatchingResult(matching_person="client2", person_match_ratio=config_importer.get_image_valid_threshold() + 4, status="ABONNE")
    street_facteur.matching_results = [mock_clients1, mock_clients2]
    street_facteur.reorder_results_to_show_the_most_corresponding_result_first()
    assert street_facteur.matching_results[0].person_match_ratio == config_importer.get_image_valid_threshold() + 4
    mock_clients1 = MatchingResult(matching_person="client1", person_match_ratio=config_importer.get_image_valid_threshold() + 10, status="ABONNE")
    mock_clients2 = MatchingResult(matching_person="client2", person_match_ratio=config_importer.get_image_valid_threshold() + 4, status="ABONNE")
    street_facteur.matching_results = [mock_clients1, mock_clients2]
    street_facteur.reorder_results_to_show_the_most_corresponding_result_first()
    assert street_facteur.matching_results[0].person_match_ratio == config_importer.get_image_valid_threshold() + 10
    

def test_reorder_results_to_show_the_most_corresponding_result_first_with_mix_matching_director_and_company():
    mock_clients1 = MatchingResult(matching_company="client1", company_match_ratio=config_importer.get_image_valid_threshold() + 1, status="ABONNE")
    mock_clients2 = MatchingResult(matching_person="client2", person_match_ratio=config_importer.get_image_valid_threshold() + 4, status="ABONNE")
    street_facteur.matching_results = [mock_clients1, mock_clients2]
    street_facteur.reorder_results_to_show_the_most_corresponding_result_first()
    assert street_facteur.matching_results[0].get_max_match_ratio() == config_importer.get_image_valid_threshold() + 4
    mock_clients1 = MatchingResult(matching_company="client1", company_match_ratio=config_importer.get_image_valid_threshold() + 10, status="ABONNE")
    mock_clients2 = MatchingResult(matching_person="client2", person_match_ratio=config_importer.get_image_valid_threshold() + 4, status="ABONNE")
    street_facteur.matching_results = [mock_clients1, mock_clients2]
    street_facteur.reorder_results_to_show_the_most_corresponding_result_first()
    assert street_facteur.matching_results[0].get_max_match_ratio() == config_importer.get_image_valid_threshold() + 10
    

def test_check_if_the_first_result_is_a_perfect_match():
    client1 = MatchingResult(matching_company="client1", company_match_ratio=100, status="ABONNE")
    street_facteur.matching_results = [client1]
    assert street_facteur.check_if_the_first_result_is_a_perfect_match() == True
    client1 = MatchingResult(matching_company="client1", company_match_ratio=99, status="ABONNE")
    street_facteur.matching_results = [client1]
    assert street_facteur.check_if_the_first_result_is_a_perfect_match() == False
    client = MatchingResult(matching_person="client1", person_match_ratio=100, status="ABONNE")
    street_facteur.matching_results = [client]
    assert street_facteur.check_if_the_first_result_is_a_perfect_match() == True
    client = MatchingResult(matching_person="client1", person_match_ratio=99, status="ABONNE")
    street_facteur.matching_results = [client]
    assert street_facteur.check_if_the_first_result_is_a_perfect_match() == False
    client1 = MatchingResult(matching_company="client1", matching_person="client un", company_match_ratio=100, person_match_ratio=100, status="ABONNE")
    street_facteur.matching_results = [client1]
    assert street_facteur.check_if_the_first_result_is_a_perfect_match() == True
    client1 = MatchingResult(matching_company="client1", matching_person="client un", company_match_ratio=99, person_match_ratio=100, status="ABONNE")
    street_facteur.matching_results = [client1]
    assert street_facteur.check_if_the_first_result_is_a_perfect_match() == True
    client1 = MatchingResult(matching_company="client1", matching_person="client un", company_match_ratio=100, person_match_ratio=99, status="ABONNE")
    street_facteur.matching_results = [client1]
    assert street_facteur.check_if_the_first_result_is_a_perfect_match() == True
    client1 = MatchingResult(matching_company="client1", matching_person="client un", company_match_ratio=99, person_match_ratio=99, status="ABONNE")
    street_facteur.matching_results = [client1]
    assert street_facteur.check_if_the_first_result_is_a_perfect_match() == False
    