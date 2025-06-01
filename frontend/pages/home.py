import taipy.gui.builder as tgb

with tgb.Page() as home_page:
    with tgb.part(class_name= "container card"):
        with tgb.part(class_name="container card"):
            tgb.navbar()
        with tgb.part():
            tgb.text("# Välkommen till YH-analys", mode="md")
            tgb.text("The Skool’s dashboard för att utforska och förstå YH-data. Snabba insikter, smarta beslut - allt på ett ställe.")
            tgb.text("Att ge en överblick över antalet ansökta utbildningar per län och utbildningsområde, med möjlighet att filtrera och analysera data utifrån användarens intresse.")

        