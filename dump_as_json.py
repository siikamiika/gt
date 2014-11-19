#!/usr/bin/env python2
import sys
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
    parser.add_argument('text')

    args = parser.parse_args()

    unpretty_json = json_preproc.preprocess(
        network.fetch_response(args.source_lang, args.target_lang, args.text))
    pretty_json = json.dumps(
        json.loads(unpretty_json), sys.stdout, ensure_ascii=False, indent=2)
    print pretty_json.encode('utf-8')

if __name__ == '__main__':
    main()
