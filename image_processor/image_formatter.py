import cv2
from pyzbar import pyzbar
import pytesseract
import numpy as np
import logging
from image_processor.image_constants import RECTANGLE_START_POINT, RECTANGLE_END_POINT, RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT
from image_processor.image_constants import RECTANGLE_START_POINT, RECTANGLE_END_POINT

class ImageFormatter:
    
    def __init__(self):
        pass
    
    
    def get_grayscaled_image(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    
    def crop_image(self, image, x, y, width, height):
        return image[y:y+height, x:x+width]
    
    
    def crop_image_with_rectangle_coordinates(self,image):
        width = RECTANGLE_END_POINT[0] - RECTANGLE_START_POINT[0]
        height = RECTANGLE_END_POINT[1] - RECTANGLE_START_POINT[1]        
        return self.crop_image(image, RECTANGLE_START_POINT[0], RECTANGLE_START_POINT[1], width, height)
    
    
    def draw_rectangle_with_coordinates(self,image):
        cv2.rectangle(image, RECTANGLE_START_POINT, RECTANGLE_END_POINT, (0, 255, 0), 2)
        return image
    
    
    def get_noise_removed_image(self, image):
        return cv2.medianBlur(image,1)
    
    
    def get_image_ready_for_text_detection(self, image):
        grayscaled_image = self.get_grayscaled_image(image)
        noise_removed_image = self.get_noise_removed_image(grayscaled_image)
        return self.crop_image_with_rectangle_coordinates(noise_removed_image)
    
    
    def get_image_ready_for_preview_display(self,image):
        self.draw_rectangle_with_coordinates(image)
        return self.resize_image(image)
    
    
    def resize_image(self, image):
        return cv2.resize(image, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))
    
    
    def add_rectangle_around_analysed_lines(self, prepared_image,to_display_image, lines):
        df = pytesseract.image_to_data(prepared_image, lang="fra", output_type=pytesseract.Output.DATAFRAME)
        print(df[["text", "conf", "line_num","block_num"]])
        
        # group recognized words by lines
        for searched_line in lines:
            for line_num, words_per_line in df.groupby(["block_num","par_num","line_num"]):
                # filter out words with a low confidence
                words_per_line = words_per_line[words_per_line["conf"] >= 5]
                if not len(words_per_line):
                    continue

                words = words_per_line["text"].values
                line = " ".join(words)
                print(f"{line_num} '{line}'")
                print(searched_line)
                logging.info("Line: " + line)
                if searched_line in line.lower():
                    print("Found a line with specified text")
                    word_boxes = []
                    for left, top, width, height in words_per_line[["left", "top", "width", "height"]].values:
                        word_boxes.append((left, top))
                        word_boxes.append((left + width, top + height))

                    x, y, w, h = cv2.boundingRect(np.array(word_boxes))
                    x = x + RECTANGLE_START_POINT[0]
                    y = y + RECTANGLE_START_POINT[1]
                    cv2.rectangle(to_display_image, (x, y), (x + w, y + h), color=(255, 0, 255), thickness=3)
                    cv2.putText(img=to_display_image, text=line, org=(x, y), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, color=(0, 0, 255), thickness=2)

        return to_display_image
