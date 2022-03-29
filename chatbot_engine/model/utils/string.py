
import re

def get_quote_content(sentence):
  pattern = r'"(.*)"'
  m = re.search(pattern, sentence)
  return m.group().replace('"', '')
