from data_analyser import DataAnalyser
from io import StringIO
from csv_constants import *
from fuzzywuzzy import fuzz

import sys





def test_ratio():
    mock_clients_data_dictionnary = {RAISON_SOCIALE : ["Mr Martin Dominique", "Mr Dominique Martin", "indominique"], STATUT : ["ABONNE", "ABONNE", "ABONNE"] }
    data_analyser = DataAnalyser(mock_clients_data_dictionnary)
    results = data_analyser.return_the_top_three_matches_for_a_line("dominique martin")
    assert results[0].matching_string == "Mr Dominique Martin".lower()
    assert results[0].correspondance_rate == 100
    assert results[1].matching_string == "Mr Martin Dominique".lower()
    assert results[2].matching_string ==  "indominique".lower()
    
def test_fuzz_sort_token_ratio():
    correspondance_rate = fuzz.token_sort_ratio("dominique martin", "Dominique Martin")
    assert correspondance_rate == 100
    correspondance_rate = fuzz.token_sort_ratio("dominique martin", "Martin Dominique")
    assert correspondance_rate == 100


def test_fuzz_set_token_ratio():
    correspondance_rate = fuzz.token_set_ratio("dominique martin", "Mr Dominique Martin totototototototot")
    assert correspondance_rate == 100
    correspondance_rate = fuzz.token_set_ratio("dominique martin", "Mr Martin Dominique toto")
    assert correspondance_rate == 100
