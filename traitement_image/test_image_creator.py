import pytest
from image_manager import *
import matplotlib.pyplot as plt

image_manager = ImageManager()

def test_open_image_with_valid_path():
    image = image_manager.open_image("images/recommande_avec_bureau3.jpg")
    assert image is not None
    
def test_open_image_with_invalid_path_raises_error():
    with pytest.raises(FileNotFoundError):
        image = image_manager.open_image("images/invalid_image.jpg")
        assert image is None

def test_take_and_save_picture():
    file_name = "captured_image.jpg"
    image_manager.take_and_save_picture()
    image = image_manager.open_image(file_name)
    assert image is not None
    image_manager.delete_picture(file_name)
    