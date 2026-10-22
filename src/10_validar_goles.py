
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

df = pd.read_csv(DATA_DIR / "resumen_por_partido.csv")

equipos = ["Canada", "Australia", "Costa Rica"]

casos = df[df["equipo"].isin(equipos)].copy()
casos["diferencia_goles"] = (
    casos["goles_oficiales"] - casos["goles_de_remate"]
)

print("PARTIDOS CON DIFERENCIAS ENTRE GOLES OFICIALES Y DE REMATE")
print("=" * 70)

print(
    casos.loc[
        casos["diferencia_goles"] != 0,
        [
            "fecha",
            "partido_id",
            "equipo",
            "goles_oficiales",
            "goles_de_remate",
            "diferencia_goles",
            "xG",
        ],
    ].to_string(index=False)
)
