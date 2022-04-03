
import json
import requests
import re
from googletrans import Translator

def get_meal_plan(sentence, intent):
  url = intent["api"]["url"]
  headers = intent["api"]["headers"]
  query_string = get_query_string(sentence)
  
  response = requests.request("GET", url, headers=headers, params=query_string)
  result = response.json()

  return get_translation_result(result)


def get_translation_result(result):
  print(result)
  translated_meals = []

  for meal in result["meals"]:
    trans_meal = get_translated_meal(meal)
    translated_meals.append(trans_meal)
  result["meals"] = translated_meals
  return result

def get_translated_meal(meal):
  translator = Translator()
  translation = translator.translate(meal["title"], src="en", dest="vi")
  meal["title"] = translation.text
  return meal

def get_query_string(sentence):
  calories = get_calories_amount(sentence)
  query_string= {'timeFrame': 'day', 'targetCalories': str(calories)}
  return query_string

def get_calories_amount(sentence):
  pattern = r'\d+'
  m = re.search(pattern, sentence)
  return m.group()
