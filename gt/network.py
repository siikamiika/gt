"""
This module contains an URL construction and fetching function.
"""
from urllib.parse import quote_plus
from urllib.request import Request, urlopen
from random import randint
import time
import ctypes

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0'

### https://github.com/soimort/translate-shell/issues/94#issuecomment-165433715
def RL(a, b):
    for c in range(0, len(b)-2, 3):
        d = b[c+2]
        d = ord(d) - 87 if d >= 'a' else int(d)
        xa = ctypes.c_uint32(a).value
        d = xa >> d if b[c+1] == '+' else xa << d
        a = a + d & 4294967295 if b[c] == '+' else a ^ d
    return ctypes.c_int32(a).value


def calc_tk(a):
    b = int(time.time() / 3600)
    d = a.encode('utf-8')
    a = b
    for di in d:
        a = RL(a + di, '+-a^+6')
    a = RL(a, '+-3^+b+-f')
    a = a if a >= 0 else ((a & 2147483647) + 2147483648)
    a %= pow(10, 6)
    return '%d.%d' % (a, a ^ b)
###

def fetch_response(source_lang, target_lang, text,
                   include_translation=True, include_translit=False,
                   include_variants=False, include_segments=False,
                   include_examples=False, include_definitions=False,
                   include_see_also=False, include_synonyms=False,
                   suggest_language=False, correct_typos=False,
                   interface_lang=None):
    """
    Fetches Google Translate's response as a string.

    Args:
        source_lang: source language code
        target_lang: target language code
        text: text to translate
        include_translation: include the translation itself
        include_translit: include transcriptions/transliterations of original
            and translated texts
        include_variants: include speech-part specific translations for a word
        include_segments: include translation of segments (words) for a text
        include_examples: include usage examples for a word
        include_definitions: include definition for a word
        include_see_also: include the "see also" list for a word
        include_synonyms: include the synonyms list for a word
        suggest_language: suggest another source language(s)
        correct_typos: suggest typo fixes
        interface_lang: code of a language will be used to name speech parts
            (default: English)

    Returns:
        response as a string
    """
    url = 'https://translate.google.com/translate_a/single?client=t'
    url += '&sl=' + quote_plus(source_lang) + \
           '&tl=' + quote_plus(target_lang) + \
           '&tk=' + calc_tk(text) + \
           '&q=' + quote_plus(text)

    if include_translation:
        # 't' is for 'translation'
        url += '&dt=t'
    if include_translit:
        url += '&dt=rm'
    if include_variants:
        url += '&dt=bd'
    if include_segments:
        # 'at' is for 'alternative translations'
        url += '&dt=at'
    if include_examples:
        # 'ex' is for 'examples'
        url += '&dt=ex'
    if include_definitions:
        url += '&dt=md'
    if include_see_also:
        url += '&dt=rw'
    if include_synonyms:
        # 'ss' is for 'source synonyms'
        url += '&dt=ss'
    if suggest_language:
        # 'ld' is for 'language detect'
        url += '&dt=ld'
    if correct_typos:
        # 'qc' is for 'quick correct'
        url += '&dt=qc'
    if interface_lang is not None:
        # 'hl' is for 'home language'
        url += '&hl=' + quote_plus(interface_lang)

    request = Request(url)
    request.add_header('User-Agent', USER_AGENT)

    response = urlopen(request)
    return response.read().decode('utf-8')
