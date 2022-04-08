
import json
import requests
import sys
import os

from pathlib import Path
from googletrans import Translator

dirname = os.path.dirname(__file__)
utils_path = str(Path(__file__).parent.parent.absolute().joinpath('utils'))
sys.path.append(utils_path)

from string_util import get_quote_content, get_best_match_item_ID
from io_util import get_response_with_exception, get_success_response, get_fail_response

with open(os.path.join(dirname, 'ingredients.json')) as file:
  data = json.load(file)

def get_ingredient_info_result(sentence, intent):
  try:
    result = get_ingredient_info(sentence, intent)
    return get_success_response(tag= intent["tag"], data= result)
  except Exception as e:
    return get_fail_response(str(e)) 

def get_ingredient_info(sentence, intent):
  url = intent["api"]["url"]
  headers = intent["api"]["headers"]
  query_string= {'amount': '100', 'unit': 'gram'}

  food_name = get_quote_content(sentence)
  food_id = get_best_match_item_ID(food_name, data["Ingredients"])
  if food_id == None:
    raise Exception("Không thể tìm thông tin về thành phần này")

  url = url.replace("FOOD_ID", str(food_id))
  response = get_response_with_exception(url, params= query_string, headers= headers)

  ingredient = response.json()
  return {
    "name": food_name,
    "nutrition": ingredient["nutrition"]
  }

