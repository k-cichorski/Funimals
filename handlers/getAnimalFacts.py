import requests
from .handleErrors import handleRequestErrors, raiseGeneralError
from helperFunctions import getResponseObject
from .handleTranslation import handleTextTranslation
from .handleCsvEmail import handleCsvEmail
from flask import redirect, url_for, request

def getAnimalFacts(animal, amount, sendTo, translateTo, useAltFactSrc, maxLength):
  if useAltFactSrc:
    factsApi = 'https://catfact.ninja/facts'
    factKey = 'fact'
    params = {
      'limit': str(amount),
      'max_length': str(maxLength)
    }
  else:
    factsApi = 'https://cat-fact.herokuapp.com/facts/random' 
    factKey = 'text'
    params = {
      'animal_type': str(animal),
      'amount': str(amount)
    }
  headers = {
    'Accept': 'application/json'
  }
  try:
    response = requests.get(factsApi, params=params, headers=headers)
  except Exception as error:
    raiseGeneralError(lambda: handleRequestErrors(error))
  
  if not response.ok:
    if useAltFactSrc:
      return response.reason, response.status_code
    else:
      newArgs = {
        **request.args,
        'useAltFactSrc': True
      }
      return redirect(url_for('.route_getAnimalFacts', **newArgs))
      # return response.text, response.status_code
  else:
    response = response.json()

    if useAltFactSrc:
      response = response['data']

    animalFacts = []
    if type(response) == list:
      for factDict in response:
        animalFacts.append(factDict[factKey])
    else:
      animalFacts.append(response[factKey])

    originalAnimal = animal

    if translateTo is not None:
      animal, *animalFacts = handleTextTranslation([animal, *animalFacts], translateTo)

    returnData = {
      'animal': animal,
      'facts': animalFacts,
      'sendTo': sendTo,
      'translateTo': translateTo
    }

    if sendTo is not None:
      handleCsvEmail(animalFacts, sendTo, originalAnimal, translateTo)

    return getResponseObject(returnData)
