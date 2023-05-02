from data_analyser import DataAnalyser
from io import StringIO

import sys

data_analyser = DataAnalyser()

def test_return_the_top_three_matching_names_for_a_line():
    results = data_analyser.return_the_top_three_matches_for_a_line("cottowood")
    assert results["matching_name"][0] == "cottonwood"
    assert results["statut"][0] == "ABONNE"
    assert results["correspondance_rate"][0] > 80
    
def test_return_the_top_three_matching_names_for_a_line_with_wakan():
    results = data_analyser.return_the_top_three_matches_for_a_line("wakan |")
    assert results["matching_name"][0] == "wakan toulouse "
    assert results["statut"][0] == "ABONNE"
    assert results["correspondance_rate"][0] > 80
    
    
def test_return_none_if_no_matching_name():
    results = data_analyser.return_the_top_three_matches_for_a_line("")
    assert results["matching_name"][0] == ""
    assert results["statut"][0] == ""
    assert results["correspondance_rate"][0] == 0
    
def test_display_results():
    results = data_analyser.return_the_top_three_matches_for_a_line("cottowood")
    capturedOutput = StringIO()          # Create StringIO object
    sys.stdout = capturedOutput                   #  and redirect stdout.
    data_analyser.display_results(results)        # Call unchanged function.
    sys.stdout = sys.__stdout__                   # Reset redirect.
    assert capturedOutput.getvalue() == "Matching name: cottonwood - Statut: ABONNE - Correspondance rate: 95\nMatching name: okto - Statut: ABONNE - Correspondance rate: 75\nMatching name: mco - Statut: DESABONNE - Correspondance rate: 67\n"