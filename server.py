from flask import Flask, request
from flask_cors import CORS, cross_origin

from tensorflow.keras.models import load_model
import random
import json
import numpy
import pickle

# feature module
from chatbot_engine.model.drug_search.searcher import get_drug_search_result
from chatbot_engine.model.symptom_checker.checker import get_check_result
from chatbot_engine.model.utils.string_util import bag_of_words

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# load data and resource
with open("./chatbot_engine/intents/intents.json",  encoding="utf8") as file:
  data = json.load(file)
with open("./chatbot_engine/model/data.pickle", "rb") as f:
  words, labels = pickle.load(f)

# model
model = load_model('./chatbot_engine/model/chatbot_model.h5')

# api
@app.get('/')
def index():
  return "hello world"

@app.post('/')
def chatbot(): 
  sentence = request.form["sentence"]
  print(sentence)
  bow = bag_of_words(words, sentence)
  results = model.predict(numpy.array([bow]))[0]
  results_index = numpy.argmax(results)
  tag = labels[results_index]
  
  result = ""
  for intent in data["intents"]:
    if intent["tag"] == tag:
      i_type = intent["type"]
      if i_type == "saying":
        result = random.choice(intent['responses'])
      elif i_type == "drug_search":
        result = get_drug_search_result(inp, intent)
      elif i_type == "symptom_checker":
        result = get_check_result(inp, intent)
      else:
        result = "unrecognized"
  return result
   
if __name__ == '__main__':
  app.run(debug=True)