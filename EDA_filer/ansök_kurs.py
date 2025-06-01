import pandas as pd
import plotly.express as px
from taipy.gui import Gui
import taipy.gui.builder as tgb
import duckdb as duckdb
import plotly.graph_objects as go

# === 1. Läs in data
df_data = {
    "2024": pd.read_excel("EDA_filer/data/resultat-2024-for-kurser-inom-yh.xlsx", sheet_name="Lista ansökningar"),
    "2023": pd.read_excel("EDA_filer/data/resultat-2023-for-kurser-inom-yh.xlsx", sheet_name="Lista ansökningar"),
    "2022": pd.read_excel("EDA_filer/data/resultat-2022-for-kurser-inom-yh.xlsx", sheet_name="Lista ansökningar"),
}

# === 2. Funktioner
def get_anordnare_count(df):
    return df["Anordnare namn"].nunique() if "Anordnare namn" in df.columns else 0

def count_beviljade_per_utbildningsområde(df):
    df_filtered = df[df["Beslut"] == "Beviljad"] if "Beslut" in df.columns else df
    return df_filtered.groupby("Utbildningsområde").size().reset_index(name="Antal beviljade kurser")

def beräkna_beviljandegrad_per_skola(df: pd.DataFrame) -> pd.DataFrame:
    query = """
    SELECT
        "Anordnare namn" AS "Anordnare",
        COUNT(*) AS "Ansökta kurser",
        COUNT(*) FILTER (WHERE Beslut = 'Beviljad') AS "Antal beviljade",
        ROUND(
            COUNT(*) FILTER (WHERE Beslut = 'Beviljad') * 100.0 / COUNT(*),
            1
        ) AS "Beviljandegrad %"
    FROM df
    GROUP BY "Anordnare namn"
    ORDER BY "Antal beviljade" DESC
    """
    return duckdb.query(query).df()

# === 3. Initvärden
selected_year = "2024"
df_selected = df_data[selected_year]
antal_kurser = len(df_selected[df_selected["Beslut"] == "Beviljad"])
antal_anordnare = get_anordnare_count(df_selected)
antal_utbildningsområden = df_selected["Utbildningsområde"].nunique()
approved_rate = round((antal_kurser / df_selected.shape[0]) * 100, 2)
df_course = beräkna_beviljandegrad_per_skola(df_selected)

df_kurser_utbildningsområde_default = count_beviljade_per_utbildningsområde(df_selected)
fig_bar = px.bar(
    df_kurser_utbildningsområde_default,
    y="Utbildningsområde",
    x="Antal beviljade kurser",
    title=f"Antal beviljade kurser per utbildningsområde ({selected_year})",
    orientation='h',
    width=950
)
fig_bar.update_layout(paper_bgcolor="blue", plot_bgcolor="darkgray")

fig_pie = px.pie(
    df_kurser_utbildningsområde_default,
    names="Utbildningsområde",
    values="Antal beviljade kurser",
    title=f"Fördelning av beviljade kurser per utbildningsområde i % ({selected_year})",
    width=950,
    color_discrete_sequence=["#FF6384", "#36A2EB", "#FFCE56", "#66BB6A", "#BA68C8", "#FFA726"]
)

# === 4. Årsuppdateringsfunktion
def update_year(state):
    global selected_year, antal_kurser, antal_anordnare, antal_utbildningsområden, approved_rate, df_course, fig_bar, fig_pie
    selected_year = state.selected_year
    df_new = df_data[selected_year]

    antal_kurser = len(df_new[df_new["Beslut"] == "Beviljad"])
    antal_anordnare = get_anordnare_count(df_new)
    antal_utbildningsområden = df_new["Utbildningsområde"].nunique()
    approved_rate = round((antal_kurser / df_new.shape[0]) * 100, 2)
    df_course = beräkna_beviljandegrad_per_skola(df_new)

    df_kurser_updated = count_beviljade_per_utbildningsområde(df_new)
    fig_bar = px.bar(
        df_kurser_updated,
        y="Utbildningsområde",
        x="Antal beviljade kurser",
        title=f"Antal beviljade kurser per utbildningsområde ({selected_year})",
        orientation='h',
        width=950
    )
    fig_bar.update_layout(paper_bgcolor="blue", plot_bgcolor="darkgray")

    fig_pie = px.pie(
        df_kurser_updated,
        names="Utbildningsområde",
        values="Antal beviljade kurser",
        title=f"Fördelning av beviljade kurser per utbildningsområde i % ({selected_year})",
        width=950,
        color_discrete_sequence=["#FF6384", "#36A2EB", "#FFCE56", "#66BB6A", "#BA68C8", "#FFA726"]
        )
    

    state.antal_kurser = antal_kurser
    state.antal_anordnare = antal_anordnare
    state.antal_utbildningsområden = antal_utbildningsområden
    state.approved_rate = approved_rate
    state.df_course = df_course
    state.fig_bar = fig_bar
    state.fig_pie = fig_pie

# === 5. GUI-layout
with tgb.Page() as ansökningar:
    with tgb.part(class_name="container card"):
        tgb.navbar()
        with tgb.part(class_name="card"):
            tgb.text("# Ansökningsomgång för kurser", class_name="center-text bold", mode="md")

            tgb.selector("{selected_year}", lov=["2024", "2023", "2022"], dropdown=True, on_change=update_year)


            with tgb.part(class_name="container"):
                with tgb.layout(columns="1fr 1fr 1fr 1fr 1fr"):
                    with tgb.part(class_name="kpi-card blue"):
                        tgb.text("Beviljade kurser", class_name="kpi-label")
                        tgb.text("{antal_kurser}", class_name="kpi-value")

                    with tgb.part(class_name="kpi-card green"):
                        tgb.text("Anordnare", class_name="kpi-label")
                        tgb.text("{antal_anordnare}", class_name="kpi-value")

                    with tgb.part(class_name="kpi-card purple"):
                        tgb.text("Utbildningsområden", class_name="kpi-label")
                        tgb.text("{antal_utbildningsområden}", class_name="kpi-value")

                    with tgb.part(class_name="kpi-card orange"):
                        tgb.text("Beviljandegrad", class_name="kpi-label")
                        tgb.text("{approved_rate}%", class_name="kpi-value")

            

            with tgb.part(class_name="card text-row"):
                tgb.chart(figure="{fig_bar}")
            with tgb.part(class_name="card text-row"):
                tgb.chart(figure="{fig_pie}")

            with tgb.part(class_name="card"):
                tgb.text("## Lista över skolor med högst andel beviljade kurser ({selected_year})", mode="md", class_name="bold")
                tgb.text("Tabellen är sorterad efter antal beviljade kurser och beviljandegrad i %", class_name="italic small")
                tgb.table("{df_course}", page_size=10)
            
            with tgb.part(class_name="card") as column_chart_bar:
                tgb.text("## Antal beviljade kurser per utbildningsområde och år ", mode="md")
                tgb.image("public/beviljade_kurser_per_utbildningsområde.png", width="95%", height="600px")




# === 6. Run GUI
Gui(ansökningar).run(
    data={
        "selected_year": selected_year,
        "antal_kurser": antal_kurser,
        "antal_anordnare": antal_anordnare,
        "antal_utbildningsområden": antal_utbildningsområden,
        "approved_rate": approved_rate,
        "df_course": df_course,
        "fig_bar": fig_bar,
        "fig_pie": fig_pie,
    },
    dark_mode=False,
    use_reloader=True,
    port=8080
)

