import os
from dotenv import load_dotenv
import json

load_dotenv()
SERVER_PORT = os.environ.get('SERVER_PORT')

def handleAmount(amount):
  if type(amount) == int:
    return (True, amount)
  else:
    try:
      amount = int(amount)
      if amount > 500:
        errorMsg = '500 facts is maximum!'
        return False, getResponseObject(error=errorMsg, code=400)
      elif amount ==  0:
        errorMsg = '1 fact is minimum!'
        return False, getResponseObject(error=errorMsg, code=400)
      return True, amount
    except ValueError:
      return False, handleIncorrectUrl()

def handleIncorrectUrl(amount=None, errorMsg=None):
  if amount is None:
    amount = 5
  if errorMsg is None:
    link = f'http://localhost:{SERVER_PORT}/cat/{amount}'
    errorMsg = f'Something\'s not right! Try {link} (only cats available right now!).'
  return getResponseObject(error=errorMsg, code=400)

def getResponseObject(data=None, error=None, code=200):
  return ({
    'data': data,
    'error': error
  }, code)
