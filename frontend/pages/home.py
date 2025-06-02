import taipy.gui.builder as tgb

with tgb.Page() as home_page:
    with tgb.part(class_name="container card stack-large"):
        with tgb.part(class_name="container card"):
            tgb.navbar()

        with tgb.part(class_name="card"):
            tgb.text(
                """
# Välkommen till The Skool YH-analys

**The Skool’s interaktiva dashboard för att utforska och förstå data inom yrkeshögskolan (YH).**
Här hittar du allt du behöver för att fatta datadrivna beslut: från ansökningar och antagningar till ekonomiska nyckeltal och regional spridning.

Plattformen är uppdelad i sex delar:

---

### 👩‍🎓 Studerande
Vad väljer studenterna?
Den här sidan belyser trender bland YH-studenter från 2019 till 2024. Du kan:

- Utforska förändringar i intresset för olika utbildningsområden.
- Filtrera på kön och indikatorer som antagningsgrad, könsfördelning och söktryck.
- Se antal studerande över tid via interaktiva diagram och bilder.

---

### 📚 Kurser
Fokus på ansökningsomgångar för YH-kurser – vilka kurser beviljas, och av vilka?
Här kan du:

- Följa beviljandegraden över tid.
- Se vilka utbildningsområden som dominerar.
- Jämföra skolor utifrån hur stor andel av deras ansökta kurser som beviljas.
- Granska stapel- och cirkeldiagram för en visuell överblick, samt en tabell över de mest framgångsrika anordnarna.

---

### 🗺️ Karta
En geografisk vy över beviljade kurser per län.
Genom en interaktiv karta kan du:

- Se fördelningen av kurser över landet.
- Välja årtal och få uppdaterad statistik för respektive region.
- Kombinera kartan med tabellen nedan för detaljerad analys.

---

### 📊 KPI
Nyckeltal (Key Performance Indicators) per utbildningsområde:
- Totalt antal platser (2019–2024)
- Statsbidrag per plats (schablonvärde)
- Beräknad total kostnad för statsbidrag
Används för att få snabb överblick över resursfördelning och ekonomiska behov inom olika YH-områden.

---

###  🏫 Anordnare

Hur lyckas enskilda utbildningsanordnare över tid?
Här får du en detaljerad översikt för valfri anordnare och årtal:

- Se hur många kurser som har beviljats respektive avslagits.
- Få ut andel beviljade ansökningar i procent.
- Granska en tabell med all relaterad kursdata.

Perfekt för att jämföra aktörer, följa upp beviljanden eller identifiera förbättringsområden.

---

### 📄 Data
För dig som vill gå djupare ner i siffrorna. Här hittar du all den underliggande data som ligger till grund för visualiseringarna i dashboarden. Perfekt för vidare analys eller export.

                """,
                mode="md"
            )

__all__ = ["home_page"]