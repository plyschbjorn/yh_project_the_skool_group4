import taipy.gui.builder as tgb
from backend.data_processing import df_2024

with tgb.Page() as data_page:
    with tgb.part(class_name="container card"):
        with tgb.part(class_name="container card"):
            tgb.navbar()
        

        with tgb.part(class_name="card"):
            tgb.text("# Rådata", mode="md")
            tgb.table("{df_2024}")