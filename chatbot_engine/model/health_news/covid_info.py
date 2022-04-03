import requests

def get_covid_info(intent):
  url = intent["api"]["url"]
  headers = intent["api"]["headers"]
  response = requests.request("GET", url=url, headers=headers)
  result = response.json()[0]

  result = {
    "lastUpdatedDate": result["last_updated_date"],
    "totalCases": result["total_cases"],
    "newCases": result["new_cases"],
    "totalDeaths": result["total_deaths"],
    "newDeaths": result["new_deaths"]
  }
  return result
