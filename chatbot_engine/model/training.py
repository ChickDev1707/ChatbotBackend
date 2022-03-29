import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

import numpy
import random
import pickle
import json

with open("../intents/intents.json") as file:
  data = json.load(file)

# prepare data
words = []
labels = []
docs_x = []
docs_y = []

for intent in data["intents"]:
  for pattern in intent["patterns"]:
    wrds = nltk.word_tokenize(pattern)
    words.extend(wrds)
    docs_x.append(wrds)
    docs_y.append(intent["tag"])

  if intent["tag"] not in labels:
    labels.append(intent["tag"])

words = [stemmer.stem(w.lower()) for w in words if w != "?"]
words = sorted(set(words))
labels = sorted(set(labels))

# prepare training data
training = []
out_empty = [0] * len(labels)
# save data
with open("./data.pickle", "wb") as f:
  pickle.dump((words, labels), f)

for x, doc in enumerate(docs_x):
  bag = []
  wrds = [stemmer.stem(w.lower()) for w in doc]

  for w in words:
    if w in wrds:
      bag.append(1)
    else:
      bag.append(0)

  output_row = list(out_empty)
  output_row[labels.index(docs_y[x])] = 1
  training.append([bag, output_row])  

random.shuffle(training)
training = numpy.array(training)

train_x = list(training[:, 0])
train_y = list(training[:, 1])

# network
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

train_x= numpy.array(train_x)
train_y= numpy.array(train_y)
hist = model.fit(train_x, train_y, epochs= 1000, batch_size=8, verbose=1)
model.save('chatbot_model.h5', hist)
print("Done")
