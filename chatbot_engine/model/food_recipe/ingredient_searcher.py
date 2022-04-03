
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

with open(os.path.join(dirname, 'ingredients.json')) as file:
  data = json.load(file)

def get_ingredient_info(sentence, intent):
  url = intent["api"]["url"]
  headers = intent["api"]["headers"]
  query_string= {'amount': '100', 'unit': 'gram'}

  food_name = get_quote_content(sentence)
  food_id = get_best_match_item_ID(food_name, data["Ingredients"])
  url = url.replace("FOOD_ID", str(food_id))
  response = requests.request("GET", url, headers=headers, params=query_string)
  result = response.json()

  return get_nutrients_data(food_name, result)


def get_nutrients_data(food_name, ingredient):
  nutrients = ingredient["nutrition"]["nutrients"]
  # NO_NUTRIENT_OUTPUT = len(nutrients) if len(nutrients) < 5 else 5
  result = "Thành phần dinh dưỡng có trong 100 gram " + food_name + "\n"
  for nutrient in nutrients:
    formater = "{name}: {amount:.2f}{unit}"
    str_nutrient = formater.format(name=nutrient["name"], amount=nutrient["amount"], unit=nutrient["unit"])
    result = result + str_nutrient + "\n"
  return result
