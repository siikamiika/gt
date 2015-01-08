#!/usr/bin/env python2
import argparse
import json
from gt import network, json_preproc

def main():
    parser = argparse.ArgumentParser(
        description='Tool for dumping Google Translate response as a '
                    'well-formatted JSON')

    parser.add_argument('source_lang',
                        help='source language code, or \'auto\' to auto-detect')
    parser.add_argument('target_lang',
                        help='target language code')
    parser.add_argument('text',
                        help='text to translate')

    args = parser.parse_args()

    semijson = network.fetch_response(
        args.source_lang, args.target_lang, args.text,
        include_translit=True, include_variants=True, include_segments=True,
        include_examples=True, include_definitions=True, include_see_also=True,
        include_synonyms=True, suggest_language=True, correct_typos=True)
    unpretty_json = json_preproc.preprocess(semijson)
    pretty_json = json.dumps(
        json.loads(unpretty_json), ensure_ascii=False, indent=2)
    print pretty_json.encode('utf-8')

if __name__ == '__main__':
    main()
