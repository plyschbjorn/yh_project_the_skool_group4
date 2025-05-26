import pandas as pd
from pathlib import Path
import taipy.gui.builder as tgb
from taipy.gui import Gui

PROJECT_ROOT = Path(r"C:\Users\azizm\Documents\github\yh_project_the_skool_group4")
FILES_DIR = PROJECT_ROOT / "files"
DATA_DIR = PROJECT_ROOT / "EDA_filer" / "Data"

# Läs in data
df = pd.read_csv(FILES_DIR / "beviljade_platser_full_2019_2024.csv", sep=",", encoding="utf-8-sig")
df.columns = df.columns.str.strip()

df_statsbidrag = pd.read_csv(DATA_DIR / "statsbidrag_schablonnivåer.csv", sep=",", encoding="utf-8-sig")

# Summera totala platser per rad (förutsatt att varje rad är en unik kombination med anordnare och utbildningsområde)
df["Totalt antal platser"] = df.iloc[:, 2:].sum(axis=1)  # justera kolumnindex om nödvändigt

# Slå ihop med statsbidrag per utbildningsområde
df_kpi = pd.merge(
    df,
    df_statsbidrag[["Utbildningsområde", "Med momskompensation"]],
    on="Utbildningsområde",
    how="inner"
)

# Beräkna kostnad per rad
df_kpi["Beräknad kostnad"] = df_kpi["Totalt antal platser"] * df_kpi["Med momskompensation"]

# Skapa lista med unika anordnare
anordnare_list = df_kpi["Anordnare"].unique().tolist()

# Initierade värden för GUI
selected_anordnare = anordnare_list[0]
total_places = total_cost = "Välj anordnare"
avg_cost_per_place = 0

def filter_anordnare(state):
    data = df_kpi[df_kpi["Anordnare"] == state.selected_anordnare]
    if not data.empty:
        total_places_val = data["Totalt antal platser"].sum()
        total_cost_val = data["Beräknad kostnad"].sum()
        # Genomsnittligt statsbidrag per plats (viktat)
        avg_cost_val = total_cost_val / total_places_val if total_places_val > 0 else 0
        
        state.total_places = f"{int(total_places_val):,} platser"
        state.total_cost = f"{int(total_cost_val):,} kr"
        state.avg_cost_per_place = f"{avg_cost_val:,.2f} kr/plats"
    else:
        state.total_places = state.total_cost = state.avg_cost_per_place = "0"

with tgb.Page() as page:
    with tgb.part(class_name="container card stack-large"):
        with tgb.part(class_name="card"):
            tgb.text("# Statistik per anordnare", mode="md")
            tgb.selector("Välj anordnare", value="{selected_anordnare}", lov=anordnare_list, dropdown=True)
            tgb.button("Visa statistik", on_action=filter_anordnare)
        with tgb.layout(columns="1 1 1"):
            with tgb.part(class_name="card"):
                tgb.text("### Totalt antal platser")
                tgb.text("{total_places}")
            with tgb.part(class_name="card"):
                tgb.text("### Beräknad total kostnad")
                tgb.text("{total_cost}")
            with tgb.part(class_name="card"):
                tgb.text("### Genomsnittligt statsbidrag per plats")
                tgb.text("{avg_cost_per_place}")
        with tgb.part(class_name="card"):
            tgb.text("### Rådata för vald anordnare")
            tgb.table("{df_kpi[df_kpi['Anordnare'] == selected_anordnare]}")

Gui(page).run()


