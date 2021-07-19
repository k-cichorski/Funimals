import re, requests
from requests.exceptions import HTTPError, ConnectionError, Timeout
from helperFunctions import handleIncorrectUrl, handleAmount, getResponseObject
from .handleCsvEmail import handleCsvEmail

def getAnimalFacts(animal, amount, email, mail):
  (amountOk, amountOrResponse) = handleAmount(amount)
  if not amountOk:
    return amountOrResponse
  if animal.lower() != 'cat':
    return handleIncorrectUrl(amount)
  
  params = {
    'animal_type': str(animal),
    'amount': str(amount)
  }
  headers = {
    'Accept': 'application/json'
  }

  try:
    response = requests.get('https://cat-fact.herokuapp.com/facts/random', params=params, headers=headers)
  except HTTPError as http_err:
    _, error = vars(http_err).values()
    return getResponseObject(error=error, code=http_err.response.status_code)
  except ConnectionError:
    return getResponseObject(error='Connection error', code=502)
  except Timeout:
    return getResponseObject(error='Connection timeout', code=504)
  except Exception:
    return getResponseObject(error='An internal server error ocurred. Please contact server administrator.', code=500)

  if False or not response.ok: 
    return response.text, response.status_code
  else:
    response = response.json()

    animalFacts = []
    if type(response) == list:
      for factDict in response:
        animalFacts.append(factDict['text'])
    else:
      animalFacts.append(response['text'])
    
    returnData = {
      'animal': animal,
      'facts': animalFacts,
      'sentTo': None
    }

    if email is not None:
      if re.match('[^@]+@[^@]+\.[^@]+$', email):
        sent, error = handleCsvEmail(animalFacts, email, animal, mail)
        if not sent:
          return error
        else:
          returnData['sentTo'] = email
          return getResponseObject(returnData)

      else:
        return getResponseObject(error='Incorrect email format', code=400)
      

    return getResponseObject(returnData)
