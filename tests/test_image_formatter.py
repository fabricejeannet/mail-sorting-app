from image_processor.image_formatter import ImageFormatter
from image_processor.image_acquisition import ImageAcquisition
from image_processor.image_constants import RECTANGLE_START_POINT, RECTANGLE_END_POINT
from pyzbar import pyzbar
image_formatter = ImageFormatter()
image_acquisition = ImageAcquisition()

def test_get_grayscaled_image():
    image = image_acquisition.open_image("tests/cropped_image.jpg")
    grayscale_image = image_formatter.get_grayscaled_image(image)
    #Verify that the image is in grayscale, if its in color it will have 3 dimensions
    assert len(grayscale_image.shape) < 3
    

def test_crop_image():
    image = image_acquisition.open_image("tests/cropped_image.jpg")
    cropped_image = image_formatter.crop_image(image, 0, 0, 100, 100)
    assert cropped_image.shape == (100, 100, 3)
    
    
def test_remove_qr_codes_and_barcodes_from_image():
    image = image_acquisition.open_image("tests/recommande.jpg")
    grayscale_image = image_formatter.get_grayscaled_image(image)
    assert len(pyzbar.decode(grayscale_image)) == 1
    cleaned_image = image_formatter.remove_qr_codes_and_barcodes_from_image(grayscale_image)
    detected_barcodes = pyzbar.decode(cleaned_image)
    assert len(detected_barcodes) == 0
    