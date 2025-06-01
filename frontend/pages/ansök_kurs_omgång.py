
from taipy.gui import Gui
import taipy.gui.builder as tgb
from backend.data_processing_kurs import (
    load_data, get_anordnare_count,
    beräkna_beviljandegrad_per_skola,
    skapa_figurer
)

df_data = load_data()
selected_year = "2024"
df_selected = df_data[selected_year]

antal_kurser = len(df_selected[df_selected["Beslut"] == "Beviljad"])
antal_anordnare = get_anordnare_count(df_selected)
antal_utbildningsområden = df_selected["Utbildningsområde"].nunique()
approved_rate = round((antal_kurser / df_selected.shape[0]) * 100, 2)
df_course = beräkna_beviljandegrad_per_skola(df_selected)
fig_bar, fig_pie = skapa_figurer(df_selected, selected_year)

def update_year(state):
    global selected_year, antal_kurser, antal_anordnare, antal_utbildningsområden, approved_rate, df_course, fig_bar, fig_pie
    selected_year = state.selected_year
    df_new = df_data[selected_year]

    antal_kurser = len(df_new[df_new["Beslut"] == "Beviljad"])
    antal_anordnare = get_anordnare_count(df_new)
    antal_utbildningsområden = df_new["Utbildningsområde"].nunique()
    approved_rate = round((antal_kurser / df_new.shape[0]) * 100, 2)
    df_course = beräkna_beviljandegrad_per_skola(df_new)
    fig_bar, fig_pie = skapa_figurer(df_new, selected_year)

    state.antal_kurser = antal_kurser
    state.antal_anordnare = antal_anordnare
    state.antal_utbildningsområden = antal_utbildningsområden
    state.approved_rate = approved_rate
    state.df_course = df_course
    state.fig_bar = fig_bar
    state.fig_pie = fig_pie

with tgb.Page() as ansökningar:
    with tgb.part(class_name="container card"):
        tgb.navbar()
        with tgb.part(class_name="card"):
            tgb.text("# Ansökningsomgång för kurser", class_name="center-text bold", mode="md")
            tgb.selector("{selected_year}", lov=["2024", "2023", "2022"], dropdown=True, on_change=update_year)
            with tgb.part(class_name="container"):
                with tgb.layout(columns="1fr 1fr 1fr 1fr"):
                    tgb.text("Beviljade kurser: {antal_kurser}")
                    tgb.text("Anordnare: {antal_anordnare}")
                    tgb.text("Utbildningsområden: {antal_utbildningsområden}")
                    tgb.text("Beviljandegrad: {approved_rate}%")
            tgb.chart(figure="{fig_bar}")
            tgb.chart(figure="{fig_pie}")
            tgb.text("## Lista över skolor med högst andel beviljade kurser ({selected_year})", mode="md", class_name="bold")
            tgb.text("Tabellen är sorterad efter antal beviljade kurser och beviljandegrad i %", class_name="italic small")
            tgb.table("{df_course}", page_size=10)

gui_data = {
    "selected_year": selected_year,
    "antal_kurser": antal_kurser,
    "antal_anordnare": antal_anordnare,
    "antal_utbildningsområden": antal_utbildningsområden,
    "approved_rate": approved_rate,
    "df_course": df_course,
    "fig_bar": fig_bar,
    "fig_pie": fig_pie,
    
}
