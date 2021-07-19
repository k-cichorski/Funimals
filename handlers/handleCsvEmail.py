import pandas as pd
import os
from dotenv import load_dotenv
from flask_mail import Message
from smtplib import SMTPException
from helperFunctions import getResponseObject

load_dotenv()

API_EMAIL = os.environ.get('API_EMAIL')
API_EMAIL_PASSWORD = os.environ.get('API_EMAIL_PASSWORD')
SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_PORT = os.environ.get('SMTP_PORT')

def handleCsvEmail(facts, email, animal, mail):
  header = f'{animal.capitalize()} Facts'
  csvFilePath = './temp/facts.csv'
  if len(facts) > 10:
    facts = facts[0:10]
  factsDict = {
    header: facts
  }
  pd.DataFrame(factsDict).to_csv(csvFilePath)
  emailMessage = Message(
    subject=f'Here are Your {header}!',
    recipients=[email]
  )
  with open(csvFilePath) as fp:
    emailMessage.attach(f'{animal}_facts.csv', 'text/csv', fp.read())
  try:
    mail.send(emailMessage)
  except SMTPException as smtp_exception:
    code, error = vars(smtp_exception).values()
    return False, getResponseObject(error=error.decode(), code=code)
  finally:
    os.remove(csvFilePath)

  return True, None