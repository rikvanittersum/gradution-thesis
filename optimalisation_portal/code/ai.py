# Importeren van libraries voor plotten van grafieken en het bewerken van data.
import matplotlib.pyplot as plt
import pandas as pd
import time

# Importeren van noodzakkelijke libraries voor trainen en vallideren van het model.
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier

# Hier wordt de data uit het optimalisatie-programma geladen en willekeurig gerangschikt.
pickle = open("data_portaal_volgorde_500duizend+++!", "rb")
df = pd.read_pickle(pickle)
df = shuffle(df)

# Code voor het weergeven van een diagram voor inzichtelijk maken tabel.
fig = plt.figure(figsize=(8,6))
df.groupby('portaal nr.').Overspanning.count().plot.bar(ylim=0)
plt.show()

# Hier worden de labels verklaard. Dit zijn de antwoorden op de 'vragen'. De tabel met de eigenschappen van het portaal,
# wordt hier gescheiden van de tabel met het optimale ontwerp.
labels = df['portaal nr.']
training_data = df.drop('portaal nr.', axis=1)

# De training en de test data worden  aangemaakt. Tien procent van de data wordt test data, op de rest zal het model
# worden getraint.
x_train, x_test, y_train, y_test = train_test_split(training_data, labels, test_size=0.10, random_state=2)

# Trainen van het model vind plaats. Forrest classifier presteerd continu het beste.
forrest = RandomForestClassifier(n_estimators=20)
forrest.fit(x_train, y_train)

# Printen van score en confusion matrix.
print(forrest.score(x_test, y_test))
start = time.time()
knn_predictions = forrest.predict(x_test)
end = time.time()
print(end - start)
resultaat_voorspellingen = confusion_matrix(y_test, knn_predictions)

for element in resultaat_voorspellingen:
    print(element)

