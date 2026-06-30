from tkinter import Tk, Label
from PIL import Image, ImageTk
import os

root = Tk()
root.title("fly-in")
root.geometry("800x600")

root.bind("<Escape>", lambda e: root.destroy())

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(BASE_DIR, "..", "assets", "background.png")

screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

img = Image.open(img_path)

img = img.resize((screen_w, screen_h), Image.Resampling.LANCZOS)

photo = ImageTk.PhotoImage(img)

label = Label(root, image=photo)
label.place(x=0, y=0, relwidth=1, relheight=1)

label.image = photo

root.mainloop()