
import json
import requests
import sys
import os

from pathlib import Path
from thefuzz import fuzz
from googletrans import Translator

dirname = os.path.dirname(__file__)
utils_path = str(Path(__file__).parent.parent.absolute().joinpath('utils'))
sys.path.append(utils_path)

from sentence import get_quote_content

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
  ids = getMatchedSymptomsInputID(symptom_string)
  ids = json.dumps(ids)
  return {"gender":"male","year_of_birth":"1984","symptoms": ids,"language":"en-gb"}


def getMatchedSymptomsInputID(inp):
  inp_symptoms = inp.split(',')
  result = []
  for symptom in inp_symptoms:
    match = getMatchedSymptomsID(symptom)
    result.extend(match)
  return result

def getMatchedSymptomsID(inp):
  matches = []
  for symptom in data["symptoms"]:
    if isStringMatch(inp, symptom["Name"]):
      matches.append(symptom["ID"])
  return matches

def isStringMatch(inp, target):
  MATCH_RATIO = 90
  ratio = fuzz.token_sort_ratio(inp.lower(), target.lower())
  if ratio > MATCH_RATIO:
    return True
  else:
    return False
