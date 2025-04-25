from tkinter import *
from tkinter import ttk

win = Tk()
win.title("My project")
win.geometry("500x300")
win.resizable()


nap = Label(win, text="Текст для напису", font=("Comic Sans MS", 20), bg="green", fg="white")
nap.place(relx=0.1, rely=0.4)

ent = Entry(win, font=("Comic Sans MS", 20), width=10)
ent.place(relx=0.1, rely=0.2)

btn = Button(win, text="Click", font=("Comic Sans MS", 20), width=7, height=3, background="red", foreground="red")
btn.place(relx=0.1, rely=0.6)

cmb = ttk.Combobox(win, values=["hi", "hi2"], font=("Comic Sans MS", 20), width=7)
cmb.place(relx=0.4, rely=0.6)

win.mainloop()