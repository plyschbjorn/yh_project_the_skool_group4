import pandas as pd
from taipy.gui import Gui
import taipy.gui.builder as tgb
from pathlib import Path
from backend.data_processing import df_filter_kön

# Load Excel
DATA_DIRECTORY = Path(__file__).parents[1] / "files"
df_filter_kön = pd.read_excel(DATA_DIRECTORY / "kön.xlsx", decimal=",")

# Clean numbers
df_clean = df_filter_kön.copy()
cols_to_clean = df_clean.columns[1:]
for col in cols_to_clean:
    df_clean[col] = df_clean[col].astype(str).str.replace(u'\xa0', '', regex=False)
    df_clean[col] = df_clean[col].str.replace(',', '.', regex=False)
    df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

# Extract indicators & years
året = list(map(str, df_clean.columns[1:]))
mainindic = df_clean["Unnamed: 0"][::3].tolist()  # Only main indicators

# Initial states
selected_year = året[0]
selected_indicator = mainindic[0]
filtered_value = ""

# Logic function to extract women/men percentages
def show_gender_distribution(indicator: str, year: str):
    indicator_rows = df_clean[df_clean["Unnamed: 0"] == indicator].index.tolist()
    if not indicator_rows:
        return "⛔ Indikatorn hittades inte."

    idx = indicator_rows[0]

    try:
        year_col = int(year) if int(year) in df_clean.columns else str(year)
        women = df_clean.iloc[idx + 1][year_col]
        men = df_clean.iloc[idx + 2][year_col]
    except (IndexError, KeyError):
        return f"⛔ Data för år {year} saknas eller har fel format."

    if pd.isna(women) or pd.isna(men):
        return f"⚠️ Fullständig data saknas för år {year}."

    return f"{indicator} år {year}:\n- 👩 Kvinnor: {women}%\n- 👨 Män: {men}%"


# Button logic
def filter_data(state):
    try:
        state.filtered_value = show_gender_distribution(state.selected_indicator, state.selected_year)
    except Exception as e:
        state.filtered_value = f"Fel: {e}"

# GUI page layout (like your working version)
with tgb.Page() as page:
    with tgb.part(class_name="container card"):
        tgb.text("## Analys av könsbaserade utbildningsindikatorer i YH (2007–2024)", mode="md")

        tgb.selector(
            value="{selected_year}",
            lov=året,
            dropdown=True,
            label="Välj år"
        )

        tgb.selector(
            value="{selected_indicator}",
            lov=mainindic,
            dropdown=True,
            label="Välj indikator"
        )

        tgb.button(" Filtrera", on_action=filter_data)

        tgb.text("**Resultat:** {filtered_value}", mode="md")

# Run GUI
Gui(page).run(dark_mode=False, use_reloader=True, port=8060)
