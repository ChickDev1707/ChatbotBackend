
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

from tensorflow.keras.models import load_model
import random
import json
import re
import numpy
import pickle
import os

from drug_search.searcher import get_drug_search_result
from symptom_checker.checker import get_check_result
from symptom_checker.issue_info import get_issue_info
from food_recipe.ingredient_searcher import get_ingredient_info
from food_recipe.meal_plan import get_meal_plan
from food_recipe.random_recipe import get_random_recipe
from location_search.searcher import get_location_search_result
from health_news.covid_info import get_covid_info
from health_news.health_news import get_health_news

from pathlib import Path
dirname = os.path.dirname(__file__)
intent_path = str(Path(__file__).parent.parent.absolute().joinpath("intents"))

with open(os.path.join(intent_path, "intents.json")) as file:
  data = json.load(file)

with open(os.path.join(dirname, "data.pickle"), "rb") as f:
  words, labels = pickle.load(f)

model = load_model(os.path.join(dirname, "chatbot_model.h5"))

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
      if intent["tag"] == tag:
        i_type = intent["type"]
        if i_type == "saying":
          result = random.choice(intent['responses'])
        elif i_type == "drug_search":
          result = get_drug_search_result(inp, intent)
        elif i_type == "symptom_checker":
          result = get_check_result(inp, intent)
        elif i_type == "ingredient_info":
          result = get_ingredient_info(inp, intent)
        elif i_type == "location_search":
          result = get_location_search_result(inp, intent)
        elif i_type == "issue_info":
          result = get_issue_info(inp, intent)
        elif i_type == "covid_info":
          result = get_covid_info(intent)
        elif i_type == "health_news":
          result = get_health_news(intent)
        elif i_type == "meal_plan":
          result = get_meal_plan(inp, intent)
        elif i_type == "random_recipe":
          result = get_random_recipe(intent)
        else:
          print("unrecognized")
      
      # if intent['tag'] == tag:
      #   if "responses" in intent:
      #     result = random.choice(intent['responses'])
      #   else:
      #     # api
      #     drug_name = get_drug_name(inp)
      #     result = get_drug_api_result(drug_name, intent)
          
    print(result)


chat()