import taipy.gui.builder as tgb

with tgb.Page() as home_page:
    with tgb.part(class_name= "container card"):
        with tgb.part(class_name="container card"):
            tgb.navbar()
        with tgb.part():
            tgb.text("## Välkommen till YH-analys", mode="md")
            tgb.text("### En interaktiv plattform för att utforska och analysera data om yrkeshögskoleutbildningar i Sverige.", mode="md")

        