from .handleErrors import handleRequestErrors, handleTranslationErrors, raiseGeneralError
from google.cloud import translate_v2 as translate
from google.auth.exceptions import GoogleAuthError

def handleTextTranslation(text, translateTo):
  try:
    translate_client = translate.Client()
    translation = translate_client.translate(text, target_language=translateTo)
  except GoogleAuthError as google_error:
    raiseGeneralError(lambda: handleRequestErrors(google_error))
  except Exception as error:
    raiseGeneralError(lambda: handleTranslationErrors(error))

  if type(text) == list:
    translatedText = [translation.get('translatedText') for translation in translation]
  else:
    translatedText = translation.get('translatedText')
  return translatedText