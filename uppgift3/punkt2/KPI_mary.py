import pandas as pd
from taipy.gui import Gui
import taipy.gui.builder as tgb
from pathlib import Path

DATA_DIRECTORY = Path(__file__).parents[2] / "files"
df = pd.read_csv(DATA_DIRECTORY / "gender_KPI.csv", sep=",",  decimal="," , encoding="utf-8-sig")

# cleaning column names
df.columns = df.columns.str.strip().str.replace(r"\s+", " ", regex=True)

# transforming the data
for col in df.columns:
    if col != "År":
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(u"\xa0", "", regex=False) 
            .str.replace(",", ".", regex=False)      
            .str.strip()
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

#transforming the "År" column
df["År"] = pd.to_numeric(df["År"], errors="coerce")
df = df.dropna(subset=["År"])
df["År"] = df["År"].astype(int)


df["År"] = pd.to_numeric(df["År"], errors="coerce")
df = df.dropna(subset=["År"])
df["År"] = df["År"].astype(int)


years = df["År"].tolist()
indicators = df.columns[1:].tolist()  


selected_year = years[0]
selected_indicator = indicators[0]
filtered_value = ""

#filter_data function
def filter_data(state):
    try:
        selected_year = int(state.selected_year)
        value = df.loc[df["År"] == selected_year, state.selected_indicator]

        if not value.empty and pd.notna(value.values[0]):
            state.filtered_value = f"{float(value.values[0]):.2f}"
        else:
            state.filtered_value = "There is no data for this year or the value is not available."
    except Exception as e:
        state.filtered_value = f"Error: {e}"



#GUI page
with tgb.Page() as page:
    with tgb.part(class_name="container card"):
        tgb.text("## Analysis of Gender-Based Educational Indicators in YH (2007–2024)", mode="md")

        tgb.selector(
            value="{selected_year}",
            lov=years,
            dropdown=True,
            label="Select year"
        )

        tgb.selector(
            value="{selected_indicator}",
            lov=indicators,
            dropdown=True,
            label="Select indicator"
        )

        tgb.button(" Filter", on_action=filter_data)

        tgb.text("**Result:** {filtered_value}", mode="md")

# Run GUI
Gui(page).run(dark_mode=False, use_reloader=True, port=8060)
