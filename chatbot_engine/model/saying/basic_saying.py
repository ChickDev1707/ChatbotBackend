import random
import sys
from pathlib import Path

utils_path = str(Path(__file__).parent.parent.absolute().joinpath('utils'))
sys.path.append(utils_path)
from io_util import get_success_response

def get_saying_result(intent):
  result = random.choice(intent['responses'])
  return get_success_response(tag= intent["tag"], data= result)
