
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

with open(os.path.join(dirname, 'symptoms.json')) as file:
  data = json.load(file)

def get_symptom_check_result(sentence, intent):
  try:
    symptom_check = get_symptom_check(sentence, intent)
    return get_success_response(sentence, intent)
  except Exception as e:
    return get_fail_response(str(e))

def get_symptom_check(sentence, intent):
  query_string = get_query_string(sentence)
  url = intent["api"]["url"]
  headers = intent["api"]["headers"]
  response = get_response_with_exception("GET", url, headers=headers, params=query_string)
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
    "name": translations[0].text,
    "arrcuracy": translations[1].text,
    "icdName": translations[2].text
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
  if len(result) == 0:
    raise Exception("Không xác định được các triệu chứng")
  else:
    return result

