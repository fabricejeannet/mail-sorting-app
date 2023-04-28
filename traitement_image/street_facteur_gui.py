import os
from picamera2 import Picamera2
import cv2
import numpy as np
import threading
from image_formatter import ImageFormatter
from data_analyser import DataAnalyser
from image_constants import *
from text_extractor import TextExtractor
import time
from PIL import ImageTk, Image
from tkinter import Tk, Label, Frame, Button, BOTTOM, Text, BOTH, Scrollbar, RIGHT, Y, END, TOP, LEFT, X, Entry, StringVar, IntVar, OptionMenu, Menu, messagebox, filedialog, ttk

class TkinterApp:

	def __init__(self):
		self.picam = Picamera2()
		self.picam.configure(self.picam.create_preview_configuration(main={"format": 'RGB888', "size": (1280, 720)}))
		self.picam.start_preview()
		self.picam.start()
		self.captured_image = self.picam.capture_array()
		self.image_formatter = ImageFormatter()
		self.text_extractor = TextExtractor()
		self.data_analyser = DataAnalyser()
		self.last_movement_time = time.time()
		self.cleaned_ocr_result = []
		self.window = Tk()
		self.window.title("Street Facteur")
		self.window.geometry("800x480")
		self.window.attributes('-fullscreen', True)

		self.window.resizable(width=False, height=False)
		self.window.configure(background='gray')


	def return_resized_image_with_rectangle(self):
		self.captured_image = self.picam.capture_array()
		cv2.rectangle(self.captured_image, RECTANGLE_START_POINT, RECTANGLE_END_POINT, (0, 255, 0), 2)
		resized_image = cv2.resize(self.captured_image, (550, 405))
		return resized_image


	def image_is_steady(self):
		return time.time() - self.last_movement_time > STEADY_WAIT_TIME


	def remove_text_from_text_widgets(self):
		self.text_widget.delete('1.0', END)
		self.result_text_widget.delete('1.0', END)
			
	def add_result_to_tkinter_text(self):
		self.remove_text_from_text_widgets()
		self.result_text_widget.insert(END, "Lignes analysées : \n",('bold','blue'))
		for line_analyse in self.cleaned_ocr_result:
			self.result_text_widget.insert(END, str(line_analyse["searched_line"][0]) + "\n")
			for index in range(len(line_analyse["matching_name"])):
				if(line_analyse["matching_name"][index] != ""):
					self.text_widget.insert(END, "Matching name: " + line_analyse["matching_name"][index] + "\nStatut: " + line_analyse["statut"][index] + "\nCorrespondance rate: " + str(line_analyse["correspondance_rate"][index]) + "\n --- \n")


	def apply_ocr_on_image(self) :
		self.cleaned_ocr_result = []
		black_and_white_image = self.image_formatter.get_cleaned_black_and_white_image(self.captured_image)
		cropped_image = self.image_formatter.crop_image_with_rectangle_coordinates(black_and_white_image,RECTANGLE_START_POINT,RECTANGLE_END_POINT)
		cleaned_ocr_result = (self.text_extractor.get_cleaned_ocr_text_from_image(cropped_image))
		for line in cleaned_ocr_result:
			matching_line_results = self.data_analyser.return_the_top_three_matches_for_a_line(line)
			self.cleaned_ocr_result.append(matching_line_results)
   
	def has_detected_a_movement(self):   
		frame_count = 0
		previous_frame = None
	
		while True:
			frame_count += 1

			# 1. Load image; convert to RGB
			image_brg = self.picam.capture_array()
			image_rgb = cv2.cvtColor(src=image_brg, code=cv2.COLOR_BGR2RGB)

			if ((frame_count % 2) == 0):

				# 2. Prepare image; grayscale and blur
				prepared_frame = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2GRAY)
				prepared_frame = cv2.GaussianBlur(src=prepared_frame, ksize=(5,5), sigmaX=0)
			
				# 3. Set previous frame and continue if there is None
				if (previous_frame is None):
					# First frame; there is no previous one yet
					previous_frame = prepared_frame
					continue
				
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


	def main(self):
		camera_frame = Frame(self.window, width=550, height=405)
		camera_frame.pack()
		camera_frame.place(relx=.01, y=5)
		# Create a Label Widget to display the text or Image
		self.label = Label(camera_frame)
		self.label.pack()

		# Create a Quit Button to exit the program
		self.quitButton = Button(self.window, text="Quitter", command=self.window.destroy)
		self.quitButton.pack(side=BOTTOM)
		self.quitButton.place(relx=.8, rely=.90)

		#Create a Text frame to display the text
		text_frame = Frame(self.window, width=150, height=200, bg="white")
		text_frame.pack()
		text_frame.place(relx=.72, rely=.012)


		# Create a Text widget
		self.text_widget = Text(text_frame, width=25, height=15)
		self.text_widget.pack(side=LEFT, fill=Y)
		self.text_widget.tag_configure("blue", foreground="blue")
		self.text_widget.tag_configure("red", foreground="red")
		self.text_widget.tag_configure("green", foreground="green")
		self.text_widget.tag_configure("bold", font=("TkDefaultFont", 12, "bold"))
  
		# Create a frame for the text lines readed by the OCR
		result_frame = Frame(self.window, width=550, height=50)
		result_frame.pack()
		result_frame.place(relx=.01, rely=.88)
  
		# Create a Text widget
		self.result_text_widget = Text(result_frame, width = 68, height=3)
		self.result_text_widget.pack(side=LEFT, fill=Y)
		self.result_text_widget.tag_configure("blue", foreground="blue")
		self.result_text_widget.tag_configure("bold", font=("TkDefaultFont", 12, "bold"))
		
		

		image_has_been_analysed = True

		# Start a loop to continuously update the displayed image
		while True:
			escape_key_pressed = False

			if not image_has_been_analysed:
				self.text_widget.insert(END, "Attente d'une seconde avant analyse !\n",('bold','colored'))

			if (self.has_detected_a_movement()):
				self.text_widget.delete('1.0', END)
				self.text_widget.insert(END, "Mouvement détecté !\n",('bold','colored'))
				self.last_movement_time = time.time()
				image_has_been_analysed = False
			
				
			if (self.image_is_steady() and not image_has_been_analysed):
				self.apply_ocr_on_image()
				image_has_been_analysed = True
				self.add_result_to_tkinter_text()
			# Capture the actual image
			final_image = self.return_resized_image_with_rectangle()
			# Convert the captured image to a Tkinter compatible format
			final_image = Image.fromarray(final_image)
			final_image = ImageTk.PhotoImage(final_image)
			# Update the image displayed in the Label Widget
			self.label.configure(image=final_image)
			self.label.image = final_image
			# Update the window to show the new image
			self.window.update()
		

app = TkinterApp()
app.main()