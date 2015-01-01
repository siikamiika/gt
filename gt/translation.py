"""This module contains data structures that reflect Google Translate
response."""

def _list_get(obj, *indices):
    """Safely obtains an object from nested lists. Returns None in case of
    an error -- that is, when if, on some step, an object fetched is not a list
    or the next index is invalid."""
    for index in indices:
        if type(obj) is not list:
            return None
        if index >= len(obj):
            return None
        obj = obj[index]
    return obj

def _list(obj):
    """Returns the original object if it is a list, or an empty list."""
    return obj if type(obj) is list else []

def _unicode(obj):
    """Returns the original object if it is an unicode object, or an empty
    unicode string."""
    return obj if type(obj) is unicode else u''

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

    def __init__(self, json_obj):
        self.speech_part = _list_get(json_obj, 0)
        self.variants = map(self.SpeechPartSpecificVariant,
                            _list(_list_get(json_obj, 2)))

class SegmentTranslation:
    original_segment = None
    translations = None

    def __init__(self, json_obj):
        self.original_segment = _list_get(json_obj, 0)
        self.translations = map(lambda obj: _list_get(obj, 0),
                                _list(_list_get(json_obj, 2)))

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
        self.definitions = map(self.SpeechPartSpecificDefinition,
                               _list(_list_get(json_obj, 1)))

class UsageExample:
    example_html = None
    dict_entry = None

    def __init__(self, json_obj):
        self.example_html = _list_get(json_obj, 0)
        self.dict_entry = _list_get(json_obj, 5)

class Correction:
    corrected_text = None
    corrected_html = None

    def __init__(self, json_obj):
        self.corrected_html = _list_get(json_obj, 0)
        self.corrected_text = _list_get(json_obj, 1)

class Translation:
    translation = None
    original = None
    translation_translit = None
    original_ipa = None
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
        self.original_ipa = ''

        for sentence in _list(_list_get(json_obj, 0)):
            if type(sentence) is not list:
                continue
            if len(sentence) == 2:
                self.translation += _unicode(sentence[0])
                self.original += _unicode(sentence[1])
            elif len(sentence) == 4:
                self.original_ipa += _unicode(sentence[0])
                self.translation_translit += _unicode(sentence[2])

        self.speech_part_variants = map(SpeechPartSpecificVariants,
                                        _list(_list_get(json_obj, 1)))
        self.source_lang = _list_get(json_obj, 2)
        self.segments = map(SegmentTranslation, _list(_list_get(json_obj, 5)))
        self.correction = Correction(_list_get(json_obj, 7))

        self.lang_suggests = [LanguageSuggestion(lang, weight) for lang, weight
                              in zip(_list(_list_get(json_obj, 8, 0)),
                                     _list(_list_get(json_obj, 8, 2)))]

        self.speech_part_synonyms = map(SpeechPartSpecificSynonyms,
                                        _list(_list_get(json_obj, 11)))
        self.speech_part_definitions = map(SpeechPartSpecificDefinitions,
                                           _list(_list_get(json_obj, 12)))
        self.examples = map(UsageExample, _list(_list_get(json_obj, 13, 0)))
        self.see_also = _list(_list_get(json_obj, 14, 0))
