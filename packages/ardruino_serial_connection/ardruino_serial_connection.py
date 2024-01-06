import serial
import numpy as np


def connect_serial(port, add_text_callback):
    """
    Upprättar en seriell anslutning till en angiven port.

    Args:
        port (str): Den port till vilken anslutningen ska upprättas.
        add_text_callback (function): En callback-funktion som tar emot en sträng för att visa meddelanden.

    Returns:
        serial.Serial: Ett Serial-objekt representerande anslutningen.

    Raises:
        ValueError: Om det angivna baudrate är ogiltigt.
        Exception: För alla övriga fel som kan uppstå vid försök att upprätta anslutningen.
    """
    baud = 115200
    serial_connection = None
    try:
        # Försök stänga en befintlig anslutning (om den finns)
        serial_connection.close()
        wait(1)
    except Exception:
        pass

    try:
        serial_connection = serial.Serial(port, baud, timeout=1)
        add_text_callback(f"Ansluten till {port} med baudrate {baud}\n")
    except ValueError:
        add_text_callback("Ogiltigt baudrate.\n")
    except Exception as e:
        add_text_callback(f"Kunde inte ansluta: {e}\n")

    return serial_connection


def read_from_arduino(serial_connection):
    """
    Läser en rad data från den angivna seriella anslutningen.

    Args:
        serial_connection (serial.Serial): Ett Serial-objekt som representerar en aktiv seriell anslutning.

    Returns:
        str: En sträng som innehåller den lästa raden.
    """
    if serial_connection.in_waiting > 0:
        line = serial_connection.readline().decode('utf-8').rstrip()
        return line


def read_average(serial_connection, num=10):
    """
    Beräknar genomsnittsvärdet av en serie viktläsningar från Arduino.

    Args:
        serial_connection (serial.Serial): Ett Serial-objekt som representerar en aktiv seriell anslutning.
        num (int, optional): Antalet viktläsningar för att beräkna genomsnittet. Standardvärdet är 10.

    Returns:
        float: Genomsnittsvärdet av de inlästa vikterna.

    Notes:
        Om ogiltiga data mottas under läsning, kommer dessa att ignoreras.
    """
    while serial_connection.in_waiting > 0:
        serial_connection.readline()
    values = []
    while len(values) < num:
        data = read_from_arduino(serial_connection)
        if data:
            try:
                weight = data
            except Exception:
                continue
            values.append(float(weight))
    mean = np.mean(values)
    return mean
