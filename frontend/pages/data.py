import taipy.gui.builder as tgb
from backend.data_processing import df_2024
from backend.map_processing import kurs_2022, kurs_2023, kurs_2024

with tgb.Page() as data_page:
    with tgb.part(class_name="container card stack-large"):
        with tgb.part(class_name="container card"):
            tgb.navbar()
        tgb.text("# Rådata", mode="md")

        with tgb.part(class_name="card"):
            tgb.text("## Program - resultat ansökningsomgång 2024",mode="md")
            tgb.table("{df_2024}")
        with tgb.part(class_name="card"):
            tgb.text("## Kurser - resultat ansökningsomgång 2022",mode="md")
            tgb.table("{kurs_2022}")
        with tgb.part(class_name="card"):
            tgb.text("## Kurser - resultat ansökningsomgång 2023",mode="md")
            tgb.table("{kurs_2023}")
        with tgb.part(class_name="card"):
            tgb.text("## Kurser - resultat ansökningsomgång 2024",mode="md")
            tgb.table("{kurs_2024}")