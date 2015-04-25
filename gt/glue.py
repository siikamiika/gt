"""This module contains a function that glues the `network', `json_preproc'
and `translation' modules and the `json' module from the python standard
library."""
from gt import network, json_preproc, translation
import json

def get_translation(*args, **kwargs):
    return translation.Translation(
        json.loads(
            json_preproc.preprocess(
                network.fetch_response(*args, **kwargs))))
