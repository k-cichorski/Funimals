import os
import pandas as pd
import numpy as np
from .handleErrors import handleRequestErrors, raiseGeneralError
from flask_mail import Message
from smtplib import SMTPException
from helperFunctions import getResponseObject
from .handleTranslation import handleTextTranslation
from extensions import mail

API_EMAIL = os.environ.get('API_EMAIL')
API_EMAIL_PASSWORD = os.environ.get('API_EMAIL_PASSWORD')
SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_PORT = os.environ.get('SMTP_PORT')

def handleCsvEmail(facts, sendTo, animal, translateTo):
  csvFilePath = './temp/facts.csv'
  animalFactsHeader = f'{animal.capitalize()} Facts'
  emailSubject = f'Here are Your {animalFactsHeader}!'
  if len(facts) > 10:
    facts = facts[0:10]

  if translateTo:
    animalFactsHeader, emailSubject= handleTextTranslation([animalFactsHeader, emailSubject], translateTo)

  factsDict = {
    animalFactsHeader: facts
  }

  df = pd.DataFrame(factsDict)
  df.index = np.arange(1, len(df) + 1)
  df.to_csv(csvFilePath)

  emailMessage = Message(
    subject=emailSubject,
    recipients=[sendTo]
  )

  with open(csvFilePath) as fp:
    emailMessage.attach(f'{animalFactsHeader}.csv', 'text/csv', fp.read())
  try:
    mail.send(emailMessage)
  except SMTPException as smtp_exception:
    exceptionVars = vars(smtp_exception)
    if not bool(exceptionVars):
      raiseGeneralError(lambda: handleRequestErrors(error=smtp_exception))
    code, error = vars(smtp_exception).values()
    raiseGeneralError(lambda: getResponseObject(errors=error.decode(), code=code))
  
  finally:
    os.remove(csvFilePath)
  return