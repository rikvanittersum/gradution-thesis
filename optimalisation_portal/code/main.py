# Functie importeren
from optimalisatie import optimalisatie

# Libraries importeren voor willekeurig kiezen en maken van een dataframe.
import random
from pandas import DataFrame

# In data wordt het resultaat van alle optimalisaties opgeslagen.
data = []

# Om een dataset te genereren voor het ML model, wordt het algoritme 1 miljoen keer uitgevoerd.
for i in range(10):
    print(i)
    # try en except wordt toegepast omdat het portaal soms te groot is voor HEA profielen. eht algoritme geeft dan een
    # error. Try en except zorgt ervoor dat het programma dan verder gaat met de loop.
    try:
        # Willekereurig afmetingen bepalen.
        hoogte = round(random.uniform(3, 9), 1)
        hoh = round(random.uniform(5, 13), 1)
        overspanning = round(random.uniform(5, 18), 1)

        ligger_teller = 0
        kolommen_teller = 0

        # Aan de data wordt nu het resultaat van de optimalisatie toegevoegd. Dit resultaat is een lijst met de
        # eigenschappen en het optimale ontwerp: [overspanning, hoh, hoogte, portaal_voldoet_nr].
        data.append(optimalisatie(overspanning, hoogte, hoh, kolommen_teller, ligger_teller))
    except:
        pass

# Alle optimalisaties zijn opgeslagen als lijsten in een lijst :
# [[overspanning, hoh, hoogte, portaal_voldoet_nr], [overspanning, hoh, hoogte, portaal_voldoet_nr], etc]. Er wordt van
# deze lijst met lijsten nu een dataframe, oftewel een tabel gemaakt, en weggeschreven.
df = DataFrame.from_records(data, columns=['Overspanning', 'hoh', 'hoogte', 'portaal nr.'])
print(df.head)
#df.to_pickle("data_portaal_volgorde_500duizend+++!")