import pytest
from image_analyser import *
from image_manager import ImageManager

image_analyser = ImageAnalyser()
image_manager = ImageManager()

def test_get_text_position_from_image_with_valid_text():
    image = image_manager.open_image("images/test.jpg")
    text_position = image_analyser.get_text_position_from_image(image, "Bordeaux")
    assert text_position is not None
    assert text_position[0] == 384
    assert text_position[1] == 336
    assert text_position[2] == 552
    assert text_position[3] == 365
    
def test_get_text_position_from_image_with_invalid_text_raises_error():
    image = image_manager.open_image("images/env2.jpg")
    with pytest.raises(NoTextFoundOnPicture):
        text_position = image_analyser.get_text_position_from_image(image, "invalid_text")
        assert text_position is None

def test_get_text_from_image():
    image = image_manager.open_image("images/env2.jpg")
    text = image_analyser.get_text_from_image(image)
    assert text is not None
    
def test_return_true_if_text_is_in_image():
    image = image_manager.open_image("images/env1.jpg")
    assert image_analyser.check_if_text_is_in_image(image, "bordeaux") == True
    
def test_return_true_if_text_is_in_image_with_different_case():
    image = image_manager.open_image("images/env1.jpg")
    assert image_analyser.check_if_text_is_in_image(image, "Bordeaux") == True
    
def test_return_false_if_text_is_not_in_image():
    image = image_manager.open_image("images/env2.jpg")
    assert image_analyser.check_if_text_is_in_image(image, "invalid_text") == False