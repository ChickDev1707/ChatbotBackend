import sys
from pathlib import Path

utils_path = str(Path(__file__).parent.parent.absolute().joinpath('utils'))
sys.path.append(utils_path)

from io_util import get_response_with_exception, get_success_response, get_fail_response

def get_covid_info_result(intent):
  try:
    covid_info = get_covid_info(intent)
    return get_success_response(tag= intent["tag"], data= covid_info)
  except Exception as e:
    return get_fail_response(str(e))

def get_covid_info(intent):
  url = intent["api"]["url"]
  headers = intent["api"]["headers"]
  response = get_response_with_exception(url, headers= headers)
  result = response.json()[0]

  result = {
    "lastUpdatedDate": result["last_updated_date"],
    "totalCases": result["total_cases"],
    "newCases": result["new_cases"],
    "totalDeaths": result["total_deaths"],
    "newDeaths": result["new_deaths"]
  }
  return result
