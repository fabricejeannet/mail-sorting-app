import pytest
from text_extractor import TextExtractor
from fuzzywuzzy import fuzz


text_extractor = TextExtractor()
file_names = ["env1","env2","env3","env4","env5","env6"]
company_names = ["XALES FORMATIONS","la maison du japon","MSPV",  "ferbat", "l'atelier d'haritza", "Art de poser"]

def test_recupere_correctement_sur_enveloppe_standard():
    for index in range(len(file_names)):
        extracted_text = text_extractor.analyse_image_silently(file_names[index])
        #assert ("9 rue de conde").lower() in extracted_text
        assert ("33000 Bordeaux").lower() in extracted_text
        assert fuzz.partial_ratio(extracted_text,company_names[index].lower()) > 0.90
        
