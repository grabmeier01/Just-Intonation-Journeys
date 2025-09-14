#!/usr/bin/env python3
import re
import tkinter as tk
from tkinter import scrolledtext

# -----------------------------------------------------------------------------
# Konfiguration
# -----------------------------------------------------------------------------
SKIP_EVERY_NTH = False   # Setze auf True, um das Entfernen jedes n-ten Synth zu aktivieren.
NTH_TO_SKIP = 7          # Standardwert: jedes 7. Element wird entfernt.
SYNTH_DEF = "def1"  # Name des Synth-Definitions-Symbols in SuperCollider.
# -----------------------------------------------------------------------------

def parse_chords(raw: str):
    """
    Sucht in raw alle Vorkommen von (Zahl Zahl Zahl)
    und liefert eine Liste von [Float, Float, Float].
    """
    
    pattern = re.compile(
        r'\(\s*([-+]?\d+(?:\.\d+)?)\s+'    # erste Zahl
        r'([-+]?\d+(?:\.\d+)?)\s+'        # zweite Zahl
        r'([-+]?\d+(?:\.\d+)?)\s+'        # dritte Zahl
        r'([-+]?\d+(?:\.\d+)?)\s*\)'      # vierte Zahl
        )
    matches = pattern.findall(raw)
    if not matches:
        raise ValueError("Keine gültigen Dreiergruppen im Input gefunden.")
    return [[float(a), float(b), float(c), float(d)] 
            for a, b, c, d in matches]
def build_synth_lines(chords):
    """
    Baut aus [[x,y,z], …] einen einzigen großen String mit den Synth-Aufrufen.
    Jeder n-te Synth-Aufruf wird entfernt, wenn SKIP_EVERY_NTH == True.
    """
    lines = []
    for idx, chord in enumerate(chords):
        # --- Bereich zum Auskommentieren START ---
        if SKIP_EVERY_NTH and NTH_TO_SKIP > 0 and ((idx + 1) % NTH_TO_SKIP == 0):
            continue
        # --- Bereich zum Auskommentieren ENDE ---

        lines.append(f"Synth(\\{SYNTH_DEF}, [\\freq, {chord}]);")

        lines.append("~waittime.wait;")
    return "\n".join(lines)

def show_in_window(text):
    """
    Öffnet ein Tkinter-Fenster mit einem scrollbaren Textfeld, in das text eingefügt wird.
    """
    root = tk.Tk()
    root.title("Generated Synth Lines")
    txt = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
    txt.insert(tk.INSERT, text)
    txt.configure(state='disabled')
    txt.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    root.mainloop()

if __name__ == "__main__":
    print("Füge deinen Lisp-Style-String ein (beende mit leerer Zeile):")
    buffer = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line.strip():
            break
        buffer.append(line)
    raw_input = "\n".join(buffer)

    try:
        chords = parse_chords(raw_input)
    except Exception as e:
        print("Fehler beim Parsen:", e)
        exit(1)

    result = build_synth_lines(chords)
    show_in_window(result)

# Lizenz GNU General Public License v3.0
# (c) 2024 by Cajus Grabmeier
# https://www.gnu.org/licenses/gpl-3.0.html
