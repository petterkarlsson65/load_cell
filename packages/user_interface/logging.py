from packages.user_interface.core import add_text_to_textbox
from packages.ardruino_serial_connection.measurement import run_measurement
from datetime import datetime

stop_logging = False  # En flagga för att kontrollera om loggningen ska stoppas


def log_data(serial_connection, num_readings, k, m, threshold, log_file_path, textbox, root):
    """
    Loggar mätdata kontinuerligt till en angiven fil och visar loggmeddelanden i en Tkinter-textbox.

    Denna funktion läser mätningar, kontrollerar om de överstiger en tröskelvärde och loggar dem med tidsstämplar
    om de gör det. Funktionen upprepar sig själv med ett intervall på 100 ms.

    Args:
        serial_connection (serial.Serial): En seriell anslutning för att läsa data.
        num_readings (int): Antal avläsningar för att beräkna ett genomsnittsvärde.
        k (float): Kalibreringsfaktor.
        m (float): Kalibreringsoffset.
        threshold (float): Tröskelvärde för att avgöra om en mätning ska loggas.
        log_file_path (tk.StringVar): Sökvägen till loggfilen.
        textbox (tk.Text): Tkinter-textbox för att visa loggmeddelanden.
        root (tk.Tk): Tkinter-root-objektet för att schemalägga upprepade mätningar.

    Notes:
        Använder globala variabler 'stop_logging' och 'log_job' för att kontrollera loggprocessen.
    """
    global stop_logging, log_job  # Använda globala variabler
    if stop_logging:
        return  # Avbryt loggningen om stop-flaggan är satt

    measurement = run_measurement(serial_connection, num_readings, k, m)
    if abs(measurement) > threshold:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Inkluderar millisekunder
        with open(log_file_path.get(), "a") as file:
            file.write(f"{current_time}, {measurement:.3f}\n")
            add_text_to_textbox(textbox, f"Logged: {measurement:.3f} kg\n")

    log_job = root.after(100, lambda: log_data(serial_connection, num_readings, k, m, threshold, log_file_path, textbox,
                                               root))


def start_logging(log_file_path, textbox, serial_connection, num_readings, k, m, threshold, root):
    """
    Startar en loggprocess genom att kalla på 'log_data'-funktionen.

    Denna funktion kontrollerar om en giltig filväg har angivits och initierar sedan loggningen om så är fallet.

    Args:
        log_file_path (tk.StringVar): Sökvägen till loggfilen.
        textbox (tk.Text): Tkinter-textbox för att visa loggmeddelanden.
        serial_connection (serial.Serial): En seriell anslutning för att läsa data.
        num_readings (int): Antal avläsningar för att beräkna ett genomsnittsvärde.
        k (float): Kalibreringsfaktor.
        m (float): Kalibreringsoffset.
        threshold (float): Tröskelvärde för att avgöra om en mätning ska loggas.
        root (tk.Tk): Tkinter-root-objektet för att schemalägga upprepade mätningar.

    Notes:
        Funktionen kontrollerar om användaren har valt en loggfil innan den startar loggningen.
    """
    global is_logging_active
    if not log_file_path.get():
        messagebox.showwarning("Ingen fil vald", "Vänligen välj en fil att logga till.")
        return  # Avsluta funktionen om ingen filväg är angiven

    global stop_logging
    stop_logging = False
    is_logging_active = True  # Uppdatera loggningstillståndet
    add_text_to_textbox(textbox, "Loggning startad.\n")
    log_data(serial_connection, num_readings, k, m, threshold, log_file_path, textbox, root)  # Starta loggningen


def stop_logging(textbox, root):
    """
    Stoppar loggningen genom att sätta en global flagga och avbryta den schemalagda mätningen.

    Args:
        textbox (tk.Text): Tkinter-textbox för att visa loggmeddelanden.
        root (tk.Tk): Tkinter-root-objektet som använts för att schemalägga mätningen.

    Notes:
        Använder globala variabler 'stop_logging' och 'log_job' för att kontrollera loggprocessen.
    """
    global stop_logging, log_job
    stop_logging = True
    if log_job is not None:
        root.after_cancel(log_job)  # Avbryt schemalagd mätning
    add_text_to_textbox(textbox,"Loggning stoppad.\n")
