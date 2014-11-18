"""This module contains the only function that glues `network', `json_preproc'
and `translation' modules and `json' module from the python standard library.
"""
from gt import network, json_preproc, translation
import json

def get_translation(source_lang, target_lang, text):
    return translation.from_json(
        json.loads(
            json_preproc.preprocess(
                network.fetch(source_lang, target_lang, text))))
