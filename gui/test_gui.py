import tkinter as tk
from tkinter import ttk


LARGEFONT =("Verdana", 35)

class tkinterApp(tk.Tk):
	
	# __init__ function for class tkinterApp
	def __init__(self, *args, **kwargs):
		
		# __init__ function for class Tk
		tk.Tk.__init__(self, *args, **kwargs)
		self.attributes('-fullscreen', True)
		# creating a container
		container = tk.Frame(self)
		container.pack(side = "top", fill = "both", expand = True)

		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)

		# initializing frames to an empty array
		self.frames = {}

		# iterating through a tuple consisting
		# of the different page layouts
		for F in (Accueil, Page_Analyse, Page_Gestion):

			frame = F(container, self)

			# initializing frame of that object from
			# Accueil, Page_Analyse, Page_Gestion respectively with
			# for loop
			self.frames[F] = frame

			frame.grid(row = 0, column = 0, sticky ="nsew")

		self.show_frame(Accueil)

	# to display the current frame passed as
	# parameter
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

# first window frame Accueil

class Accueil(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
		# label of frame Layout 2
		label = ttk.Label(self, text ="Accueil", font = LARGEFONT)
		
		button1 = ttk.Button(self, text ="Scan du courrier",
		command = lambda : controller.show_frame(Page_Analyse))
	
        button_exit = ttk.button(self, text ="Quitter", command = close)
        button_exit.grid(row = 3, column  = 1, padx =  10, pady=10)
        
		# putting the button in its place by
		# using grid
		button1.grid(row = 1, column = 1, padx = 10, pady = 10)

		## button to show frame 2 with text layout2
		button2 = ttk.Button(self, text ="Gestion des données",
		command = lambda : controller.show_frame(Page_Gestion))
	
		# putting the button in its place by
		# using grid
		button2.grid(row = 2, column = 1, padx = 10, pady = 10)

		


# second window frame Page_Analyse
class Page_Analyse(tk.Frame):
	
	def __init__(self, parent, controller):
		
		tk.Frame.__init__(self, parent)
		label = ttk.Label(self, text ="Page 1", font = LARGEFONT)
		label.grid(row = 0, column = 4, padx = 10, pady = 10)

		# button to show frame 2 with text
		# layout2
		button1 = ttk.Button(self, text ="Accueil",
							command = lambda : controller.show_frame(Accueil))
	
		# putting the button in its place
		# by using grid
		button1.grid(row = 1, column = 1, padx = 10, pady = 10)

		# button to show frame 2 with text
		# layout2
		button2 = ttk.Button(self, text ="Page 2",
							command = lambda : controller.show_frame(Page_Gestion))
	
        button_exit = ttk.button(self, text="Quitter", command = close)
        button_exit.pack()
        button_exit.grid(row = 3, column  = 1, padx =  10, pady=10)
 
		# putting the button in its place by
		# using grid
		button2.grid(row = 2, column = 1, padx = 10, pady = 10)




# third window frame Page_Gestion
class Page_Gestion(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = ttk.Label(self, text ="Page 2", font = LARGEFONT)
		label.grid(row = 0, column = 4, padx = 10, pady = 10)

		# button to show frame 2 with text
		# layout2
		button1 = ttk.Button(self, text ="Page 1",
							command = lambda : controller.show_frame(Page_Analyse))
	
		# putting the button in its place by
		# using grid
		button1.grid(row = 1, column = 1, padx = 10, pady = 10)

		# button to show frame 3 with text
		# layout3
		button2 = ttk.Button(self, text ="Accueil",
							command = lambda : controller.show_frame(Accueil))
	
		# putting the button in its place by
		# using grid
		button2.grid(row = 2, column = 1, padx = 10, pady = 10)
  
        button_exit = ttk.button(self, text="Quitter", command = close)
        button_exit.pack()
        button_exit.grid(row = 3, column  = 1, padx =  10, pady=10)


# Driver Code
app = tkinterApp()
app.mainloop()
