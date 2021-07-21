import os
from flask import Flask, request
from extensions import mail
from dotenv import load_dotenv
from werkzeug.exceptions import HTTPException
from handlers.getAnimalFacts import getAnimalFacts
from handlers.handleErrors import GeneralError, handleHttpErrors
from helperFunctions import getResponseObject, verifyArguments

load_dotenv()

app = Flask(__name__)
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')
app.config['JSON_AS_ASCII'] = False
app.url_map.strict_slashes = False
mail.init_app(app)

SERVER_PORT = os.environ.get('SERVER_PORT')
BASE_URL = os.environ.get('BASE_URL')
DEBUG = os.environ.get('DEBUG')

@app.route('/')
def route_index():
  return getResponseObject(f'''Try a request like this: {BASE_URL}/facts?animal=cat&amount=5 (only cat facts available right now!).
Additional options:
- Add a sendTo argument equal to a valid email address to get up to 10 facts sent to you in a CSV file.
- Add a translateTo argument equal to a language shorthand to have your facts translated.
- You can add useAltFactSrc=true to request params (serving only cat facts) to use alternate fact source. Add maxLength argument to limit fact char length.''')

@app.route('/facts')
def route_getAnimalFacts():
  useAltFactSrc = request.args.get('useAltFactSrc')
  animal = request.args.get('animal', 'cat')
  if useAltFactSrc is not None:
    useAltFactSrc = useAltFactSrc.lower() == 'true'
  amount = request.args.get('amount')
  sendTo = request.args.get('sendTo')
  verifyArguments(animal, amount, sendTo, useAltFactSrc)
  translateTo = request.args.get('translateTo')
  maxLength = request.args.get('maxLength')
  return getAnimalFacts(animal, amount, sendTo, translateTo, useAltFactSrc, maxLength)

@app.errorhandler(HTTPException)
def handler_httpError(error):
  return handleHttpErrors(error)

@app.errorhandler(GeneralError)
def handler_generalError(error):
  data, code = error.args
  return data, code

if __name__ == '__main__':
  app.run(port=SERVER_PORT, debug=DEBUG)
