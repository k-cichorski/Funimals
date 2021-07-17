import os
from dotenv import load_dotenv

load_dotenv()
SERVER_PORT = os.environ.get('SERVER_PORT')

def handleAmount(amount):
  if type(amount) == int:
    return amount
  else:
    try:
      amount = int(amount)
      if amount > 500:
        amount = 500
      return amount
    except ValueError:
      return None

def handleIncorrectUrl(amount=None):
  if amount == None:
    amount = 1
  link = f'http://localhost:{SERVER_PORT}/cat/{amount}'
  return f'<p>Something\'s not right! Try <a href="{link}">{link}</a> (only cats available right now!).'