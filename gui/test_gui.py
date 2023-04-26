import os
from picamera2 import Picamera2
import cv2
import numpy as np
from PIL import ImageTk, Image
from tkinter import Tk, Label, Frame, Button, BOTTOM

class TkinterApp:

	def __init__(self):
		self.picam = Picamera2()
		self.picam.start()

	#Launch a Tkinter window with a quit button a window for the camera preview and the ocr results at the right of the camera preview
	def main(self):
		self.window = Tk()
		self.window.title("StreetFacteur")
		self.window.geometry("800x420")
		self.window.resizable(width=False, height=False)
		self.window.configure(background='blue')


		frame = Frame(self.window, width=600, height=400)
		frame.pack()
		frame.place(anchor='center', relx=0.5, rely=0.5)

		# Create an object of tkinter ImageTk
		img = ImageTk.PhotoImage(Image.fromarray(self.picam.capture_array()))

		# Create a Label Widget to display the text or Image
		label = Label(frame, image = img)
		label.pack()
  
		self.quitButton = Button(self.window, text = "Quit", command = self.window.destroy)
		self.quitButton.pack(side = BOTTOM)



		self.window.mainloop()
		

app = TkinterApp()
app.main()