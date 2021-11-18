import pandas as pd
import matplotlib.pyplot as plt
from helpers import csv_naar_dataframe
from helpers import referentie_bij_nr
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix

# Lijst om meest gebruikte referenties uit dataframe te filtereren.
meest_gebruikt = ["1", "10", "11", "12", "13", "14", "15", "17", "19", "2", "22", "23", "24", "28", "29", "3", "30",
                  "5", "8", "9"]

# Opzetten variabelen voor dataframe.
kolom1, kolom2 = csv_naar_dataframe()
dict1 = referentie_bij_nr()
kolom3 = []

# Toevoegen referentie nr.
for item in kolom1:
    kolom3.append(dict1.get(int(item)))

# Toevoegen ID nr.
id = []
for x in range(542):
    id.append(x)

# Creeren dataframe. Eerste kolom het nummer van de referentie, tweede kolom de tekst van de eis, derde kolom het id nr.
# en vierde kolom de titel van de referentie.
df = pd.DataFrame(data={"Referentie_nr": kolom1,"eis": kolom2, "id": id, "referentie_tekst": kolom3})

# Selecteren van meeste gebruikte referenties voor prestatie verbetering.
df = df[~df['Referentie_nr'].isin(meest_gebruikt)]
print(len(df))

# Eigenschappen van de eisen bepalen voor trainen model.
tfidf = TfidfVectorizer(sublinear_tf=True, min_df=1, norm='max', encoding='latin-1', ngram_range=(1, 2))
features = tfidf.fit_transform(df.eis).toarray()
labels = df.Referentie_nr
print(features.shape)

# Bewerken lijsten en dicts aanmaken voor trainen model.
category_id_df = df[['referentie_tekst', 'Referentie_nr']].drop_duplicates().sort_values('Referentie_nr')
category_to_id = dict(category_id_df.values)
id_to_category = dict(category_id_df[['Referentie_nr', 'referentie_tekst']].values)

# Code voor plotten grafiek meest gebruikte referenties
fig = plt.figure(figsize=(8,6))
df.groupby('referentie_tekst').eis.count().plot.bar(ylim=0)
plt.show()

# Modellen om te testen.
models = [
    RandomForestClassifier(n_estimators=200, max_depth=3, random_state=0),
    LinearSVC(),
    MultinomialNB(),
    LogisticRegression(random_state=0),
]

# Variabelen voor trainen modellen.
CV = 5
cv_df = pd.DataFrame(index=range(CV * len(models)))
entries = []

# Trainen modellen
for model in models:
  model_name = model.__class__.__name__
  accuracies = cross_val_score(model, features, labels, scoring='accuracy', cv=CV)
  for fold_idx, accuracy in enumerate(accuracies):
    entries.append((model_name, fold_idx, accuracy))

# Plotten en printen uitslagen model nauwkeurigheid.
cv_df = pd.DataFrame(entries, columns=['model_name', 'fold_idx', 'accuracy'])
sns.boxplot(x='model_name', y='accuracy', data=cv_df)
sns.stripplot(x='model_name', y='accuracy', data=cv_df,
              size=8, jitter=True, edgecolor="gray", linewidth=2)
plt.show()
print(cv_df.groupby('model_name').accuracy.mean())

# Trainen best presterende model.
model = LinearSVC()
X_train, X_test, y_train, y_test, indices_train, indices_test = train_test_split(features, labels, df.index,
                                                                                 test_size=0.33, random_state=0)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Plotten correcte en incorrecte voorspellingen.
conf_mat = confusion_matrix(y_test, y_pred)
fig, ax = plt.subplots(figsize=(8,6))
sns.heatmap(conf_mat, annot=True, fmt='d',
            xticklabels=category_id_df.referentie_tekst.values, yticklabels=category_id_df.referentie_tekst.values)
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.show()
