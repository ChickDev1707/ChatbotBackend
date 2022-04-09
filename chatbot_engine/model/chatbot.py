from utils.bot import get_result

def chat():
  print("Start talking with the bot (type quit to stop)!")
  while True:
    inp = input("You: ")
    if inp.lower() == "quit":
      break
  
    result = get_result(inp)
    print(result)

chat()