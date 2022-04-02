
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

with open(os.path.join(dirname, 'symptoms.json')) as file:
  data = json.load(file)

def get_check_result(sentence, intent):
  query_string = get_query_string(sentence)
  url = intent["api"]["url"]
  headers = intent["api"]["headers"]
  response = requests.request("GET", url, headers=headers, params=query_string)
  result = response.json()
  return get_translation_result(result)

def get_translation_result(result):
  translated_result = []
  NO_SYMPTOM = 3
  i = 0;
  while i< NO_SYMPTOM:
    item = result[i]
    translated_issue = get_translated_issue(item)
    translated_result.append(translated_issue)
    i+= 1
  return translated_result

def get_translated_issue(item):
  issue = item["Issue"]
  issue_data = [issue["Name"], issue["Accuracy"], issue["IcdName"]]

  translator = Translator()
  translations = translator.translate(issue_data, src="en", dest="vi")

  result = {
    "Name": translations[0].text,
    "Arrcuracy": translations[1].text,
    "IcdName": translations[2].text
  }
  return result

def get_query_string(sentence):
  symptom_string = get_quote_content(sentence)
  ids = get_match_symptom_input_ID(symptom_string)
  ids = json.dumps(ids)
  return {"gender":"male","year_of_birth":"1984","symptoms": ids,"language":"en-gb"}


def get_match_symptom_input_ID(inp):
  inp_symptoms = inp.split(',')
  result = []
  for symptom in inp_symptoms:
    match = get_best_match_item_ID(symptom, data["symptoms"])
    if match!= None:
      result.append(match)
  return result

