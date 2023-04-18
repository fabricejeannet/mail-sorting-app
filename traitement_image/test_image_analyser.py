import pytest
from image_analyser import *
from image_manager import ImageManager

image_analyser = ImageAnalyser()
image_manager = ImageManager()

def test_get_text_position_from_image_with_valid_text():
    image = image_manager.open_image("images/test.jpg")
    text_position = image_analyser.get_text_position_from_image(image, "Bordeaux")
    assert text_position is not None
    assert text_position[0] == 1459
    assert text_position[1] == 752
    assert text_position[2] == 167
    assert text_position[3] == 32
    
def test_get_text_position_from_image_with_invalid_text_raises_error():
    image = image_manager.open_image("images/env2.jpg")
    with pytest.raises(ValueError):
        text_position = image_analyser.get_text_position_from_image(image, "invalid_text")
        assert text_position is None

def test_get_text_from_image():
    image = image_manager.open_image("images/env2.jpg")
    text = image_analyser.get_text_from_image(image)
    assert text is not None