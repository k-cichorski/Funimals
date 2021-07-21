from .handleErrors import handleTranslationErrors, raiseGeneralError
from google.cloud import translate_v2 as translate

def handleTextTranslation(text, translateTo):
  translate_client = translate.Client()
  try:
    translation = translate_client.translate(text, target_language=translateTo)
  except Exception as error:
    raiseGeneralError(lambda: handleTranslationErrors(error))

  if type(text) == list:
    translatedText = [translation.get('translatedText') for translation in translation]
  else:
    translatedText = translation.get('translatedText')
  return translatedText