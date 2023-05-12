import tkinter as tk
from tkinter import messagebox

root = tk.Tk()

def popup_message():
    messagebox.showinfo("Titre de la fenêtre", "Contenu du message")

popup_button = tk.Button(root, text="Afficher la pop-up", command=popup_message)
popup_button.pack()

root.mainloop()
