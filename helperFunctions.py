import os, re
import handlers.handleErrors as handleErrors

BASE_URL = os.environ.get('BASE_URL')

def verifyAmount(amount, maxAmount):
  try:
    amount = int(amount)
    if amount > maxAmount:
      error = f'{maxAmount} facts is maximum!'
    elif amount ==  0:
      error = '1 fact is minimum!'
    else:
      error = None
    return error
  except ValueError:
    return 'Make sure the amount argument is an integer!'

def verifyArguments(animal, amount, sendTo, useAltFactSrc):
  errors = []
  if animal is not None:
    if animal.lower() != 'cat':
      errors.append('Only cat facts available right now!')
  else:
    errors.append('Argument \'animal\' is required (only cat facts available right now)!')

  if useAltFactSrc:
    maxAmount = 1000
  else:
    maxAmount = 500
  if amount is not None:
    amountErrors = verifyAmount(amount, maxAmount)
    if amountErrors is not None:
      errors.append(amountErrors)
  else:
    errors.append(f'Argument \'amount\' is required (1-{maxAmount})!')

  if sendTo is not None:
    if not re.match('[^@]+@[^@]+\.[^@]+$', sendTo):
      errors.append('Incorrect email format!')
  
  if len(errors) > 0:
    raise handleErrors.raiseGeneralError(lambda: getResponseObject(errors=errors, code=400))
  return


def getResponseObject(data=None, errors=None, code=200):
  if type(errors) is str:
    errors = [errors]
  return ({
    'data': data,
    'errors': errors
  }, code)
