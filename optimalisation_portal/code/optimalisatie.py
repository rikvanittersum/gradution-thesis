from portaal import portaal
from spanningen_portaal import spanningen_portaal
from helpers import combinaties_sterkte, stabiliteit_check, combinaties_portaal, combinaties_bruikbaarheid
import time
combinaties_balk_ligger = combinaties_portaal()

# Algoritme voor optimalisatie van het portaal.
def optimalisatie(overspanning, hoogte, hoh, kolommen_teller, ligger_teller):
    # Combinaties portaal wordt gebruikt om de portaal combinaties logisch te nummeren, data om alle portalen tijdelijk op
    # te slaan in de loop voordat ze naar een dataframe worden geschreven.
    start = time.time()
    # Alle maatgevende combinaties van ULS itereren.
    for cominatie_geval in combinaties_sterkte:

        # Portaal en de spanningen genereren.
        portaal_instance = portaal(hoogte, overspanning, hoh, ligger_teller, kolommen_teller)
        spanningen_portaal_instance = spanningen_portaal(portaal_instance, cominatie_geval)

        # Onafhankelijke spanningen controleren.
        spanningen_voldoen = spanningen_portaal_instance.controle_spanningen()

        # Als de spanningen niet voldoen, wordt de functie opnieuw uitgevoerd met andere profielen.
        if spanningen_voldoen is not True:
            # Id en else statements om te bepalen welk element de hoogste spanning ondervind.
            if spanningen_voldoen is 'ligger':
                ligger_teller += 1
            else:
                kolommen_teller += 1

            # De functie begint weer van vooraf aan met nieuwe profielen.
            return optimalisatie(overspanning, hoogte, hoh, kolommen_teller, ligger_teller)


        # Combinatie van spanningen controleren.
        combi_spanningen_voldoet = spanningen_portaal_instance.controle_spanning_combinatie()

        # Als de combinatie spanningen niet voldoen, wordt de functie opnieuw uitgevoerd met andere profielen.
        if combi_spanningen_voldoet is not True:
            if combi_spanningen_voldoet is 1:
                ligger_teller += 1
            else:
                kolommen_teller += 1
            return optimalisatie(overspanning, hoogte, hoh, kolommen_teller, ligger_teller)

        # Lokale stabiliteit controleren.
        stabiliteit = stabiliteit_check(portaal_instance, cominatie_geval)
        stabiliteit_voldoet = stabiliteit.controle_stabiliteit()

        # Als de lokale stabiliteit niet voldoen, wordt de functie opnieuw uitgevoerd met andere profielen.
        if stabiliteit_voldoet is not True:
            if stabiliteit_voldoet is 1:
                ligger_teller += 1
            else:
                kolommen_teller += 1
            return optimalisatie(overspanning, hoogte, hoh, kolommen_teller, ligger_teller)

    # Controle verplaatsingen bruikbaarheid. Een nieuwe loop.
    for combinatie in combinaties_bruikbaarheid:

        # Controle op verplaatsingen.
        verplaatsingen_voldoen = portaal_instance.verplaatsingen_controle(combinatie)

        # Als de verplaatsingen niet voldoen, wordt de functie opnieuw uitgevoerd met andere profielen.
        if verplaatsingen_voldoen is not True:
            if verplaatsingen_voldoen is 0:
                ligger_teller += 1
            else:
                kolommen_teller += 1

            return optimalisatie(overspanning, hoogte, hoh, kolommen_teller, ligger_teller)

    # De optimalisatie is nu afgelopen, het portaal voldoet aan alle eisen. Nu kan het worden opgeslagen. Het
    # portaal wordt een nr gegeven voor het ML model, en daarna opgeslagen onder de lijst data.
    end = time.time()
    print(end - start)
    profielen = portaal_instance.liggerprofiel, portaal_instance.kolomprofiel
    portaal_voldoet_nr = combinaties_balk_ligger.get(profielen)
    data = [overspanning, hoh, hoogte, portaal_voldoet_nr]

    return data