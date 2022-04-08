
import re
import nltk
import numpy
from thefuzz import fuzz
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

def get_quote_content(sentence):
	try:
		pattern = r'"(.*)"'
		m = re.search(pattern, sentence)
		return m.group().replace('"', '').lower()
	except:
		raise Exception('Không xác định được từ khóa tìm kiếm, hãy nhập từ khóa tìm kiếm trong cặp ngoặc kép ""')

def get_best_match_item_ID(inp, items):
  MATCH_RATIO = 70
  match = None
  maxRatio = 0
  for item in items:
    ratio = fuzz.token_sort_ratio(inp.lower(), item["Name"].lower())
    if ratio> maxRatio:
      maxRatio = ratio
      match = item["ID"]
  if maxRatio> MATCH_RATIO:
    return match
  else:
    return None

# sentence

def clean_up_sentence(sentence):
  s_words = nltk.word_tokenize(sentence)
  s_words = [stemmer.stem(word.lower()) for word in s_words]
  return s_words

def bag_of_words(words, sentence):
  s_words = clean_up_sentence(sentence)
  bag = [0] * len(words)
  for se in s_words:
    for i, w in enumerate(words):
      if w == se:
        bag[i] = 1
          
  return numpy.array(bag)