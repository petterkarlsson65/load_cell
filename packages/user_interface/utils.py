import tkinter as tk
import webbrowser

def add_text_to_textbox(textbox, text="exempel text\n"):
    textbox.insert(tk.END, text)
    textbox.see(tk.END)

def open_link(url):
    webbrowser.open_new(url)