# Libraries voor trainen van modellen en algemene tools voor NLP
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
import nltk
from nltk.classify import ClassifierI
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Libraries voor willekeurigheid en oplslaan en zoeken van bestanden
import random
import os
import pickle

# Functie voor het omzetten van pdf's naar woorden
from helpers import pdf_woorden

# Functie die eigenschappen van een document bepaald, bepaalde woorden in dit geval.
def find_features(document):
    words = set(document)
    features = {}
    for w in  word_features:
        features[w] = (w in words)
    return features

# Zoeken van mappen in de directory.
directory1 = os.listdir('positief')
directory2 = os.listdir('negatief')

# Aanmaken van lijsten die alle woorden van de leidraden zullen bevatten
meegedaan = []
niet_meegedaan = []

# Toevoegen van woorden aan lijsten
 # for filename in directory2:
    # niet_meegedaan.append(pdf_woorden('negatief/' + filename))
    # print(filename)
# for filename in directory1:
    # print(filename)
    # meegedaan.append(pdf_woorden('positief/' + filename))

# Beide pickles bestaan om proces te versnellen.
# pickle_pos = open("pickle_pos", "wb")
# pickle.dump(meegedaan, pickle_pos)
# pickle_pos.close()

# pickle_neg = open("pickle_neg", "wb")
# pickle.dump(niet_meegedaan, pickle_neg)
# pickle_neg.close()

# Reeds opgeslagen bestanden openen en laden.
pickle1 = open("pickle_pos", "rb")
meegedaan = pickle.load(pickle1)
pickle2 = open("pickle_neg", "rb")
niet_meegedaan = pickle.load(pickle2)

# Lijst die lijsten bevat met alle leidraden, met daarbij aanduiding of ze positief of negatief zijn.
documents = []

#   Alle bestanden toevoegen
for pdf in meegedaan:
    documents.append( (pdf, "pos") )
for pdf in niet_meegedaan:
    documents.append( (pdf, "neg") )

# Lijst voor het bijhouden van alle woorden die gebruikt worden in selectieleidraden.
all_words = []

# Toevoegen van alle woorden aan all_words en alle letters kleine letters maken.
for lijst in meegedaan:
    for woorden in lijst:
        all_words.append(woorden.lower())
for lijst in niet_meegedaan:
    for woorden in lijst:
        all_words.append(woorden.lower())

# Van alle woorden meest 3000 meest gebruikte selecteren in word_feautures. Vervolgens een lijst maken welke vaak in
# negatieve en in positieve documenten voorkomen.
all_words = nltk.FreqDist(all_words)
word_features = list(all_words.keys())[:3000]
featuresets = [(find_features(doc), category) for (doc, category) in documents]

# Variabele voor bijhouden gemiddelde score.
Nu = mnb = ber = logic = lin = 0

# tien keer herhalen trainen en testen
for i in range (100):

    # De data wordt willekeurig gerangschikt. Vervolgens worden de de eerste 270 leidraden geselecteerd als
    # trainings data, en de rest als test data.
    random.shuffle(featuresets)
    training_set = featuresets[:270]
    testing_set = featuresets[270:]

    MNB_classifier = SklearnClassifier(MultinomialNB())
    MNB_classifier.train(training_set)
    mnb += nltk.classify.accuracy(MNB_classifier, testing_set)*100

    BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
    BernoulliNB_classifier.train(training_set)
    ber += nltk.classify.accuracy(BernoulliNB_classifier, testing_set)*100

    LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
    LogisticRegression_classifier.train(training_set)
    logic += nltk.classify.accuracy(LogisticRegression_classifier, testing_set)*100

    LinearSVC_classifier = SklearnClassifier(LinearSVC())
    LinearSVC_classifier.train(training_set)
    lin += nltk.classify.accuracy(LinearSVC_classifier, testing_set)*100

    # Uit meerdere tests is gebleken dat de NuSVC het best presteert.
    # Hiervan worden momenteel de resultaten gegenereerd.
    NuSVC_classifier = SklearnClassifier(NuSVC())
    NuSVC_classifier.train(training_set)
    Nu += nltk.classify.accuracy(NuSVC_classifier, testing_set)*100

# Print de gemiddelde score uit.
print("MNB = ", mnb/100, "Ber = ", ber/100, "Logistic = ", logic/100, "Linear = ", lin/100, "Nu = ", Nu/100)
