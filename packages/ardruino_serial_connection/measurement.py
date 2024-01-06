from packages.ardruino_serial_connection.ardruino_serial_connection import read_average


def run_measurement(serial_connection, num_readings=10, k=1, m=1):
    """
    Kör en mätning genom att beräkna genomsnittsvärdet av flera avläsningar från en seriell anslutning och
    applicerar sedan en kalibreringsformel på detta värde.

    Args:
        serial_connection (serial.Serial): Ett Serial-objekt som representerar en aktiv seriell anslutning.
        num_readings (int, optional): Antalet avläsningar som ska användas för att beräkna genomsnittet. Standardvärdet är 10.
        k (float, optional): Skalfaktorn som används i kalibreringsformeln. Standardvärdet är 1.
        m (float, optional): Offsetvärdet som används i kalibreringsformeln. Standardvärdet är 1.

    Returns:
        float: Det kalibrerade mätvärdet efter att ha tillämpat skalfaktorn och offsetvärdet.

    Notes:
        Mätvärdet beräknas genom formeln 'k * measurement + m', där 'measurement' är genomsnittsvärdet
        från 'read_average'-funktionen. Denna formel tillämpar kalibreringsparametrarna på det råa mätvärdet.
    """
    measurement = read_average(serial_connection, num=num_readings)
    return k * measurement + m
