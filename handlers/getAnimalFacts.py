import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout
from helperFunctions import handleIncorrectUrl, handleAmount, getResponseObject

def getAnimalFacts(animal, amount):
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
    return getResponseObject(error=http_err, code=http_err.response.status_code)
  except ConnectionError:
    return getResponseObject(error='Connection error', code=502)
  except Timeout:
    return getResponseObject(error='Connection timeout', code=504)
  except Exception:
    return getResponseObject(error='An internal server error ocurred. Please contact server administrator.', code=500)

  if not response.ok: 
    return response.text, response.status_code
  else:
    response = response.json()
    catFacts = []
    if type(response) == list:
      for factDict in response:
        catFacts.append(factDict['text'])
    else:
      catFacts.append(response['text'])
    return getResponseObject({
      'facts': catFacts
    })
