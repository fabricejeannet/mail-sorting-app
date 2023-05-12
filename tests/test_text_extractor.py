import pytest
from text_processor.text_extractor import TextExtractor
from exceptions.custom_exceptions import NoImageGiven, NoTextFoundOnPicture
import numpy as np
text_extractor = TextExtractor()
cropped_image = "tests/cropped_image.jpg"
empty_image = "tests/empty_image.png"


def test_get_ocr_text_from_image():
    extracted_text = text_extractor.get_text_from_image(cropped_image).splitlines()
    assert extracted_text[0] == "M10 1341 510 0007690 00234 B"
    assert extracted_text[1] == ""
    assert extracted_text[2] == "L'ATELIER D'HARITZA"
    assert extracted_text[3] == "9 RUE DE CONDE"
    assert extracted_text[4] == "33000 BORDEAUX"
    
    
def test_get_cleaned_ocr_text_from_image():
    extracted_text = text_extractor.get_cleaned_text_from_image(cropped_image)
    assert extracted_text[0] == "l'atelier d'haritza"
    assert len(extracted_text) == 1
    
    
def test_dont_give_a_valid_image_raises_error():
    with pytest.raises(NoImageGiven):
        text_extractor.get_text_from_image("")
    with pytest.raises(NoImageGiven):
        text_extractor.get_text_from_image(None)
        
        
def test_dont_find_text_on_image_raises_error():
    with pytest.raises(NoTextFoundOnPicture):
        text_extractor.get_cleaned_text_from_image(empty_image)