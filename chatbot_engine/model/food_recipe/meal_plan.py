
import json
import re
import sys
from pathlib import Path
from googletrans import Translator


utils_path = str(Path(__file__).parent.parent.absolute().joinpath('utils'))
sys.path.append(utils_path)

from io_util import get_response_with_exception, get_success_response, get_fail_response

def get_meal_plan_result(sentence, intent):
  try:
    meal_plan = get_meal_plan(sentence, intent)
    return get_success_response(tag= intent["tag"], data= meal_plan)
  except Exception as e:
    return get_fail_response(str(e))

def get_meal_plan(sentence, intent):
  url = intent["api"]["url"]
  headers = intent["api"]["headers"]
  query_string = get_query_string(sentence)

  response = get_response_with_exception(url, params= query_string, headers = headers)
  result = response.json()

  return get_translation_result(result)


def get_translation_result(result):
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
  try:
    pattern = r'\d+'
    m = re.search(pattern, sentence)
    return m.group()
  except:
    raise Exception("Không xác định được lượng calo cần tính toán, vui lòng hãy nhập lượng calo cho chế độ ăn")
