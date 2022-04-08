
import json
import requests
import sys
from pathlib import Path
from googletrans import Translator

utils_path = str(Path(__file__).parent.parent.absolute().joinpath('utils'))
sys.path.append(utils_path)

from io_util import get_response_with_exception, get_success_response, get_fail_response

def get_random_recipe_result(intent):
  try:
    recipe = get_random_recipe(intent)
    return get_success_response(tag= intent["tag"], data= recipe)
  except Exception as e:
    return get_fail_response(str(e))

def get_random_recipe(intent):
  url = intent["api"]["url"]
  headers = intent["api"]["headers"]
  
  response = get_response_with_exception(url, headers=headers)
  recipe = response.json()["recipes"][0]

  translator = Translator()
  translation = translator.translate(recipe["title"], src="en", dest="vi")
  recipe = {
    "title": translation.text,
    "vegan": recipe["vegan"],
    "servings": recipe["servings"],
    "sourceUrl": recipe["sourceUrl"],
    "readyInMinutes": recipe["readyInMinutes"],
  }
  return recipe


