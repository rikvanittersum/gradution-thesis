import pandas as pd

pickle = open("data_portaal_volgorde_500duizend", "rb")
pickle2 = open("data_portaal_volgorde_500duizend++", "rb")
df = pd.read_pickle(pickle)
df1 = pd.read_pickle(pickle2)


joe = [df, df1]
dftot = pd.concat(joe)

dftot.to_pickle('totaal data 1mil')