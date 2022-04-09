
from tensorflow.keras.models import load_model
import json
import numpy
import pickle
import os
import sys
from pathlib import Path

chatbot_engine_path = str(Path(__file__).parent.parent.parent.absolute())
sys.path.append(chatbot_engine_path)

from model.utils.string_util import bag_of_words

from model.saying.basic_saying import get_saying_result
from model.drug_search.searcher import get_drug_search_result
from model.symptom_checker.checker import get_symptom_check_result
from model.symptom_checker.issue_info import get_issue_info_result
from model.food_recipe.ingredient_searcher import get_ingredient_info_result
from model.food_recipe.meal_plan import get_meal_plan_result
from model.food_recipe.random_recipe import get_random_recipe_result
from model.location_search.searcher import get_location_search_result
from model.health_news.covid_info import get_covid_info_result
from model.health_news.health_news import get_health_news_result


with open(os.path.join(chatbot_engine_path, "intents/intents.json")) as file:
  data = json.load(file)

with open(os.path.join(chatbot_engine_path, "model/data.pickle"), "rb") as f:
  words, labels = pickle.load(f)

model = load_model(os.path.join(chatbot_engine_path, "model/chatbot_model.h5"))

def get_result(inp):
  ACCEPT_RATIO = 0.9
  bow = bag_of_words(words, inp)
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
      output = get_saying_result(intent)
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