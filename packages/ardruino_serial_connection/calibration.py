import os
import json

def calibrate_scale(zero_reading, weight_reading, weight):
    """
    Kalibrerar en skala genom att beräkna koefficienter baserat på nollavläsning, viktavläsning och faktisk vikt.

    Args:
        zero_reading (float): Avläsning från skalan när ingen vikt är applicerad (nollavläsning).
        weight_reading (float): Avläsning från skalan när en känd vikt är applicerad.
        weight (float): Den faktiska vikten som applicerades på skalan under kalibreringen.

    Returns:
        tuple: Ett tuple med två float-värden (k, m) där 'k' är skalfaktorn och 'm' är offsetvärdet.

    Notes:
        Formeln för kalibrering är k = weight / (weight_reading - zero_reading) och m = -k * zero_reading.
    """
    k = weight / (weight_reading - zero_reading)
    m = -k * zero_reading
    return k, m


def read_calibrated_values():
    """
    Läser kalibrerade värden från en JSON-fil.

    Filen förväntas innehålla ett JSON-objekt med kalibrerade värden.

    Returns:
        dict: En ordbok som innehåller kalibrerade värden.

    Raises:
        FileNotFoundError: Om filen inte finns.
        json.JSONDecodeError: Om filen inte innehåller giltig JSON.

    Notes:
        Filen antas finnas i samma mapp som detta skript, med namnet 'calibrated_values.json'.
    """
    file_path = os.path.join("calibrated_values.json")
    with open(file_path, "r") as f:
        calibrated = json.load(f)
    return calibrated
