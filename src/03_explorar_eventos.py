
"""
Football Analytics Lab
Proyecto 01: Mundial de Qatar 2022

Objetivo:
Descargar los eventos de un partido y examinar
qué información contiene cada registro.
"""

import json
from pathlib import Path

import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# Leer la lista de partidos que descargamos anteriormente.
MATCHES_FILE = DATA_DIR / "matches_world_cup_2022.json"

# En este primer ejercicio usaremos el primer partido
# de la lista. No asumimos de antemano cuál es.
with MATCHES_FILE.open("r", encoding="utf-8") as file:
    matches = json.load(file)

match = matches[0]
match_id = match["match_id"]

# Construir la dirección de los eventos del partido.
URL = (
    "https://raw.githubusercontent.com/"
    "hudl/open-data/master/data/events/"
    f"{match_id}.json"
)

def main():
    print("Football Analytics Lab")
    print("-" * 40)

    # Mostrar qué partido estamos explorando.
    home_team = match.get("home_team", {}).get("home_team_name")
    away_team = match.get("away_team", {}).get("away_team_name")

    print(f"Partido seleccionado: {home_team} vs. {away_team}")
    print(f"Match ID: {match_id}")
    print()
    print("Descargando eventos...")

    response = requests.get(URL, timeout=30)
    response.raise_for_status()

    events = response.json()

    if not isinstance(events, list) or not events:
        raise ValueError("No encontramos una lista válida de eventos.")

    # Guardar los eventos originales en nuestro proyecto.
    output_file = DATA_DIR / f"events_{match_id}.json"

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(events, file, ensure_ascii=False, indent=2)

    print(f"Eventos descargados: {len(events)}")
    print(f"Archivo guardado: {output_file}")
    print()

    # Mostrar los campos que tiene el primer evento.
    first_event = events[0]

    print("Campos del primer evento:")
    for field in first_event.keys():
        print(f"- {field}")

    print()
    print("Ejemplo de evento:")
    print(json.dumps(first_event, ensure_ascii=False, indent=2))

    print()
    print("Exploración inicial completada.")


if __name__ == "__main__":
    main()
