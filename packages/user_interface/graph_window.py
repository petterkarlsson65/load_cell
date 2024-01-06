from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog


def save_graph(fig):
    """
    Öppnar en dialogruta för att spara den aktuella grafen som en bildfil.

    Args:
        fig (matplotlib.figure.Figure): Figure-objektet som innehåller grafen som ska sparas.
    """
    filetypes = [('PNG-bilder', '*.png'), ('Alla filer', '*.*')]
    filename = filedialog.asksaveasfilename(title="Spara grafen som", initialfile='graph.png', filetypes=filetypes)
    if filename:
        if not filename.endswith('.png'):
            filename += '.png'
        fig.savefig(filename)
        messagebox.showinfo("Sparad", f"Grafen har sparats som {filename}")


def update_graph(fig, ax, line, log_file_path):
    """
    Uppdaterar en matplotlib-graf med nya data från en loggfil.

    Läser tidsstämplade viktdata från en angiven loggfil och uppdaterar grafen med denna data.

    Args:
        fig (matplotlib.figure.Figure): En matplotlib-figur som innehåller grafen.
        ax (matplotlib.axes.Axes): En axel inom figuren som ska uppdateras.
        line (matplotlib.lines.Line2D): En linjeobjekt som representerar dataserien i grafen.
        log_file_path (tk.StringVar): En strängvariabel som innehåller sökvägen till loggfilen.

    Raises:
        Exception: Om ett fel uppstår vid läsning av loggfilen.
    """
    try:
        with open(log_file_path.get(), "r") as file:
            times = []
            values = []
            for line_text in file:
                parts = line_text.strip().split(',')
                if len(parts) == 2:
                    time = datetime.strptime(parts[0].strip(), '%Y-%m-%d %H:%M:%S.%f')
                    value = float(parts[1].strip())
                    times.append(time)
                    values.append(value)

            line.set_data(times, values)
            ax.relim()
            ax.autoscale_view()
            # Anpassa x-axeln
            ax.set_xlabel('Tid')
            ax.set_xticklabels([])  # Ta bort faktiska tidsvärden från x-axeln

            # ... [Din kod för att läsa och uppdatera grafen] ...

            # Stilinställningar
            ax.set_facecolor('whitesmoke')  # Bakgrundsfärg
            line.set_color('steelblue')  # Linjefärg
            line.set_marker('o')  # Typ av markörer
            line.set_markersize(5)  # Storlek på markörer
            line.set_linestyle('-')  # Typ av linje
            line.set_linewidth(2)  # Tjocklek på linjen

            # Typsnitt och text
            ax.set_xlabel('Tid', fontsize=12)
            ax.set_ylabel('Vikt [Kg]', fontsize=12, fontname='Arial')
            ax.set_title('Mätvärden över Tid', fontsize=14, fontweight='bold', fontname='Arial')

            # Layout och marginaler
            fig.tight_layout()

            # Lägg till rutnät
            ax.grid(True, linestyle='--', color='grey', alpha=0.5)

            # Uppdatera fig
            fig.canvas.draw()
    except Exception as e:
        messagebox.showerror("Fel", f"Kunde inte läsa data: {e}")


def open_graph_window(log_file_path, root):
    """
    Öppnar ett nytt Tkinter-fönster för att visa en matplotlib-graf över loggade data.

    Skapar en matplotlib-graf och en Tkinter-knapp för att uppdatera grafen med data från en angiven loggfil.

    Args:
        log_file_path (tk.StringVar): En strängvariabel som innehåller sökvägen till loggfilen.
        root (tk.Tk): Rot-Tkinter-objektet som fungerar som huvudfönstret för applikationen.

    Notes:
        Ett nytt Tkinter-fönster skapas med en matplotlib-graf inbäddad i det.
        Användaren kan uppdatera grafen med den senaste datan från loggfilen genom att klicka på en knapp.
    """
    graph_window = tk.Toplevel(root)
    graph_window.title("Loggad Data")

    fig, ax = plt.subplots(figsize=(10, 6))
    line, = ax.plot([], [], marker='o', color='b')
    ax.set_title('Mätvärden över Tid')
    ax.set_xlabel('Tid')
    ax.set_xticklabels([])  # Ta bort faktiska tidsvärden från x-axeln
    ax.set_ylabel('Vikt [Kg]')
    ax.grid(True)

    # Knapp för att uppdatera grafen
    update_button = tk.Button(graph_window, text="Uppdatera Graf",
                              command=lambda: update_graph(fig, ax, line, log_file_path))
    update_button.pack()

    # Knapp för att spara grafen
    save_button = tk.Button(graph_window, text="Spara Bild", command=lambda: save_graph(fig))
    save_button.pack()

    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)

    # Initiala stilinställningar
    ax.set_facecolor('whitesmoke')
    ax.grid(True, linestyle='--', color='grey', alpha=0.5)

    # ... [Resten av din kod] ...

    update_graph(fig, ax, line, log_file_path)  # Uppdatera grafen initialt
