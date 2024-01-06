import tkinter as tk
from tkinter import filedialog

from packages.tooltip import Tooltip
from packages.ardruino_serial_connection.ardruino_serial_connection import connect_serial
from packages.ardruino_serial_connection.calibration import read_calibrated_values
from packages.user_interface.calibrate import run_calibration_gui
from packages.user_interface.logging import start_logging, stop_logging
from packages.user_interface.core import add_text_to_textbox
from packages.ardruino_serial_connection.measurement import run_measurement
from packages.user_interface.graph_window import open_graph_window

# ... [Dina tidigare funktioner, inklusive run_calibration och run_measurement]
threshold = 1.0  # Exempel på tröskelvärde, ändra efter behov
serial_connection = None  # Global variabel
num_readings = 1

try:
    calibrated = read_calibrated_values()
    k = calibrated["k"]
    m = calibrated["m"]
    print(f"Loaded calibrated values (k={k}, m={m})")
except Exception:
    pass


def connect(textbox, port_entry):
    global serial_connection
    serial_connection = connect_serial(port_entry.get(), lambda text: add_text_to_textbox(textbox, text))


# Define functions for what should happen when buttons are pressed
def on_weigh_click():
    global num_readings, k, m
    num_readings = int(readings_entry.get())
    measurement = run_measurement(serial_connection, num_readings, k, m)
    add_text_to_textbox(textbox, f"Mätt: {measurement:.3f} kg\n")


def on_log_click():
    global threshold, num_readings, k, m
    threshold = float(threshold_entry.get())
    num_readings = int(readings_entry.get())
    start_logging(log_file_path, textbox, serial_connection, num_readings, k, m, threshold, root)
    add_text_to_textbox(textbox, "Loggning startad. Tryck 'q' för att avsluta.\n")


def on_stop_click():
    stop_logging(textbox, root)


def on_calibration_click():
    global k, m
    k,m = run_calibration_gui(serial_connection, num_readings, textbox)


def on_connect_click():
    connect(textbox, port_entry)


def on_show_graph_click():
    open_graph_window(log_file_path, root)


def choose_log_file():
    filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if filename:
        log_file_path.set(filename)


# Create GUI
root = tk.Tk()
root.geometry("800x800")
root.title("Lastcell v1.0")
root.configure(bg='#f0f0f0')  # Ljus bakgrund

# Define fonts
default_font = ('Helvetica', 12)
button_font = ('Helvetica', 14, 'bold')

# Set dialogue window title (what it says at the top)
label = tk.Label(root, text="Lastcell", font=('times new roman', 40))
label.pack(padx=30, pady=30)

# Ny etikett för programinformation
info_text = "Detta program används för att mäta och logga vikter.\n Koden finns här http://github.com/petter.karlsson65/..."
info_label = tk.Label(root, text=info_text, font=('Arial', 12))  # Använd en mindre fontstorlek för info-texten
info_label.pack(padx=20, pady=10)  # Justera paddings efter behov

# Connection section
connection_frame = tk.LabelFrame(root, text="Anslutning", font=default_font, bg='#f0f0f0', padx=10, pady=10)
connection_frame.pack(fill='x', padx=10, pady=5)

connect_button = tk.Button(connection_frame, text="Anslut", command=on_connect_click, font=button_font, bg="#add8e6")
connect_button.pack(side='right')
tooltip = Tooltip(connect_button, "Klicka här för att ansluta")

# COM-port section
port_label = tk.Label(connection_frame, text="COM-port:", font=default_font, bg='#f0f0f0')
port_label.pack(side='left')

port_entry = tk.Entry(connection_frame, font=default_font)
port_entry.pack(side='left', padx=(0, 10))
port_entry.insert(0, "COM3")

# Log-file selection section
log_file_path = tk.StringVar()  # Skapar en variabel för att lagra loggfilens sökväg

log_file_frame = tk.LabelFrame(root, text="Loggfil", font=default_font, bg='#f0f0f0', padx=10, pady=10)
log_file_frame.pack(fill='x', padx=10, pady=5)

log_file_entry = tk.Entry(log_file_frame, textvariable=log_file_path, font=default_font)
log_file_entry.pack(side='left', fill='x', expand=True)

log_file_button = tk.Button(log_file_frame, text="Bläddra...", command=choose_log_file, font=button_font, bg="#add8e6")
log_file_button.pack(side='left')

# Control button section
button_frame = tk.Frame(root, bg='#f0f0f0', padx=10, pady=10)
button_frame.pack(fill='x', padx=10, pady=5)

calibrate_button = tk.Button(button_frame, text="Kalibrera", command=on_calibration_click, font=button_font,
                             bg="#90ee90")
calibrate_button.pack(side='left', fill='x', expand=True)
tooltip = Tooltip(calibrate_button, "Kalibrera: Ange vikten i [kg]")

weigh_button = tk.Button(button_frame, text="Väga", command=on_weigh_click, font=button_font, bg="#90ee90")
weigh_button.pack(side='left', fill='x', expand=True)

log_button = tk.Button(button_frame, text="Logga", command=on_log_click, font=button_font, bg="#90ee90")
log_button.pack(side='left', fill='x', expand=True)
tooltip = Tooltip(log_button, "Loggar endast vid vikt över tröskelvärde")

stop_button = tk.Button(button_frame, text="Stopp", command=on_stop_click, font=button_font, bg="#ff6347")
stop_button.pack(side='left', fill='x', expand=True)
tooltip = Tooltip(stop_button, "Avsluta loggning")

show_graph_button = tk.Button(button_frame, text="Visa Graf", command=on_show_graph_click, font=button_font,
                              bg="#ff6347")
show_graph_button.pack(side='left', fill='x', expand=True)
tooltip = Tooltip(show_graph_button, "Plotta mätvärden i vald log-fil")

# Threshold section
settings_frame = tk.LabelFrame(root, text="Settings", font=default_font, bg='#f0f0f0', padx=10, pady=10)
settings_frame.pack(fill='x', padx=10, pady=5)

threshold_label = tk.Label(settings_frame, text="Tröskelvärde [kg]:", font=default_font, bg='#f0f0f0')
threshold_label.pack(side='left')

threshold_entry = tk.Entry(settings_frame, font=default_font)
threshold_entry.pack(side='left')
threshold_entry.insert(0, "1.0")  # Standardvärde

readings_label = tk.Label(settings_frame, text="Antal mätpunkter:", font=default_font, bg='#f0f0f0')
readings_label.pack(side='left')

readings_entry = tk.Entry(settings_frame, font=default_font)
readings_entry.pack(side='left')
readings_entry.insert(0, "1")  # Standardvärde
tooltip = Tooltip(readings_entry, "Medelvärde beräknas av antalet mätpunkter")


# Textbox section
textbox = tk.Text(root, height=5, font=default_font)
textbox.pack(fill='both', expand=True, padx=10, pady=5)

# Run main-loop
root.mainloop()
