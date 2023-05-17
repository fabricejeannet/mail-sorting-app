import pytest
from streetfacteur_processor.app_gui import StreetFacteur
from match_processor.matching_result import MatchingResult
from image_processor.image_constants import *

street_facteur = StreetFacteur()


def test_init_csv():
    street_facteur.init_csv()
    assert street_facteur.match_analyser.clients_data_dictionary != None
    

def test_string_match_found():
    street_facteur.matching_results = ["test"]
    assert street_facteur.string_match_found() == True
    
    
def test_show_valid_image_on_full_match():
    client1 = MatchingResult(matching_string="client1", correspondance_ratio=100, status="ABONNE")
    client2 = MatchingResult(matching_string="client2", correspondance_ratio=90, status="ABONNE")
    client3 = MatchingResult(matching_string="client3", correspondance_ratio=80, status="ABONNE")
    street_facteur.matching_results = [client1, client2, client3]
    assert street_facteur.select_the_good_image_for_help_widget() == "valid"
    
    
def test_show_warning_image_if_a_result_is_not_subscribed():
    client1 = MatchingResult(matching_string="client1", correspondance_ratio=100, status="ABONNE")
    client2 = MatchingResult(matching_string="client2", correspondance_ratio=90, status="ABONNE")
    client3 = MatchingResult(matching_string="client3", correspondance_ratio=80, status="DESABONNE")
    street_facteur.matching_results = [client1, client2, client3]
    assert street_facteur.select_the_good_image_for_help_widget() == "warning"

def test_show_warning_if_all_valid_but_no_match_with_a_good_matching_rate():
    client1 = MatchingResult(matching_string="client1", correspondance_ratio=VALID_CORRESPONDANCE_RATE_THRESHOLD - 5, status="ABONNE")
    client2 = MatchingResult(matching_string="client2", correspondance_ratio=VALID_CORRESPONDANCE_RATE_THRESHOLD - 10, status="ABONNE")
    client3 = MatchingResult(matching_string="client3", correspondance_ratio=VALID_CORRESPONDANCE_RATE_THRESHOLD- 20, status="ABONNE")
    street_facteur.matching_results = [client1, client2, client3]
    assert street_facteur.select_the_good_image_for_help_widget() == "warning"
    

def test_multiple_valid_results_but_differents_status_return_warning():
    client1 = MatchingResult(matching_string="client1", correspondance_ratio=VALID_CORRESPONDANCE_RATE_THRESHOLD + 11, status="ABONNE")
    client2 = MatchingResult(matching_string="client2", correspondance_ratio=VALID_CORRESPONDANCE_RATE_THRESHOLD + 10, status="DESABONNE")
    client3 = MatchingResult(matching_string="client3", correspondance_ratio=VALID_CORRESPONDANCE_RATE_THRESHOLD + 5, status="RADIE")
    street_facteur.matching_results = [client1, client2, client3]
    assert street_facteur.select_the_good_image_for_help_widget() == "warning"
    
    
def test_no_match_found_with_higher_rate_than_threshold():
    client1 = MatchingResult(matching_string="client1", correspondance_ratio=MINIMUM_CORRESPONDANCE_RATE_THRESHOLD - 5, status="ABONNE")
    client2 = MatchingResult(matching_string="client2", correspondance_ratio=MINIMUM_CORRESPONDANCE_RATE_THRESHOLD - 10, status="DESABONNE")
    client3 = MatchingResult(matching_string="client3", correspondance_ratio=MINIMUM_CORRESPONDANCE_RATE_THRESHOLD - 15, status="RADIE")
    street_facteur.matching_results = [client1, client2, client3]
    assert street_facteur.select_the_good_image_for_help_widget() == "invalid"
    
    
def test_no_match_found_at_all():
    street_facteur.matching_results = []
    assert street_facteur.select_the_good_image_for_help_widget() == "invalid"


def test_check_if_the_first_result_have_a_good_correspondance_rate():
    client1 = MatchingResult(matching_string="client1", correspondance_ratio=VALID_CORRESPONDANCE_RATE_THRESHOLD + 1, status="ABONNE")
    client2 = MatchingResult(matching_string="client2", correspondance_ratio=VALID_CORRESPONDANCE_RATE_THRESHOLD - 1, status="ABONNE")
    client3 = MatchingResult(matching_string="client3", correspondance_ratio=VALID_CORRESPONDANCE_RATE_THRESHOLD - 5, status="ABONNE")
    street_facteur.matching_results = [client1, client2, client3]
    assert street_facteur.check_if_the_first_result_have_a_good_correspondance_rate() == True
    client1 = MatchingResult(matching_string="client1", correspondance_ratio=VALID_CORRESPONDANCE_RATE_THRESHOLD - 1, status="ABONNE")
    client2 = MatchingResult(matching_string="client2", correspondance_ratio=VALID_CORRESPONDANCE_RATE_THRESHOLD - 1, status="ABONNE")
    client3 = MatchingResult(matching_string="client3", correspondance_ratio=VALID_CORRESPONDANCE_RATE_THRESHOLD - 5, status="ABONNE")
    street_facteur.matching_results = [client1, client2, client3]
    assert street_facteur.check_if_the_first_result_have_a_good_correspondance_rate() == False
    

def test_check_if_the_first_result_have_a_minimum_correspondance_rate():
    client1 = MatchingResult(matching_string="client1", correspondance_ratio=MINIMUM_CORRESPONDANCE_RATE_THRESHOLD + 1, status="ABONNE")
    client2 = MatchingResult(matching_string="client2", correspondance_ratio=MINIMUM_CORRESPONDANCE_RATE_THRESHOLD - 1, status="ABONNE")
    client3 = MatchingResult(matching_string="client3", correspondance_ratio=MINIMUM_CORRESPONDANCE_RATE_THRESHOLD - 5, status="ABONNE")
    street_facteur.matching_results = [client1, client2, client3]
    assert street_facteur.check_if_the_first_result_have_a_minimum_correspondance_rate() == True
    client1 = MatchingResult(matching_string="client1", correspondance_ratio=MINIMUM_CORRESPONDANCE_RATE_THRESHOLD - 1, status="ABONNE")
    client2 = MatchingResult(matching_string="client2", correspondance_ratio=MINIMUM_CORRESPONDANCE_RATE_THRESHOLD - 1, status="ABONNE")
    client3 = MatchingResult(matching_string="client3", correspondance_ratio=MINIMUM_CORRESPONDANCE_RATE_THRESHOLD - 5, status="ABONNE")
    street_facteur.matching_results = [client1, client2, client3]
    assert street_facteur.check_if_the_first_result_have_a_minimum_correspondance_rate() == False
    
    
def test_reorder_results_to_show_the_most_corresponding_result_first():
    mock_clients1 = MatchingResult(matching_string="client1", correspondance_ratio=VALID_CORRESPONDANCE_RATE_THRESHOLD + 1, status="ABONNE")
    mock_clients2 = MatchingResult(matching_string="client2", correspondance_ratio=VALID_CORRESPONDANCE_RATE_THRESHOLD + 4, status="ABONNE")
    street_facteur.matching_results = [mock_clients1, mock_clients2]
    street_facteur.reorder_results_to_show_the_most_corresponding_result_first()
    assert street_facteur.matching_results[0].match_ratio == VALID_CORRESPONDANCE_RATE_THRESHOLD + 4
    mock_clients1 = MatchingResult(matching_string="client1", correspondance_ratio=VALID_CORRESPONDANCE_RATE_THRESHOLD + 10, status="ABONNE")
    mock_clients2 = MatchingResult(matching_string="client2", correspondance_ratio=VALID_CORRESPONDANCE_RATE_THRESHOLD + 4, status="ABONNE")
    street_facteur.matching_results = [mock_clients1, mock_clients2]
    street_facteur.reorder_results_to_show_the_most_corresponding_result_first()
    assert street_facteur.matching_results[0].match_ratio == VALID_CORRESPONDANCE_RATE_THRESHOLD + 10
    

def test_check_if_the_first_result_is_a_perfect_match():
    client1 = MatchingResult(matching_string="client1", correspondance_ratio=100, status="ABONNE")
    street_facteur.matching_results = [client1]
    assert street_facteur.check_if_the_first_result_is_a_perfect_match() == True
    client1 = MatchingResult(matching_string="client1", correspondance_ratio=99, status="ABONNE")
    street_facteur.matching_results = [client1]
    assert street_facteur.check_if_the_first_result_is_a_perfect_match() == False