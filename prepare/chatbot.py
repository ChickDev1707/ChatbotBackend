
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

from tensorflow.keras.models import load_model
import random
import json
import requests
import re
import numpy
import pickle

with open("../intents/vietnamese-intents.json") as file:
  data = json.load(file)

with open("data.pickle", "rb") as f:
  words, labels = pickle.load(f)

model = load_model('chatbot_model.h5')

# chatbot function

def clean_up_sentence(sentence):
  s_words = nltk.word_tokenize(sentence)
  s_words = [stemmer.stem(word.lower()) for word in s_words]
  return s_words

def bag_of_words(sentence):
  s_words = clean_up_sentence(sentence)
  bag = [0] * len(words)
  for se in s_words:
    for i, w in enumerate(words):
      if w == se:
        bag[i] = 1
          
  return numpy.array(bag)


def chat():
  print("Start talking with the bot (type quit to stop)!")
  while True:
    inp = input("You: ")
    if inp.lower() == "quit":
      break
    
    bow = bag_of_words(inp)
    results = model.predict(numpy.array([bow]))[0]
    results_index = numpy.argmax(results)
    tag = labels[results_index]

    result = ""
    for intent in data["intents"]:
      if intent['tag'] == tag:
        if "responses" in intent:
          result = random.choice(intent['responses'])
        else:
          # api
          drug_name = get_drug_name(inp)
          result = get_drug_api_result(drug_name, intent)
          
    print(result)

def get_drug_name(sentence):
  pattern = r'"([A-Za-z0-9_\./\\-]*)"'
  m = re.search(pattern, sentence)
  return m.group().replace('"', '')

def get_drug_api_result(drug_name, intent):
  complete_api = intent['api'].replace('DRUG_NAME', drug_name)
  response = requests.get(complete_api)
  drugInfo = response.json()
  label = intent['tag']
  result = drugInfo["results"][0][label][0]
  return result

chat()