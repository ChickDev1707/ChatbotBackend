import sys
import requests
from pathlib import Path
from googletrans import Translator

utils_path = str(Path(__file__).parent.parent.absolute().joinpath('utils'))
sys.path.append(utils_path)

from string_util import get_quote_content

def get_drug_search_result(sentence, intent):
  drug_name = get_quote_content(sentence)
  result = get_drug_api_result(drug_name, intent)

  translator = Translator()
  translation = translator.translate(result, src="en", dest="vi")
  return translation.text

def get_query_string(drug_name):
  search_value = "openfda.brand_name:"+ drug_name
  return {
    "search": search_value,
    "limit": 1
  }

def get_drug_api_result(drug_name, intent):
  query_string = get_query_string(drug_name)
  url = intent["api"]["url"]
  response = requests.request("GET", url, params=query_string)
  drugInfo = response.json()
  label = intent['tag']
  result = drugInfo["results"][0][label][0]
  return result
