from helperFunctions import getResponseObject

def handleRequestErrors(error):
  if type(error).__name__ == 'HTTPError':
    _, error = vars(error).values()
    return getResponseObject(error=error, code=error.response.status_code)
  elif type(error).__name__ == 'ConnectionError':
    return getResponseObject(error='Connection error', code=502)
  elif type(error).__name__ == 'Timeout':
    return getResponseObject(error='Connection timeout', code=504)
  else:
    return getResponseObject(error='An internal server error ocurred. Please contact server administrator.', code=500)