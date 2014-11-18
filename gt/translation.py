"""This module contains translation data structures and the `from_json' function
that parses a python representation of a JavaScript sent by Google Translate
as a response into a Translation object.

To get some idea about a structure of a response, run

    ./dump_as_json.py en ru get

    ./dump_as_json.py en ru 'London is the capital of Great Britain'

This will print out Google Translate response as well-formatted JSON.
"""
from collections import namedtuple

SegmentTranslation = namedtuple('SegmentTranslation',
                                ['source', 'variants'])

SpeechPartSpecificVariant = namedtuple('SpeechPartSpecificVariant',
                                       ['variant', 'weight', 'synonyms'])

SpeechPart = namedtuple('SpeechPart',
                        ['name', 'variants'])

Translation = namedtuple('Translation',
                         ['translation', 'source', 'transcription',
                          'source_lang', 'speech_parts', 'segments'])
def from_json(json):

    def segment_from_json(segment_json):
        return SegmentTranslation(
            source=segment_json[0],
            variants=map(lambda x: x[0], segment_json[2] or []))

    def speech_part_from_json(speech_part_json):

        def variant_from_json(variant_json):
            variant, synonyms = variant_json[:2]
            weight = variant_json[3] if len(variant_json) >= 4 else None
            return SpeechPartSpecificVariant(variant=variant, weight=weight,
                                             synonyms=synonyms)

        return SpeechPart(name=speech_part_json[0],
                          variants=map(variant_from_json, speech_part_json[2]))

    return Translation(translation=' '.join(map(lambda x: x[0].strip(),
                                                json[0])),
                       source=json[0][0][1],
                       transcription=json[0][0][2],
                       source_lang=json[2],
                       speech_parts=map(speech_part_from_json, json[1] or []),
                       segments=map(segment_from_json, json[5] or []))
