
import json
import requests
from googletrans import Translator

def get_random_recipe(intent):
  url = intent["api"]["url"]
  headers = intent["api"]["headers"]
  
  response = requests.request("GET", url, headers=headers)
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


