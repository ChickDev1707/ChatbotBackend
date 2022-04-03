import sys
import requests
from pathlib import Path

utils_path = str(Path(__file__).parent.parent.absolute().joinpath('utils'))
sys.path.append(utils_path)

from string_util import get_quote_content

def get_location_search_result(sentence, intent):
  location_name = get_quote_content(sentence)
  url = intent["api"]["url"]
  key = intent["api"]["key"]
  query_string = get_query_string(location_name, key)
  response = requests.request("GET", url, params=query_string)
  return response.json()

def get_query_string(location_name, key):
  fields = ["formatted_address", "name", "rating", "geometry"]
  fields_string = ",".join(fields)

  query_string={
    "input": location_name,
    "inputtype": "textquery",
    "fields": fields_string,
    "key": key
  }
  return query_string
