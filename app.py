import os
from flask import Flask
from dotenv import load_dotenv
from handlers.getAnimalFacts import getAnimalFacts

load_dotenv()

app = Flask(__name__)
SERVER_PORT = os.environ.get('SERVER_PORT')
DEBUG = os.environ.get('DEBUG')

@app.route('/')
def route_index():
  return f'<p>Try a request like this: <a href="http://localhost:{SERVER_PORT}/cat/1">http://localhost:{SERVER_PORT}/cat/1</a> (only cats available right now!).</p>'

@app.route('/<animal>/<amount>')
def route_getAnimalFacts(animal, amount):
  return getAnimalFacts(animal, amount)

if __name__ == '__main__':
  app.run(port=SERVER_PORT, debug=DEBUG)