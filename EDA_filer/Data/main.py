from taipy.gui import Gui
import pandas as pd
import plotly.express as px

df = pd.read_csv("data/ansokan_program.csv")

anordnare = df["Utbildningsanordnare"].dropna().unique().tolist()
val_anordnare = anordnare[0]

def kpi(df, namn):
    antal = df[df["Utbildningsanordnare"] == namn]
    return len(antal)

def rita_graf(df, namn):
    d = df[df["Utbildningsanordnare"] == namn]
    fig = px.bar(d, x="År", y="Antal studerande", title="Studerande per år")
    return fig

kpi_värde = kpi(df, val_anordnare)
grafen = rita_graf(df, val_anordnare)

sida = """
# Enkel Dashboard

<|layout|columns=1 1|gap=10px|>
<|dropdown|lov={anordnare}|value={val_anordnare}|label=Anordnare|on_change=byt_anordnare|>
<|{kpi_värde}|metric|label=Antal utbildningar|>
|>

<|{grafen}|chart|>
"""

def byt_anordnare(state):
    state.kpi_värde = kpi(df, state.val_anordnare)
    state.grafen = rita_graf(df, state.val_anordnare)

Gui(sida).run()
