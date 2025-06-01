import taipy.gui.builder as tgb
from backend.data_processing import  long_df, utb_list, df_2024 , chart_fig, selected_field, mainindic, året
from backend.updates import update_chart , filter_data
from backend.data_processing import filtered_value
from taipy.gui.builder import page
from taipy.gui import Gui
from backend.data_processing import selected_indicator, selected_year
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter




with tgb.Page() as dashboard_page:
    
    with tgb.part(class_name="container card"):
        with tgb.part(class_name="container card"):
            tgb.navbar()
        tgb.text("## Vad väljer studenterna? En titt på trender inom yrkeshögskolan (2019–2024)", mode="md")

        with tgb.layout(columns="2 1"):
            with tgb.part(class_name="card") as column_chart:
                tgb.chart(figure="{chart_fig}", mode="plotly")

            with tgb.part(class_name="card") as column_filters:
                tgb.text("#### Välj utbildningsområde", mode="md")
                tgb.selector(
                    value="{selected_field}",
                    lov=utb_list,
                    dropdown=True,
                    on_change=update_chart,
                    width="90%"
                 )
        with tgb.layout(columns="3"):
            with tgb.part(class_name="card") as column_filters:
                
                # GUI page layout (like your working version)


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
             
            with tgb.part(class_name="card") as column_chart_bar:
                tgb.text("## Antal studerande över tid", mode="md")
                tgb.image("public/bar_chart.png", width="100%", height="600px")


 
    __all__ = ["dashboard_page"]


