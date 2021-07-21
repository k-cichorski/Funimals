from helperFunctions import getResponseObject

def handleRequestErrors(error):
  if type(error).__name__ == 'HTTPError':
    _, error = vars(error).values()
    return getResponseObject(errors=error, code=error.response.status_code)
  elif type(error).__name__ == 'ConnectionError':
    return getResponseObject(errors='Connection error', code=502)
  elif type(error).__name__ == 'Timeout':
    return getResponseObject(errors='Connection timeout', code=504)
  else:
    return getResponseObject(errors='An internal server error ocurred. Please contact server administrator.', code=500)

def handleTranslationErrors(error):
  error = vars(error)
  print(error)
  return getResponseObject(errors=error['message'], code=error['_response'].status_code)

def handleHttpErrors(error):
  return getResponseObject(errors=f'{error.name}: {error.description}', code=error.code)

class GeneralError(Exception):
  pass

def raiseGeneralError(handler):
  data, code = handler()
  raise GeneralError(data, code)
