from handlers.handleErrors import handleRequestErrors, raiseGeneralError
import re, requests
from helperFunctions import handleIncorrectUrl, handleAmount, getResponseObject
from handlers.handleTranslation import handleTextTranslation
from .handleCsvEmail import handleCsvEmail

def getAnimalFacts(animal, amount, sendTo, translateTo, mail):
  amount = handleAmount(amount)
  if animal.lower() != 'cat':
    raiseGeneralError(lambda: handleIncorrectUrl(amount))
  
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
    raiseGeneralError(lambda: handleRequestErrors(error))
  
  if not response.ok: 
    return response.text, response.status_code
  else:
    response = response.json()

    animalFacts = []
    if type(response) == list:
      for factDict in response:
        animalFacts.append(factDict['text'])
    else:
      animalFacts.append(response['text'])

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
      if re.match('[^@]+@[^@]+\.[^@]+$', sendTo):
        handleCsvEmail(animalFacts, sendTo, originalAnimal, mail, translateTo)
      else:
        return getResponseObject(error='Incorrect email format', code=400)

    return getResponseObject(returnData)
