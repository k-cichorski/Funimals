import os
from flask import Flask, request
from flask_mail import Mail
from dotenv import load_dotenv
from handlers.getAnimalFacts import getAnimalFacts
from helperFunctions import getResponseObject, handleIncorrectUrl

load_dotenv()

app = Flask(__name__)
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')
mail = Mail(app)

SERVER_PORT = os.environ.get('SERVER_PORT')
BASE_URL = os.environ.get('BASE_URL')
DEBUG = os.environ.get('DEBUG')

@app.route('/')
def route_index():
  return getResponseObject(f'''Try a request like this: {BASE_URL}/facts/?animal=cat&amount=5 (only cats available right now!).
  Additional options:
  - Add an email argument to get up to 10 facts sent to you in a CSV file.
  - Add a translateTo argument equal to a language shorthand to have your facts translated.''')

@app.route('/facts/')
def route_getAnimalFacts():
  animal = request.args.get('animal')
  amount = request.args.get('amount')
  email = request.args.get('email')
  translateTo = request.args.get('translateTo')
  if animal is not None and amount is not None:
    return getAnimalFacts(animal, amount, email, translateTo, mail)
  return handleIncorrectUrl(amount)

if __name__ == '__main__':
  app.run(port=SERVER_PORT, debug=DEBUG)
