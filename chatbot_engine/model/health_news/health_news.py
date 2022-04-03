import requests
from googletrans import Translator

def get_health_news(intent):
  url = intent["api"]["url"]
  headers = intent["api"]["headers"]
  response = requests.request("GET", url=url, headers=headers)
  result = response.json()
  result ={
    "news": get_translation_result(result["news"])
  }
  return result

def get_translation_result(news_list):
  translated_result = []
  NO_NEWS = 3
  i = 0;
  while i< NO_NEWS:
    news = news_list[i]
    translated_issue = get_translated_news(news)
    translated_result.append(translated_issue)
    i+= 1
  return translated_result

def get_translated_news(news):
  news_data = [news["title"], news["description"]]

  translator = Translator()
  translations = translator.translate(news_data, src="en", dest="vi")

  result = {
    "title": translations[0].text,
    "description": translations[1].text,
    "url": news["url"]
  }
  return result