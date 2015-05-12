from gt import translation, json_preproc, network
import json

def get_translation(*args, **kwargs):
    return translation.Translation(
        json.loads(
            json_preproc.preprocess(
                network.fetch_response(*args, **kwargs))))
