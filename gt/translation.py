"""
This module contains data structures that reflect Google Translate response.
"""

def _list_get(obj, *indices):
    """
    Safely obtains an object from nested lists. Returns None in case of an
    error - that is, if on some step an object fetched is not a list or if the
    next index is invalid.

    >>> _list_get([1, 2, 3], 2)
    3
    >>> _list_get([1, 2, 3], 3) # invalid index, returns None
    >>> _list_get([[1, 2, 3], [4, [5, 6]], 7], 1, 1, 0)
    5
    >>> _list_get([[1, 2], 3], 1, 0) # not a list, returns None
    """
    for index in indices:
        if not isinstance(obj, list):
            return None
        if index >= len(obj):
            return None
        obj = obj[index]
    return obj

def _list(obj):
    """
    Returns the original object if it is a list, or an empty list.

    >>> _list([])
    []
    >>> _list([1, 2, 3])
    [1, 2, 3]
    >>> _list(None)
    []
    """
    return obj if isinstance(obj, list) else []

def _str(obj):
    """
    Returns the original object if it is a string, or an empty string.

    >>> _str('')
    ''
    >>> _str('abc')
    'abc'
    >>> _str(None)
    ''
    """
    return obj if isinstance(obj, str) else ''

class SpeechPartSpecificVariants:
    class SpeechPartSpecificVariant:
        translation = None
        synonyms = None
        weight = None

        def __init__(self, json_obj):
            self.translation = _list_get(json_obj, 0)
            self.synonyms = _list_get(json_obj, 1)
            self.weight = _list_get(json_obj, 3)

    speech_part = None
    variants = None
    max_weight = None

    def __init__(self, json_obj):
        self.speech_part = _list_get(json_obj, 0)
        self.variants = [self.SpeechPartSpecificVariant(obj) for obj
                         in _list(_list_get(json_obj, 2))]
        self.max_weight = max((v.weight for v in self.variants if v.weight),
                              default=0)

class SegmentTranslation:
    original_segment = None
    translations = None

    def __init__(self, json_obj):
        self.original_segment = _list_get(json_obj, 0)
        self.translations = [_list_get(obj, 0) for obj
                             in _list(_list_get(json_obj, 2))]

class LanguageSuggestion:
    language = None
    weight = None

    def __init__(self, language, weight):
        self.language = language
        self.weight = weight

class SpeechPartSpecificSynonyms:
    speech_part = None
    synonyms = None
    dict_entry = None

    def __init__(self, json_obj):
        self.speech_part = _list_get(json_obj, 0)
        self.synonyms = _list_get(json_obj, 1, 0, 0)
        self.dict_entry = _list_get(json_obj, 1, 0, 1)

class SpeechPartSpecificDefinitions:
    class SpeechPartSpecificDefinition:
        definition = None
        dict_entry = None
        example = None

        def __init__(self, json_obj):
            self.definition = _list_get(json_obj, 0)
            self.dict_entry = _list_get(json_obj, 1)
            self.example = _list_get(json_obj, 2)

    speech_part = None
    definitions = None

    def __init__(self, json_obj):
        self.speech_part = _list_get(json_obj, 0)
        self.definitions = [self.SpeechPartSpecificDefinition(obj) for obj
                            in _list(_list_get(json_obj, 1))]

class UsageExample:
    example_html = None
    dict_entry = None

    def __init__(self, json_obj):
        self.example_html = _list_get(json_obj, 0)
        self.dict_entry = _list_get(json_obj, 5)

class Correction:
    """
    Correction.

    corrected_text is 'None' when no corrections were made.

    corrected_html can be 'None' when corrected_text is not - e.g. when Google
    Translate "corrects" a transliteration to a different writing system.
    """
    corrected_text = None
    corrected_html = None

    def __init__(self, json_obj):
        self.corrected_html = _list_get(json_obj, 0)
        self.corrected_text = _list_get(json_obj, 1)

class Translation:
    translation = None
    original = None
    translation_translit = None
    original_translit = None
    source_lang = None
    speech_part_variants = None
    segments = None
    correction = None
    lang_suggests = None
    speech_part_synonyms = None
    speech_part_definitions = None
    examples = None
    see_also = None

    def __init__(self, json_obj):
        self.translation = ''
        self.original = ''
        self.translation_translit = ''
        self.original_translit = ''

        for sentence in _list(_list_get(json_obj, 0)):
            self.translation += _str(_list_get(sentence, 0))
            self.original += _str(_list_get(sentence, 1))
            self.translation_translit += _str(_list_get(sentence, 2))
            self.original_translit += _str(_list_get(sentence, 3))

        self.speech_part_variants = [SpeechPartSpecificVariants(obj) for obj
                                     in _list(_list_get(json_obj, 1))]

        self.source_lang = _list_get(json_obj, 2)

        self.segments = [SegmentTranslation(obj) for obj
                         in _list(_list_get(json_obj, 5))]

        self.correction = Correction(_list_get(json_obj, 7))

        self.lang_suggests = [LanguageSuggestion(lang, weight) for lang, weight
                              in zip(_list(_list_get(json_obj, 8, 0)),
                                     _list(_list_get(json_obj, 8, 2)))]

        self.speech_part_synonyms = [SpeechPartSpecificSynonyms(obj) for obj
                                     in _list(_list_get(json_obj, 11))]

        self.speech_part_definitions = [SpeechPartSpecificDefinitions(obj)
                                        for obj in _list(
                                            _list_get(json_obj, 12))]

        self.examples = [UsageExample(obj) for obj
                         in _list(_list_get(json_obj, 13, 0))]

        self.see_also = _list(_list_get(json_obj, 14, 0))
