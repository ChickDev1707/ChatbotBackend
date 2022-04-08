
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
from symptom_checker.checker import get_symptom_check_result
from symptom_checker.issue_info import get_issue_info_result
from food_recipe.ingredient_searcher import get_ingredient_info_result
from food_recipe.meal_plan import get_meal_plan_result
from food_recipe.random_recipe import get_random_recipe_result
from location_search.searcher import get_location_search_result
from health_news.covid_info import get_covid_info_result
from health_news.health_news import get_health_news_result

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

def get_result(inp):
  ACCEPT_RATIO = 0.9
  bow = bag_of_words(inp)
  results = model.predict(numpy.array([bow]))[0]
  results_index = numpy.argmax(results)
  tag = labels[results_index]
  
  result = None
  if results[results_index] > ACCEPT_RATIO:
    result = get_output(inp, tag)
  else:
    result = {
      "status": "FAILED",
      "message": "Tôi không hiểu yêu cầu của bạn, xin nhập lại một yêu cầu khác!"
    }
  return result

def get_output(inp, tag):
  output = ""
  intent = get_matched_intent(tag)
  i_type = intent["type"]
  if i_type != None:
    if i_type == "saying":
      output = random.choice(intent['responses'])
    elif i_type == "drug_search":
      output = get_drug_search_result(inp, intent)
    elif i_type == "symptom_checker":
      output = get_symptom_check_result(inp, intent)
    elif i_type == "ingredient_info":
      output = get_ingredient_info_result(inp, intent)
    elif i_type == "location_search":
      output = get_location_search_result(inp, intent)
    elif i_type == "issue_info":
      output = get_issue_info_result(inp, intent)
    elif i_type == "covid_info":
      output = get_covid_info_result(intent)
    elif i_type == "health_news":
      output = get_health_news_result(intent)
    elif i_type == "meal_plan":
      output = get_meal_plan_result(inp, intent)
    elif i_type == "random_recipe":
      output = get_random_recipe_result(intent)
  else:
    output = "Không xác định"
  return output

def get_matched_intent(tag):
  for intent in data["intents"]:
    if intent["tag"] == tag:
      return intent
  return None

def chat():
  print("Start talking with the bot (type quit to stop)!")
  while True:
    inp = input("You: ")
    if inp.lower() == "quit":
      break
  
    result = get_result(inp)
    print(result)

chat()