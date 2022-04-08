import sys
import requests
from pathlib import Path

utils_path = str(Path(__file__).parent.parent.absolute().joinpath('utils'))
sys.path.append(utils_path)

from string_util import get_quote_content
from io_util import get_response_with_exception, get_success_response, get_fail_response

def get_location_search_result(sentence, intent):
  try:
    location = get_location(sentence, intent)
    return get_success_response(tag= intent["tag"], data= location)
  except Exception as e:
    return get_fail_response(str(e))

def get_location(sentence, intent):
  url = intent["api"]["url"]
  key = intent["api"]["key"]
  query_string = get_query_string(sentence, key)
  response = get_response_with_exception(url, params= query_string)
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
