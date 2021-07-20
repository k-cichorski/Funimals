from handlers.handleErrors import handleRequestErrors
import re, requests
from requests.exceptions import HTTPError, ConnectionError, Timeout
from helperFunctions import handleIncorrectUrl, handleAmount, getResponseObject
from handlers.handleTranslation import handleTranslation
from .handleCsvEmail import handleCsvEmail

def getAnimalFacts(animal, amount, email, translateTo, mail):
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
  except Exception as error:
    return handleRequestErrors(error)

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

    if translateTo is not None:
      ok, translationError, animalFacts, animal = handleTranslation(animalFacts, animal, translateTo)
      if not ok:
        return translationError
    
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
