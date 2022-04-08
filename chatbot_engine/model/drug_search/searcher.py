import sys
from pathlib import Path
from googletrans import Translator

utils_path = str(Path(__file__).parent.parent.absolute().joinpath('utils'))
sys.path.append(utils_path)

from string_util import get_quote_content
from io_util import get_response_with_exception, get_success_response, get_fail_response

def get_drug_search_result(sentence, intent):
  try:
    drug_name = get_quote_content(sentence)
    result = get_drug_api_result(drug_name, intent)

    translator = Translator()
    translation = translator.translate(result, src="en", dest="vi")
    return get_success_response(tag= intent["tag"], data= translation.text)
  except Exception as e:
    return get_fail_response(str(e))

def get_query_string(drug_name):
  search_value = "openfda.brand_name:"+ drug_name
  return {
    "search": search_value,
    "limit": 1
  }

def get_drug_api_result(drug_name, intent):
  query_string = get_query_string(drug_name)
  url = intent["api"]["url"]
  response = get_response_with_exception(url, params= query_string)
  drugInfo = response.json()
  if "error" in drugInfo:
    raise Exception("Không tìm thấy thuốc")
  label = intent['tag']
  result = drugInfo["results"][0][label][0]
  return result

