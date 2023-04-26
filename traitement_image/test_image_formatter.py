from image_formatter import *
from image_manager import ImageManager

image_formatter = ImageFormatter()
image_manager = ImageManager()

def test_return_gray_image():
    image = image_manager.open_image("images/env1.jpg")
    gray_image = image_formatter.get_grayscaled_image(image)
    assert gray_image is not None
    assert len(gray_image.shape)<3
    
def test_crop_image():
    image = image_manager.open_image("images/env1.jpg")
    cropped_image = image_formatter.crop_image(image, 0, 0, 100, 100)
    assert cropped_image is not None
    assert cropped_image.shape[0] == 100
    assert cropped_image.shape[1] == 100
    
def test_crop_image_from_rectangle_coordinates():
    image = image_manager.open_image("images/env1.jpg")
    cropped_image = image_formatter.crop_image_with_rectangle_coordinates(image, [0, 0], [100, 100])
    assert cropped_image is not None
    assert cropped_image.shape[0] == 100
    assert cropped_image.shape[1] == 100
    
def test_crop_image_from_text():
    image = image_manager.open_image("images/env1.jpg")
    cropped_image = image_formatter.crop_image_around_text(image, "Bordeaux")
    assert cropped_image is not None
    assert cropped_image.shape[0] == 212
    assert cropped_image.shape[1] == 891