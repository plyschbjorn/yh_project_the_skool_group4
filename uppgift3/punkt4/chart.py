import pandas as pd
from pathlib import Path
from taipy.gui import Gui



PROJECT_ROOT = Path(r"C:\Users\azizm\Documents\github\yh_project_the_skool_group4")
FILES_DIR = PROJECT_ROOT / "files"
DATA_DIR = PROJECT_ROOT / "EDA_filer" / "Data"

df = pd.read_csv(FILES_DIR / "beviljade_platser_full_2019_2024.csv", sep=",", encoding="utf-8-sig")
df.columns = df.columns.str.strip()

df_statsbidrag = pd.read_csv(DATA_DIR / "statsbidrag_schablonnivåer.csv", sep=",", encoding="utf-8-sig")

df["Totalt antal platser"] = df.iloc[:, 1:].sum(axis=1)

df_kpi = pd.merge(
    df,
    df_statsbidrag[["Utbildningsområde", "Med momskompensation"]],
    on="Utbildningsområde",
    how="inner"
)

df_long = df_kpi.melt(
    id_vars=["Utbildningsområde", "Med momskompensation"],
    value_vars=["2019", "2020", "2021", "2022", "2023", "2024"],
    var_name="År",
    value_name="Antal platser"
)

df_long["Statsbidrag"] = df_long["Antal platser"] * df_long["Med momskompensation"]
df_long["Statsbidrag"] = df_long["Statsbidrag"].fillna(0).astype(int)


df_total_per_year = df_long.groupby("År")["Statsbidrag"].sum().reset_index()

page = """
# Totalt statsbidrag per år

<|{df_total_per_year}|chart|type=line|x=År|y=Statsbidrag|height=450px|width=700px|>

"""



Gui(page).run()


