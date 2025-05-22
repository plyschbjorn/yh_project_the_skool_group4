
import plotly.express as px
from taipy.gui import Gui
import taipy.gui.builder as tgb
from backend.data_processing import  long_df, utb_list, df_2024 , chart_fig, selected_field
from backend.updates import update_chart








# === 7. GUI layout
with tgb.Page() as page:
    with tgb.part(class_name="container card"):
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

        #with tgb.part(class_name="card"):
         #   tgb.text("## Rådata för alla utbildningsområden", mode="md")
          #  for utb in utb_list:
           #     tgb.text(f"### {utb}", mode="md")
               # tgb.table(f"{{all_tables['{utb}']}}")

        with tgb.part(class_name="card"):

            tgb.text("## Rådata", mode="md")
            tgb.table("{df_2024}")

# === 8. Run GUI
Gui(page).run(dark_mode=False, use_reloader=True, port=8050)
