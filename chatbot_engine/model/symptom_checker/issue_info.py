
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

with open(os.path.join(dirname, 'issues.json')) as file:
  data = json.load(file)

def get_issue_info(sentence, intent):
  query_string = {"language":"en-gb"}
  headers = intent["api"]["headers"]
  url = intent["api"]["url"]

  issue_ID = get_issue_ID(sentence, data["Issues"])
  url = url.replace("ISSUE_ID", str(issue_ID))

  response = requests.request("GET", url, headers=headers, params=query_string)
  result = response.json()
  return get_translation_result(result)

def get_issue_ID(sentence, issues):
  issue_name = get_quote_content(sentence)
  issue_ID = get_best_match_item_ID(issue_name, issues)
  return issue_ID

def get_translation_result(issue):
  issue_data = [issue["Name"], issue["DescriptionShort"], issue["MedicalCondition"], issue["PossibleSymptoms"], issue["TreatmentDescription"]]

  translator = Translator()
  translations = translator.translate(issue_data, src="en", dest="vi")

  result = {
    "name": translations[0].text,
    "descriptionShort": translations[1].text,
    "medicalCondition": translations[2].text,
    "possibleSymptoms": translations[3].text,
    "treatmentDescription": translations[4].text,
  }
  return result


