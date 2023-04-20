import cv2
from image_formatter import ImageFormatter
from picamera2 import *
import numpy as np

# Grab images as numpy arrays and leave everything else to OpenCV.
image_formatter = ImageFormatter()
cv2.startWindowThread()

picam2 = Picamera2()
preview = picam2.start_preview()
picam2.start()


def is_there_movement_on_frame(previous_frame):
    frame_count = 0
    
    frame_count += 1

    # 1. Load image; convert to RGB
    img_brg = picam2.capture_array()
    img_rgb = cv2.cvtColor(src=img_brg, code=cv2.COLOR_BGR2RGB)


    # 2. Prepare image; grayscale and blur
    prepared_frame = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    prepared_frame = cv2.GaussianBlur(src=prepared_frame, ksize=(5,5), sigmaX=0)
    
    # 3. Set previous frame and continue if there is None
    if (previous_frame is None):
        # First frame; there is no previous one yet
        previous_frame = prepared_frame
    
    # calculate difference and update previous frame
    diff_frame = cv2.absdiff(src1=previous_frame, src2=prepared_frame)
    previous_frame = prepared_frame

    # 4. Dilute the image a bit to make differences more seeable; more suitable for contour detection
    kernel = np.ones((5, 5))
    diff_frame = cv2.dilate(diff_frame, kernel, 1)

    # 5. Only take different areas that are different enough (>20 / 255)
    thresh_frame = cv2.threshold(src=diff_frame, thresh=20, maxval=255, type=cv2.THRESH_BINARY)[1]

    contours, _ = cv2.findContours(image=thresh_frame, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)

    contours, _ = cv2.findContours(image=thresh_frame, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) < 50:
            # too small: skip!
            continue
        return True
    return False
        

def rectangular_black_and_white_preview():
    while True:
        im = picam2.capture_array()
        im = image_formatter.get_cleaned_black_and_white_image(im)
        cv2.rectangle(im, (50, 50), (600, 400), (0, 255, 0))
        im = cv2.resize(im, (600,400))
        cv2.imshow("Camera", im)
        
while True:
    print(is_there_movement_on_frame())