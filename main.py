from tokenize import String
from warnings import catch_warnings
from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
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

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
with open("./intents/vietnamese-intents.json",  encoding="utf8") as file:
  data = json.load(file)
with open("./prepare/data.pickle", "rb") as f:
  words, labels = pickle.load(f)
model = load_model('./prepare/chatbot_model.h5')


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


def get_drug_name(sentence):
  pattern = '"([A-Za-z0-9_\./\\-]*)"'
  m = re.search(pattern, sentence)
  return m.group().replace('"', '')

def get_drug_api_result(drug_name, intent):
  complete_api = intent['api'].replace('DRUG_NAME', drug_name)
  response = requests.get(complete_api)
  drugInfo = response.json()
  label = intent['tag']
  result = drugInfo["results"][0][label][0]
  return result


@app.route('/', methods=['POST', "GET"])
def chatbot(): 
    if request.method =="POST":  
        sentence = request.form["sentence"]
        bow = bag_of_words(sentence)
        results = model.predict(numpy.array([bow]))[0]
        results_index = numpy.argmax(results)
        tag = labels[results_index]
        result = ""
        for intent in data["intents"]:
            if intent['tag'] == tag:
                if "responses" in intent:
                    result = random.choice(intent['responses'])
                else:
                    drug_name = get_drug_name(sentence)
                    result = get_drug_api_result(drug_name, intent)

        return result
    else:
        return render_template('chatbot.html')
       

if __name__ == '__main__':
    app.run(debug=True)