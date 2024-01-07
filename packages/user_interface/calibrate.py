import os
import json
from packages.ardruino_serial_connection.ardruino_serial_connection import read_average
from packages.ardruino_serial_connection.calibration import calibrate_scale
from packages.user_interface.utils import add_text_to_textbox

def run_calibration_gui(serial_connection, num_readings, textbox, root):
    """
    Kör en GUI-baserad kalibreringsprocess för en våg ansluten via en seriell port.

    Denna funktion använder Tkinter dialogrutor för att interagera med användaren under kalibreringsprocessen.
    Den ber användaren först nollställa vågen och sedan ange en känd vikt för kalibrering.

    Args:
        serial_connection (serial.Serial): Ett Serial-objekt som representerar en aktiv seriell anslutning.
        num_readings (int): Antalet avläsningar som ska användas för att beräkna genomsnittet vid varje kalibreringssteg.
        textbox (tkinter.Text): Ett Text-widget i Tkinter för att visa statusmeddelanden.

    Returns:
        tuple: Ett tuple med två float-värden (k, m) som representerar de kalibrerade värdena.

    Notes:
        Funktionen utför följande steg:
        1. Frågar användaren att nollställa vågen och tar sedan ett genomsnittsvärde för nollavläsningen.
        2. Frågar användaren att placera en känd vikt på vågen och tar ett genomsnittsvärde för denna viktavläsning.
        3. Beräknar kalibreringskoefficienterna (k och m) och sparar dessa i en JSON-fil.
        4. Visar en bekräftelse i GUI om att vågen har kalibrerats och värdena har sparats.
    """
    global k, m  # Använd globala variabler för att spara kalibrerade värden
    from tkinter import simpledialog
    _ = simpledialog.askfloat("Kalibrering", "Nollställ vågen och klicka på OK", parent=root)

    try:
        zero_reading = read_average(serial_connection, num=num_readings)
    except Exception as e:
        add_text_to_textbox(textbox, f"Kolla så att du är ansluten till COM-porten, fel: {e}.")

    weight_answer = simpledialog.askfloat("Kalibrering", "Lägg på en känd vikt och skriv värdet i kg:", parent=root)

    weight = float(weight_answer)

    weight_reading = read_average(serial_connection, num=num_readings)

    k, m = calibrate_scale(zero_reading, weight_reading, weight)
    # Resten av koden för att spara kalibrerade värden
    file_path = os.path.join("calibrated_values.json")
    with open(file_path, "w") as f:
        json.dump({"k": k, "m": m}, f)

    add_text_to_textbox(textbox, f"Vågen är nu kalibrerad (k={k}, m={m}) och värdena är sparade i {file_path}.\n")
    return k, m