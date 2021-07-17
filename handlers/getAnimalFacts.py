import requests
from requests.exceptions import HTTPError
from helperFunctions import handleIncorrectUrl, handleAmount

def getAnimalFacts(animal, amount):
  amount = handleAmount(amount)
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
    return f'<p>HTTP error ocurred: {http_err}'
  except Exception as exc:
    return f'<p>Exception ocurred: {exc}'

  if response.ok is False:
    return f'{response.text}'
  else:
    response = response.json()
    return f'<p>{response}</p>'


