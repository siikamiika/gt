"""
This module contains an URL construction and fetching function.
"""
from urllib.parse import quote_plus
from urllib.request import Request, urlopen

USER_AGENT = 'Mozilla/5.0'

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
    url = 'http://translate.google.com/translate_a/single?client=t'
    url += '&sl=' + quote_plus(source_lang) + \
           '&tl=' + quote_plus(target_lang) + \
           '&q=' + quote_plus(text)

    if include_translation:
        url += '&dt=t'
    if include_translit:
        url += '&dt=rm'
    if include_variants:
        url += '&dt=bd'
    if include_segments:
        url += '&dt=at'
    if include_examples:
        url += '&dt=ex'
    if include_definitions:
        url += '&dt=md'
    if include_see_also:
        url += '&dt=rw'
    if include_synonyms:
        url += '&dt=ss'
    if suggest_language:
        url += '&dt=ld'
    if correct_typos:
        url += '&dt=qc'
    if interface_lang is not None:
        url += '&hl=' + quote_plus(interface_lang)

    request = Request(url)
    request.add_header('User-Agent', USER_AGENT)

    response = urlopen(request)
    return response.read().decode('utf-8')
