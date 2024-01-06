# Lastcell Applikation

## Beskrivning
Lastcell är en applikation utvecklad för att mäta och logga vikter via en seriell anslutning. Applikationen erbjuder realtidsmätning, datalogging, grafvisning och kalibreringsfunktioner.

## Funktioner
- **Anslutning till Seriell Port**: Möjliggör kommunikation med en ansluten lastcell.
- **Kalibrering**: Kalibrerar lastcellen för noggranna mätningar.
- **Viktloggning**: Loggar viktmätningar i realtid med möjlighet att spara datan till en fil.
- **Visa Graf**: Visar en graf över loggade viktmätningar.
- **Exportera Data**: Exporterar insamlad data till en textfil för vidare analys.

## Installation
För att installera och köra Lastcell, följ dessa steg:

1. Klona repo:
git clone [Repo-URL]
2. Installera nödvändiga beroenden (t.ex. via `requirements.txt` om tillgängligt):
pip install -r requirements.txt
3. Kör applikationen:
python main.py


## Användning
För att använda Lastcell, följ dessa grundläggande steg:

1. Starta programmet.
2. Anslut till den seriella porten där lastcellen är ansluten.
3. Kalibrera enheten vid behov.
4. Starta mätning och/eller loggning av data.
5. Visa mätdata i grafisk form vid behov.

## Utveckling
Denna applikation är utvecklad med Python och använder Tkinter för grafiskt användargränssnitt. Ytterligare bibliotek som används inkluderar `matplotlib` för grafhantering och `pyserial` för seriell kommunikation.

## Kompilering till .exe
Programmet kan kompileras till en .exe-fil med ``pyinstaller``:

``
pyinstaller --onefile --name=LoadCellApp --icon=favicon.ico --add-data="favicon.ico;." main.py``