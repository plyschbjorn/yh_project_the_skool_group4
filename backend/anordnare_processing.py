import pandas as pd
from utils.constants import DATA_DIRECTORY

def load_anordnarstatistik(anordnare_namn, year):
    # Läs in data för det valda året
    path = DATA_DIRECTORY / f"resultat-{year}-for-kurser-inom-yh.xlsx"
    df = pd.read_excel(path)
    df["Årtal"] = df["Diarienummer"].str.extract(r'(\d{4})')

    # Filtrera på anordnare
    anordnar_df = df[df["Anordnare namn"].str.contains(anordnare_namn, case=False, na=False)]

    # Sammanfatta statistik
    total = anordnar_df.shape[0]
    approved = anordnar_df[anordnar_df["Beslut"] == "Beviljad"].shape[0]
    approved_ratio = approved / total if total else 0

    return anordnar_df, approved, total, approved_ratio