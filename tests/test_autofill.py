import tkinter as tk

chiefs = [
    'Sitting Bull', 'Geronimo', 'Tecumseh', 'Pontiac', 
    'Red Cloud', 'Crazy Horse', 'Cochise', 'Red Jacket', 
    'Red Czar', 'Red Czechoslovakian']

def match_string():
    hits = []
    got = auto.get()
    for item in chiefs:
        if item.startswith(got):
            hits.append(item)
    return hits    

def get_typed(event):
    if len(event.keysym) == 1:
        hits = match_string()
        show_hit(hits)

def show_hit(lst):
    if len(lst) == 1:
        auto.set(lst[0])
        detect_pressed.filled = True

def detect_pressed(event):    
    key = event.keysym
    if len(key) == 1 and detect_pressed.filled is True:
        pos = autofill.index(tk.INSERT)
        autofill.delete(pos, tk.END)

detect_pressed.filled = False

root = tk.Tk()

auto = tk.StringVar()

autofill = tk.Entry(
    root, 
    font=('tacoma', 30),
    bg='black',
    insertbackground='white',
    fg='white',
    textvariable=auto)
autofill.grid()
autofill.focus_set()
autofill.bind('<KeyRelease>', get_typed)
autofill.bind('<Key>', detect_pressed)

root.mainloop()