import handlers.handleErrors as handleErrors
import os

BASE_URL = os.environ.get('BASE_URL')

def handleAmount(amount):
  if type(amount) == int:
    return amount
  else:
    try:
      amount = int(amount)
      if amount > 500:
        errorMsg = '500 facts is maximum!'
        handleErrors.raiseGeneralError(lambda: getResponseObject(error=errorMsg, code=400))
      elif amount ==  0:
        errorMsg = '1 fact is minimum!'
        handleErrors.raiseGeneralError(lambda: getResponseObject(error=errorMsg, code=400))
      return amount
    except ValueError:
      handleErrors.raiseGeneralError(handleIncorrectUrl)

def handleIncorrectUrl(amount=None):
  if amount == None:
    amount = 5
  link = f'{BASE_URL}/facts/?animal=cat&amount={amount}'
  errorMsg = f'Something\'s not right! Try {link} (only cats available right now!). Make a request to {BASE_URL} for more information.'
  handleErrors.raiseGeneralError(lambda: getResponseObject(error=errorMsg, code=400))

def getResponseObject(data=None, error=None, code=200):
  return ({
    'data': data,
    'error': error
  }, code)
