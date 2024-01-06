import tkinter as tk

def add_text_to_textbox(textbox, text="exempel text\n"):
    textbox.insert(tk.END, text)
    textbox.see(tk.END)