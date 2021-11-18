# Functies en klassen importeren.
from helpers import combinaties_sterkte, stabiliteit_check, combinaties_portaal, combinaties_bruikbaarheid
from portaal import portaal
from spanningen_portaal import spanningen_portaal

# Libraries importeren voor willekeurig kiezen en maken van een dataframe.
import random
from pandas import DataFrame

# Combinaties portaal wordt gebruikt om de portaal combinaties logisch te nummeren, data om alle portalen tijdelijk op
# te slaan voordat ze naar een dataframe worden geschreven.
combinaties_balk_ligger = combinaties_portaal()
data = []

# Om een dataset te genereren voor het ML model, wordt het algoritme 1 miljoen keer uitgevoerd.
for i in range(450000):
    #
    try:
        print(i)
        overspanning = round(random.uniform(5, 18), 1)
        hoogte = round(random.uniform(3, 9), 1)
        hoh = round(random.uniform(5, 13), 1)
        kolommen_teller = 0
        ligger_teller = 0


        for cominatie_geval in combinaties_sterkte:
            voldoet = False

            # Onafhankelijke spanningen.
            while voldoet is False:

                portaal_instance = portaal(hoogte, overspanning, hoh,ligger_teller, kolommen_teller)
                spanningen_portaal_instance = spanningen_portaal(portaal_instance, cominatie_geval)

                spanningen_voldoen = spanningen_portaal_instance.controle_spanningen()

                if spanningen_voldoen is not True:
                    if spanningen_voldoen is 'ligger':
                        ligger_teller += 1
                    else:
                        kolommen_teller += 1
                else:
                    voldoet = True

            voldoet = False

            # Combinatie spanningen.
            while voldoet is False:

                combi_spanningen_voldoet = spanningen_portaal_instance.controle_spanning_combinatie()

                if combi_spanningen_voldoet is True:
                    voldoet = True
                else:
                    if combi_spanningen_voldoet is 1:
                        ligger_teller += 1
                    else:
                        kolommen_teller += 1
                    portaal_instance = portaal(hoogte, overspanning, hoh, ligger_teller, kolommen_teller)
                    spanningen_portaal_instance = spanningen_portaal(portaal_instance, cominatie_geval)

            voldoet = False

            # Lokale stabiliteit.
            while voldoet is False:

                stabiliteit = stabiliteit_check(portaal_instance, cominatie_geval)

                stabiliteit_voldoet = stabiliteit.controle_stabiliteit(portaal_instance)
                if stabiliteit_voldoet is True:
                    voldoet = True

                if stabiliteit_voldoet is 1:
                    ligger_teller += 1
                else:
                    kolommen_teller += 1
                portaal_instance = portaal(hoogte, overspanning, hoh,ligger_teller, kolommen_teller)
                spanningen_portaal_instance = spanningen_portaal(portaal_instance, cominatie_geval)

        # Controle verplaatsingen bruikbaarheid.
        for combinatie in combinaties_bruikbaarheid:
            voldoet = False

            while voldoet is False:
                portaal_instance = portaal(hoogte, overspanning, hoh,ligger_teller, kolommen_teller)

                verplaatsingen_voldoen = portaal_instance.verplaatsingen_controle(combinatie)

                if verplaatsingen_voldoen is True:
                    voldoet = True
                    break

                if verplaatsingen_voldoen is 0:
                    ligger_teller += 1
                else:
                    kolommen_teller += 1

        joe = portaal_instance.liggerprofiel, portaal_instance.kolomprofiel

        portaal_voldoet = combinaties_balk_ligger.get(joe)
        data.append([overspanning, hoh, hoogte, portaal_voldoet])
    except:
        pass


df = DataFrame.from_records(data, columns=['Overspanning', 'hoh', 'hoogte', 'portaal nr.'])
df.to_pickle("data_portaal_volgorde_500duizend+++")

