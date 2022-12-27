#Import required library
from tkinter import *
from tkinter import font
#Create an instance of tkinter frame
win = Tk()
win.geometry("750x350")
win.title('Font List')
#Create a list of font using the font-family constructor
fonts=list(font.families())
fonts.sort()
def fill_frame(frame):
   for f in fonts:
      #Create a label to display the font
      label = Label(frame,text=f'{f} 1234567890',font=(f, 14)).pack()
def onFrameConfigure(canvas):
   canvas.configure(scrollregion=canvas.bbox("all"))
#Create a canvas
canvas = Canvas(win,bd=1, background="white")
#Create a frame inside the canvas
frame = Frame(canvas, background="white")
#Add a scrollbar
scroll_y = Scrollbar(win, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scroll_y.set)
scroll_y.pack(side="right", fill="y")
canvas.pack(side="left", expand=1, fill="both")
canvas.create_window((5,4), window=frame, anchor="n")
frame.bind("<Configure>", lambda e, canvas=canvas: onFrameConfigure(canvas))
fill_frame(frame)
win.mainloop()