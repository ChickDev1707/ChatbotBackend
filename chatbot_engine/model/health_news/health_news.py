from googletrans import Translator
import sys
from pathlib import Path

utils_path = str(Path(__file__).parent.parent.absolute().joinpath('utils'))
sys.path.append(utils_path)

from io_util import get_response_with_exception, get_success_response, get_fail_response

def get_health_news_result(intent):
  try:
    health_news = get_health_news(intent)
    return get_success_response(tag= intent["tag"], data= health_news)
  except Exception as e:
    return get_fail_response(str(e))

def get_health_news(intent):
  url = intent["api"]["url"]
  headers = intent["api"]["headers"]
  response = get_response_with_exception(url, headers= headers)
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