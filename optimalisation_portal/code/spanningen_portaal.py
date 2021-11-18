# Libraries voor wortel-trekken en omzetten eenheden.
import math
from anastruct.material.units import to_kN

# In deze klasse worden de spanningen bepaald. zowel per element als per soort spanning.
class spanningen_portaal:

    # Tijdens de init fase wordt middels de krachten en de profielen van de elementen de spanningen bepaald.
    def __init__(self,  portaal, combinatiegeval):
        elementen_constructie_krachten = portaal.krachten_en_verplaatsingen_elementen(combinatiegeval)
        self.normaal_spanning = {'kolom1': normaal_spanningen(elementen_constructie_krachten.get("normaalkracht"),
                                                              portaal, 0),
                       'ligger': normaal_spanningen(elementen_constructie_krachten.get("normaalkracht"), portaal, 1),
                       'kolom2': normaal_spanningen(elementen_constructie_krachten.get("normaalkracht"), portaal, 2)}
        self.buigspanning = {'kolom1': buig_spanningen(elementen_constructie_krachten.get("moment"), portaal, 0),
                       'ligger': buig_spanningen(elementen_constructie_krachten.get("moment"), portaal, 1),
                       'kolom2': buig_spanningen(elementen_constructie_krachten.get("moment"), portaal, 2)}
        self.dwarspanning = {'kolom1': dwars_spanningen(elementen_constructie_krachten.get("dwarskracht"), portaal, 0),
                       'ligger': dwars_spanningen(elementen_constructie_krachten.get("dwarskracht"), portaal, 1),
                       'kolom2': dwars_spanningen(elementen_constructie_krachten.get("dwarskracht"), portaal, 2)}
        self.kolom1 = {'normaal_spanning': normaal_spanningen(elementen_constructie_krachten.get("normaalkracht"),
                                                              portaal, 0),
                       'dwarspanning': dwars_spanningen(elementen_constructie_krachten.get("dwarskracht"), portaal, 0),
                       'momentspanning': buig_spanningen(elementen_constructie_krachten.get("moment"), portaal, 0)}
        self.ligger = {'normaal_spanning': normaal_spanningen(elementen_constructie_krachten.get("normaalkracht"),
                                                              portaal, 1),
                       'dwarspanning': dwars_spanningen(elementen_constructie_krachten.get("dwarskracht"), portaal, 1),
                       'momentspanning': buig_spanningen(elementen_constructie_krachten.get("moment"), portaal, 1)}
        self.kolom2 = {'normaal_spanning': normaal_spanningen(elementen_constructie_krachten.get("normaalkracht"),
                                                              portaal, 2),
                       'dwarspanning': dwars_spanningen(elementen_constructie_krachten.get("dwarskracht"), portaal, 2),
                       'momentspanning': buig_spanningen(elementen_constructie_krachten.get("moment"), portaal, 2)}

    # Controle elementen van afzonderlijke spanningen. Geeft element terug met de hoogste spanning.
    def controle_spanningen(self):
        # Floeispanning staal.
        max_spanning_materiaal = 235

        # Lijst met lijsten van spanningen.
        spanningen = [self.normaal_spanning, self.buigspanning, self.dwarspanning]

        # Alle spanningen itereren.
        for item in spanningen:
            # Van deze spanning het element met de hoogste spanning bepalen.
            element, max_spanning = max(item.items(), key=lambda x: abs(x[1]))

            # De hoogste spanning toetsen. Als deze niet voldoet moet de hoogst belaste worden bepaald.
            if abs(max_spanning) > max_spanning_materiaal:
                max_belaste_elementen = element
                max_spanning_materiaal = abs(max_spanning)

        # De elementen voldoen.
        if max_spanning_materiaal <= 235:
            return True

        # het maximaal belaste element wordt teruggegeven, de constructie voldoet niet.
        else:
            return max_belaste_elementen

    # Controle van combinatie van spanningen.
    def controle_spanning_combinatie(self):
        combispanning_elementen = []
        max_spanning_materiaal = 235

        # Lijst met dicts waarin per element de spanningen in staan.
        spanningen_per_element = [self.kolom1, self.ligger, self.kolom2]

        # Itereren over elementen.
        for element in spanningen_per_element:
            # Combispanning bepalen en in de lijst combispanning_elementen zeten.
            combispanning = (element.get("momentspanning") + element.get("normaal_spanning"))**2 + 3 * element.get("dwarspanning")**2
            combispanning_elementen.append(math.sqrt(combispanning))

        # De maximale combispanning van de elementen bepalen.
        max_spanning = max(combispanning_elementen)

        # Als het element met de maximale combispanning voldoet, return True, anders wordt het element doorgestuurd.
        if max_spanning < max_spanning_materiaal:
            return True
        else:
            return combispanning_elementen.index(max_spanning)


# Functie voor bepalen normaal spanning
def normaal_spanningen(normaal_krachten, portaal, element):

    if element is not 1:
        N_spanningen = normaal_krachten[element] / to_kN(portaal.A_kolommen)
    else:
        N_spanningen = normaal_krachten[element] / to_kN(portaal.A_ligger)

    return N_spanningen


# Functie voor bepalen buig spanning
def buig_spanningen(momenten, portaal, element):

    if element is not 1:
        buiging_spanning = momenten[element] * 1E6/portaal.W_kolommen
    else:
        buiging_spanning = momenten[element] * 1E6 / portaal.W_ligger
    return buiging_spanning


# Functie voor bepalen dwarsspanning spanning
def dwars_spanningen(dwarskrachten, portaal, element):

    if element is not 1:
        tau = dwarskrachten[element] * math.sqrt(3) / to_kN(portaal.A_profiel_kolommen)
    else:
        tau = dwarskrachten[element] * math.sqrt(3) / to_kN(portaal.A_profiel_ligger)
    return tau