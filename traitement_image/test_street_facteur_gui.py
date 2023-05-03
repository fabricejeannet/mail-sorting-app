from street_facteur_gui import *

street_facteur = StreetFacteurGui()
street_facteur.cleaned_ocr_result = ["test"]
street_facteur.add_matching_results_from_cleaned_ocr_result(street_facteur.cleaned_ocr_result)


def test_return_resized_image_with_rectangle():
    image = cv2.imread("images_test/test.jpg")
    resized_image = street_facteur.return_resized_image_with_rectangle()
    assert resized_image.shape == (RESIZED_IMAGE_HEIGHT, RESIZED_IMAGE_WIDTH, 3)
    

def test_image_is_steady():
    assert street_facteur.image_is_steady() == False
    time.sleep(STEADY_WAIT_TIME)
    assert street_facteur.image_is_steady() == True
    

def test_remove_text_from_text_widgets():
    street_facteur.insert_a_separator_in_matching_text_widget()
    street_facteur.insert_a_separator_in_matching_text_widget()
    street_facteur.matching_text_widget.insert(END, "test")
    street_facteur.readed_line_widget.insert(END, "test")
    street_facteur.remove_text_from_text_widgets()
    assert street_facteur.matching_text_widget.get(1.0,END) == "\n"
    assert street_facteur.readed_line_widget.get(1.0,END) == "\n"
    

def test_check_if_the_first_result_have_a_good_correspondance_rate():
    street_facteur.matching_results[0]["correspondance_rate"][0] = 90
    assert street_facteur.check_if_the_first_result_have_a_good_correspondance_rate() == True
    street_facteur.matching_results[0]["correspondance_rate"][0] = 85
    assert street_facteur.check_if_the_first_result_have_a_good_correspondance_rate() == True
    street_facteur.matching_results[0]["correspondance_rate"][0] = 84
    assert street_facteur.check_if_the_first_result_have_a_good_correspondance_rate() == False
    street_facteur.matching_results[0]["correspondance_rate"][0] = -1
    assert street_facteur.check_if_the_first_result_have_a_good_correspondance_rate() == False
    

def test_reset_ocr_results():
    street_facteur.reset_ocr_results()
    assert street_facteur.matching_results == []
  