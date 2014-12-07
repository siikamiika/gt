#!/usr/bin/env python2
import sys
import argparse
from gt import glue

def main():
    parser = argparse.ArgumentParser(
        description='CLI Google Translate client',
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--colors', default='33:32:4;1;37:0:1;37:0', help='''\
colon-separated list of ANSI SGR attributes will be used to highlight the \
following parts of the output, respectively:
    - Program messages/notes
    - Transcription
    - Speech part names
    - Translation variants without -s/--synonyms
    - Translation variants with -s/--synonyms
    - Synonyms with -s/--synonyms

Example:
    gt_console.py --colors='3:3:4;1;37:0:1;37:0' ...''')

    parser.add_argument('-c', '--enable-colors',
                        choices=['auto', 'yes', 'no'], default='auto',
                        help='''\
controls if the program should use ANSI SGR escapes; 'auto' (default) will \
check if stdout is a tty''')

    parser.add_argument('-s', '--synonyms', action='store_true',
                        dest='synonyms',
                        help='include synonyms for each variant')

    parser.add_argument('-S', '--no-synonyms', action='store_false',
                        dest='synonyms',
                        help='don\'t include synonyms (default)')

    parser.add_argument('-t', '--transcription', action='store_true',
                        dest='transcription',
                        help='include transcription')

    parser.add_argument('-T', '--no-transcription', action='store_false',
                        dest='transcription',
                        help='don\'t include transcription (default)')

    parser.add_argument('-r', '--result-only', action='store_true',
                        dest='result_only',
                        help='don\'t show anything but a translation')

    parser.add_argument('-R', '--no-result-only', action='store_false',
                        dest='result_only',
                        help='include speech part-specific variants (default)')

    parser.add_argument('source_lang',
                        help='source language code, or \'auto\' to auto-detect')
    parser.add_argument('target_lang',
                        help='target language code')
    parser.add_argument('text',
                        help='text to translate')

    args = parser.parse_args()

    enable_colors = None
    if args.enable_colors == 'yes':
        enable_colors = True
    elif args.enable_colors == 'no':
        enable_colors = False
    elif args.enable_colors == 'auto':
        enable_colors = sys.stdout.isatty()

    def sgr_escape(attr, text):
        if enable_colors:
            return u'\033[{}m{}\033[0m'.format(attr, text)
        else:
            return text

    def uprint(value):
        print value.encode('utf-8')

    # SGR attributes: program message, transcription, speech part,
    # variant with normal format (without -s/--synonyms),
    # variant with extended format (with -s/--synonyms)
    # synonym
    [msg_attr, transcription_attr, speech_part_attr,
     n_variant_attr, s_variant_attr, synonym_attr] = args.colors.split(':')

    translation = glue.get_translation(source_lang=args.source_lang,
                                       target_lang=args.target_lang,
                                       text=args.text)
    if args.source_lang == 'auto':
        uprint(sgr_escape(msg_attr, u'Language detected: {}'.format(
            translation.source_lang)))

    uprint(translation.translation)

    if args.transcription:
        uprint(sgr_escape(transcription_attr, translation.transcription))

    if not args.result_only:
        for speech_part in translation.speech_parts:
            plural_name = speech_part.name + 's'

            if args.synonyms:
                uprint(u'\n{}'.format(sgr_escape(speech_part_attr,
                                                 plural_name)))

                for variant in speech_part.variants:
                    synonyms = [sgr_escape(synonym_attr, s)
                                for s in variant.synonyms]
                    uprint(u'  {}: {}'.format(
                        sgr_escape(s_variant_attr, variant.variant),
                        ', '.join(synonyms)))
            else:
                variants = [sgr_escape(n_variant_attr, v.variant)
                            for v in speech_part.variants]
                uprint(u'\n{}: {}'.format(
                    sgr_escape(speech_part_attr, plural_name),
                    ', '.join(variants)))

if __name__ == '__main__':
    main()
