"""Contains various network/URL construction functions"""
from urllib2 import Request, urlopen
from urllib import quote_plus

def fetch_response(source_lang, target_lang, text):
    url = 'http://translate.google.com/translate_a/t?client=t&'\
          'text={text}&sl={sl}&tl={tl}'.format(
              text=quote_plus(text),
              sl=quote_plus(source_lang),
              tl=quote_plus(target_lang))

    request = Request(url)

    request.add_header('User-Agent', 'Mozilla/5.0')

    response = urlopen(request)
    try:
        return response.read()
    finally:
        response.close()

def get_speech_url(lang, text):
    return 'http://translate.google.com/translate_tts?ie=UTF-8&'\
           'tl={lang}&q={text}'.format(
               lang=quote_plus(lang), text=quote_plus(text))
