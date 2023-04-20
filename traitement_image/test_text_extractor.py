import pytest
from text_extractor import TextExtractor
from fuzzywuzzy import fuzz


text_extractor = TextExtractor()
file_names = ["env1","env2","env3","env4","env5","env6","env7"]
company_names = ["XALES FORMATIONS","la maison du japon","MSPV",  "ferbat", "l'atelier d'haritza", "Art de poser","ma vie pratique"]
cleaned_text = [[["xales formations"]], [["la maison du japon"]],[["mspv"]],[["s.a.s. ferbat"]],[["l'atelier d'haritza"]],[["monsieur mehdi belhachemi"],["art de poser"]], [["ma vie pratique - olivia licoys"]]]

def test_recupere_correctement_sur_enveloppe_standard():
    for index in range(len(file_names)):
        extracted_text = text_extractor.analyse_image_silently(file_names[index])
        print(extracted_text)
        assert ("33000").lower() in extracted_text
        assert fuzz.partial_ratio(extracted_text,company_names[index].lower()) > 95
        assert text_extractor.clean_text_output_lines(extracted_text) == cleaned_text[index]     

def test_fuzz_partial_ration():
    assert fuzz.partial_ratio("9 rue de conde","rue de conde") > 90