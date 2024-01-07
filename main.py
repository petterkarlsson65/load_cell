import tkinter as tk
from tkinter import filedialog, Frame
import sys
import os
from tkinter import PhotoImage

from packages.tooltip import Tooltip
from packages.ardruino_serial_connection.ardruino_serial_connection import connect_serial
from packages.ardruino_serial_connection.calibration import read_calibrated_values
from packages.user_interface.calibrate import run_calibration_gui
from packages.user_interface.logging import start_logging, stop_logging
from packages.user_interface.utils import add_text_to_textbox, open_link
from packages.ardruino_serial_connection.measurement import run_measurement
from packages.user_interface.graph_window import open_graph_window

serial_connection = None  # Global variabel


def connect(textbox, port_entry):
    global serial_connection, k, m
    serial_connection = connect_serial(port_entry.get(), lambda text: add_text_to_textbox(textbox, text))
    try:
        calibrated = read_calibrated_values()
        k = calibrated["k"]
        m = calibrated["m"]
        add_text_to_textbox(textbox,f"Loaded calibrated values (k={k}, m={m})\n")
    except Exception as e:
        add_text_to_textbox(textbox, f"Kalibrering krävs! Fel: {e}\n")


# Define functions for what should happen when buttons are pressed
def on_weigh_click():
    global num_readings, k, m
    try:
        num_readings = int(readings_entry.get())
        measurement = run_measurement(serial_connection, num_readings, k, m)
        add_text_to_textbox(textbox, f"Mätt: {measurement:.3f} kg\n")
    except ValueError:
        add_text_to_textbox(textbox, "Ogiltigt värde för antal mätpunkter. Ange ett heltal.\n")


def on_log_click():
    global threshold, num_readings, k, m
    try:
        threshold = float(threshold_entry.get())
        num_readings = int(readings_entry.get())
        start_logging(log_file_path, textbox, serial_connection, num_readings, k, m, threshold, root)
        add_text_to_textbox(textbox, "Loggning startad. Tryck 'q' för att avsluta.\n")
    except ValueError:
        add_text_to_textbox(textbox, "Ogiltigt värde för tröskelvärde eller antal mätpunkter.\n")


def on_stop_click():
    stop_logging(textbox, root)


def on_calibration_click():
    global k, m
    num_readings = int(readings_entry.get())
    k, m = run_calibration_gui(serial_connection, num_readings, textbox, root)


def on_connect_click():
    connect(textbox, port_entry)


def on_show_graph_click():
    open_graph_window(log_file_path, root)


def on_choose_log_file_click():
    filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if filename:
        log_file_path.set(filename)


# Define color-palette
background_color = '#f0f0f0'
button_color = '#add8e6'
button_active_color = '#87CEEB'
highlight_color = '#90ee90'
danger_color = '#ff6347'


def resource_path(relative_path):
    """ Hämtar den absoluta sökvägen till resursen för kompilerade applikationer. """
    try:
        # PyInstaller skapar en temporär mapp och lagrar sökvägen i _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


icon_path = resource_path('favicon.ico')

# Create GUI
root = tk.Tk()
root.geometry("900x800")
root.title("Lastcell v1.0")
root.configure(bg=background_color)
root.iconbitmap(icon_path)

# Define fonts
default_font = ('Arial', 12)
title_font = ('Arial', 14, 'bold')
button_font = ('Arial', 12, 'bold')


# Skapa en Frame för logga och titel
header_frame = Frame(root, bg=background_color)
header_frame.pack(fill='x', padx=10, pady=10)

# Frame för logga
logo_frame = Frame(header_frame, bg=background_color)
logo_frame.pack(side='left', padx=10, pady=10)

# Logga
logo_path = resource_path('transparent_icon_120_120.png')
logo_image = PhotoImage(file=logo_path)
logo_label = tk.Label(logo_frame, image=logo_image, bg=background_color)
logo_label.pack(side='top', padx=10, pady=10)

# Frame för titel och beskrivande text
title_text_frame = Frame(header_frame, bg=background_color)
title_text_frame.pack(side='left', padx=10, pady=10)

# Titel
label = tk.Label(title_text_frame, text="Lastcell: Balkböjare", font=title_font, bg=background_color)
label.pack(side='top', padx=10, pady=10)

# Beskrivande text under titeln
info_text_widget = tk.Text(title_text_frame, height=4, wrap='word', background=root.cget('bg'), relief='flat', font=default_font, cursor="arrow")
info_text_widget.insert(tk.END, "Detta program används för att mäta och logga vikter från en lastcell via en A/D-omvandlare HX711 som läses av en Arduino.\nKoden finns här: ")
info_text_widget.insert(tk.INSERT, "GitHub", ("link",))
info_text_widget.tag_config("link", foreground="blue", underline=1)
info_text_widget.tag_bind("link", "<Button-1>", lambda e: open_link("https://github.com/petterkarlsson65/load_cell"))
info_text_widget.configure(state="disabled", inactiveselectbackground=info_text_widget.cget("selectbackground"))
info_text_widget.pack(side='top', padx=10, pady=10)


# Connection section
connection_frame = tk.LabelFrame(root, text="Anslutning", font=default_font, padx=10, pady=10)
connection_frame.pack(fill='x', padx=10, pady=5)

connect_button = tk.Button(connection_frame, text="Anslut", command=on_connect_click, font=button_font)
connect_button.pack(side='right')
tooltip = Tooltip(connect_button, "Klicka här för att ansluta")

# COM-port section
port_label = tk.Label(connection_frame, text="COM-port:", font=default_font)
port_label.pack(side='left')

port_entry = tk.Entry(connection_frame, font=default_font)
port_entry.pack(side='left', padx=(0, 10))
port_entry.insert(0, "COM3")

# Log-file selection section
log_file_path = tk.StringVar()  # Skapar en variabel för att lagra loggfilens sökväg

log_file_frame = tk.LabelFrame(root, text="Loggfil", font=default_font, padx=10, pady=10)
log_file_frame.pack(fill='x', padx=10, pady=5)

log_file_entry = tk.Entry(log_file_frame, textvariable=log_file_path, font=default_font)
log_file_entry.pack(side='left', fill='x', expand=True)

log_file_button = tk.Button(log_file_frame, text="Bläddra...", command=on_choose_log_file_click, font=button_font)
log_file_button.pack(side='left')

# Control button section
button_frame = tk.Frame(root, padx=10, pady=10)
button_frame.pack(fill='x', padx=10, pady=5)

calibrate_button = tk.Button(button_frame, text="Kalibrera", command=on_calibration_click, font=button_font)
calibrate_button.pack(side='left', fill='x', expand=True)
tooltip = Tooltip(calibrate_button, "Kalibrera: Ange vikten i [kg]")

weigh_button = tk.Button(button_frame, text="Väga", command=on_weigh_click, font=button_font)
weigh_button.pack(side='left', fill='x', expand=True)

log_button = tk.Button(button_frame, text="Logga", command=on_log_click, font=button_font)
log_button.pack(side='left', fill='x', expand=True)
tooltip = Tooltip(log_button, "Loggar endast vid vikt över tröskelvärde")

stop_button = tk.Button(button_frame, text="Sluta logga", command=on_stop_click, font=button_font)
stop_button.pack(side='left', fill='x', expand=True)
tooltip = Tooltip(stop_button, "Avsluta loggning")

show_graph_button = tk.Button(button_frame, text="Visa Graf", command=on_show_graph_click, font=button_font)
show_graph_button.pack(side='left', fill='x', expand=True)
tooltip = Tooltip(show_graph_button, "Plotta mätvärden i vald log-fil")

# Threshold section
settings_frame = tk.LabelFrame(root, text="Inställningar", font=default_font, padx=10, pady=10)
settings_frame.pack(fill='x', padx=10, pady=5)

threshold_label = tk.Label(settings_frame, text="Tröskelvärde [kg]:", font=default_font)
threshold_label.pack(side='left')

threshold_entry = tk.Entry(settings_frame, font=default_font)
threshold_entry.pack(side='left')
threshold_entry.insert(0, "1.0")  # Standardvärde
tooltip = Tooltip(threshold_entry, "Loggning sker endast om absolutbeloppet av vikten överstiger tröskelvärdet")

readings_label = tk.Label(settings_frame, text="Antal mätpunkter:", font=default_font)
readings_label.pack(side='left')

readings_entry = tk.Entry(settings_frame, font=default_font)
readings_entry.pack(side='left')
readings_entry.insert(0, "1")  # Standardvärde
tooltip = Tooltip(readings_entry, "Medelvärde beräknas av antalet mätpunkter")

# Set colors of buttons
connect_button.configure(bg=button_color, activebackground=button_active_color)
log_file_button.configure(bg=button_color, activebackground=button_active_color)
calibrate_button.configure(bg=highlight_color, activebackground=button_active_color)
weigh_button.configure(bg=highlight_color, activebackground=button_active_color)
log_button.configure(bg=highlight_color, activebackground=button_active_color)
stop_button.configure(bg=danger_color, activebackground=button_active_color)
show_graph_button.configure(bg=highlight_color, activebackground=button_active_color)

# Textbox section
textbox = tk.Text(root, height=5, font=default_font)
textbox.pack(fill='both', expand=True, padx=10, pady=5)

# Notis längst ned på sidan
footer_text = "Petter Karlsson - Soltorgsgymnasiet - 2024"
footer_label = tk.Label(root, text=footer_text, font=('Arial', 8), bg=background_color)
footer_label.pack(side='bottom', anchor='e', padx=10, pady=5)

# Run main-loop
root.mainloop()
