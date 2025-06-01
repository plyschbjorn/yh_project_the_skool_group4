
import pandas as pd
import duckdb
import plotly.express as px

def load_data():
    return {
        "2024": pd.read_excel("EDA_filer/data/resultat-2024-for-kurser-inom-yh.xlsx", sheet_name="Lista ansökningar"),
        "2023": pd.read_excel("EDA_filer/data/resultat-2023-for-kurser-inom-yh.xlsx", sheet_name="Lista ansökningar"),
        "2022": pd.read_excel("EDA_filer/data/resultat-2022-for-kurser-inom-yh.xlsx", sheet_name="Lista ansökningar"),
    }

def get_anordnare_count(df):
    return df["Anordnare namn"].nunique()

def count_beviljade_per_utbildningsområde(df):
    df_filtered = df[df["Beslut"] == "Beviljad"]
    return df_filtered.groupby("Utbildningsområde").size().reset_index(name="Antal beviljade kurser")

def beräkna_beviljandegrad_per_skola(df):
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

def skapa_figurer(df, year):
    df_grouped = count_beviljade_per_utbildningsområde(df)

    fig_bar = px.bar(
        df_grouped,
        y="Utbildningsområde",
        x="Antal beviljade kurser",
        title=f"Antal beviljade kurser per utbildningsområde ({year})",
        orientation='h',
        width=950
    )
    fig_bar.update_layout(paper_bgcolor="blue", plot_bgcolor="darkgray")

    fig_pie = px.pie(
        df_grouped,
        names="Utbildningsområde",
        values="Antal beviljade kurser",
        title=f"Fördelning av beviljade kurser per utbildningsområde i % ({year})",
        width=950
    )
    return fig_bar, fig_pie