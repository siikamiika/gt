"""Contains the `fetch' function for fetching Google Translate response"""
from urllib2 import Request, urlopen
from urllib import quote_plus

USER_AGENT = 'Mozilla/5.0'
URL_FMT = 'http://translate.google.com/translate_a/t?client=t'\
          '&text={text}&sl={sl}&tl={tl}'

def fetch(source_lang, target_lang, text):
    url = URL_FMT.format(text=quote_plus(text),
                         sl=quote_plus(source_lang),
                         tl=quote_plus(target_lang))

    request = Request(url)

    request.add_header('User-Agent', USER_AGENT)

    response = urlopen(request)
    try:
        return response.read()
    finally:
        response.close()
