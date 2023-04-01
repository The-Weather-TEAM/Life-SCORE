import pyglet,tkinter,os


nom_du_repertoire = os.path.dirname(__file__) + '/polices'
print(nom_du_repertoire)

print(pyglet.font.have_font('Montez'))
pyglet.font.add_directory(nom_du_repertoire)
print(pyglet.font.have_font('Montez'))

   
root = tkinter.Tk()
MyLabel = tkinter.Label(root,text="test",font=('Montez',25))
MyLabel.pack()
root.mainloop()