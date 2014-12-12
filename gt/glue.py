"""This module contains the only function that glues `network', `json_preproc'
and `translation' modules and `json' module from the python standard library.
"""
from gt import network, json_preproc, translation
import json

def get_translation(*args, **kwargs):
    return translation.Translation(
        json.loads(
            json_preproc.preprocess(
                network.fetch_response(*args, **kwargs))))
