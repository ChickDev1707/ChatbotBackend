import requests

def get_response_with_exception(url, **kwargs):
  try:
    response = requests.request("GET", url, **kwargs)
    return response
  except:
    raise Exception("Lỗi khi lấy dữ liệu")

def get_success_response(tag, data):
  return {
    "status": "OK",
    "response": {
      "tag": tag,
      "data": data
    }
  }
def get_fail_response(message):
  return {
    "status": "FAILED",
    "message": message
  }
