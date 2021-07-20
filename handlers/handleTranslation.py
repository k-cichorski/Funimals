import requests, os
from helperFunctions import getResponseObject
from handlers.handleErrors import handleRequestErrors

X_RAPIDAPI_KEY = os.environ.get('X_RAPIDAPI_KEY')

def handleTranslation(facts, animal, translateTo):
  data = {
      'q': [animal, *facts],
      'target': translateTo
    }
  headers = {
    'content-type': 'application/x-www-form-urlencoded',
    'accept-encoding': 'application/gzip',
    'x-rapidapi-key': X_RAPIDAPI_KEY,
    'x-rapidapi-host': 'google-translate1.p.rapidapi.com'
  }
  try:
    response = requests.post('https://google-translate1.p.rapidapi.com/language/translate/v2', data=data, headers=headers)
  except Exception as error:
    return False, handleRequestErrors(error), None, None
  
  response = response.json()
  responseData = response.get('data')
  if responseData is None:
    return False, getResponseObject(
      error='Bad language shorthand. Make sure your shorthand is supported: https://cloud.google.com/translate/docs/languages',
      code=400
    ), None, None
  translations = responseData.get('translations')
  animal = translations[0].get('translatedText')
  translatedFacts = [translation.get('translatedText') for translation in translations[1:]]
  return True, None, translatedFacts, animal