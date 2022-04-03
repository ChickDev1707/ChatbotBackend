import requests

def get_covid_info(intent):
  url = intent["api"]["url"]
  headers = intent["api"]["headers"]
  response = requests.request("GET", url=url, headers=headers)
  result = response.json()[0]

  result = {
    "last_updated_date": result["last_updated_date"],
    "total_cases": result["total_cases"],
    "new_cases": result["new_cases"],
    "total_deaths": result["total_deaths"],
    "new_deaths": result["new_deaths"]
  }
  return result
