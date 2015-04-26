#!/usr/bin/env python3
import os
import sys
import argparse
from gt import glue

def parse_colors(colors):
    return dict(kv.split('=', 1) for kv in colors.split(':') if '=' in kv)

DEFAULT_COLORS = 'no=1;33:tr=32:sp=1;34:tv=1;31:os=:he=1;32:ex=33:bo=1;4'

def main():
    parser = argparse.ArgumentParser(
        description='''CLI Google Translate client

environment variables:

    GT_COLORS
        overrides the default colors and other attributes used to highlight
        various parts of the output. Its value is a colon-separated list of
        part=attributes pairs that defaults to
            ''' + DEFAULT_COLORS + '''

        The following parts of output are supported:
            no  notice
            tr  translit
            sp  speech part name
            tv  speech part-specific translation variant
            os  synonym in original language
            he  header
            ex  usage example in the context of the definition
            bo  "bold" text used to highlight the word in the example
''',
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-t', '--translit',
                        action='store_true',
                        help='show translation transliteration')

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument('-r', '--result-only',
                           action='store_true',
                           help='do not show translation variants of a given '
                                'word')

    verbosity.add_argument('-x', '--extended',
                           action='store_true',
                           help='show synonyms in source language for each '
                                'translation variant')

    parser.add_argument('-e', '--examples',
                        action='store_true',
                        help='show usage examples of a given word')

    parser.add_argument('-d', '--definitions',
                        action='store_true',
                        help='show definition(s) of a given word')

    parser.add_argument('-a', '--see-also',
                        action='store_true',
                        help='show the "see also" list for a given word')

    parser.add_argument('-s', '--synonyms',
                        action='store_true',
                        help='show synonym list for a given word')

    parser.add_argument('-c', '--correct',
                        action='store_true',
                        help='auto-correct the original text')

    parser.add_argument('-l', '--suggest-lang',
                        action='store_true',
                        help='suggect the original language(s)')

    parser.add_argument('source_lang',
                        help='source language code, or \'auto\' to auto-detect')
    parser.add_argument('target_lang',
                        help='target language code')
    parser.add_argument('text',
                        help='text to translate')

    args = parser.parse_args()

    ansi_capable = sys.stdout.isatty() and \
                   os.getenv('TERM') not in [None, 'dumb']

    colors = parse_colors(DEFAULT_COLORS)
    colors.update(parse_colors(os.getenv('GT_COLORS', '')))

    def colorize(color, text):
        if ansi_capable and color in colors:
            return '\033[{}m{}\033[0m'.format(colors[color], text)
        return text

    def get_translation(source_lang, target_lang, text):
        return glue.get_translation(
            source_lang, target_lang, text,
            include_translit=args.translit,
            include_variants=not args.result_only,
            include_segments=False,
            include_examples=args.examples,
            include_definitions=args.definitions,
            include_see_also=args.see_also,
            include_synonyms=args.synonyms,
            suggest_language=args.suggest_lang,
            correct_typos=args.correct,
            interface_lang=None)

    translation = get_translation(args.source_lang, args.target_lang, args.text)

    if translation.correction.corrected_text:
        if translation.correction.corrected_html:
            typos_n = translation.correction.corrected_html.count('<b><i>')
            print(colorize('no', 'Typo(s) corrected: {}'.format(typos_n)))
        else:
            print(colorize('no', 'Text was corrected'))

        translation = get_translation(args.source_lang, args.target_lang,
                                      translation.correction.corrected_text)

    if args.source_lang == 'auto':
        print(colorize('no', 'Language detected: {}'.format(
            translation.source_lang)))

    if args.suggest_lang:
        lang_suggests = list(map(lambda s: s.language, translation.lang_suggests))
        if not lang_suggests:
            print(colorize('no', 'No languages were suggested'))
        elif lang_suggests != [translation.source_lang]:
            print(colorize('no', 'Language(s) suggested: {}'.format(
                ', '.join(lang_suggests))))

    print(translation.translation)

    if translation.translation_translit:
        print(colorize('tr', format(translation.translation_translit)))

    if translation.speech_part_variants:
        for speech_part_variants in translation.speech_part_variants:
            if args.extended:
                print(' {}:'.format(colorize(
                    'sp', speech_part_variants.speech_part)))

                for varaint in speech_part_variants.variants:
                    print('  {}: {}'.format(
                        colorize('tv', varaint.translation),
                        colorize('os', ', '.join(varaint.synonyms))))
            else:
                variants = (v.translation for v
                            in speech_part_variants.variants)
                print(' {}: {}'.format(
                    colorize('sp', speech_part_variants.speech_part),
                    colorize('tv', ', '.join(variants))))

    if translation.examples:
        print('\n{}:'.format(colorize('he', 'Examples')))
        for ex in translation.examples:
            if ansi_capable and 'bo' in colors:
                bold_start, bold_end = '\033[{}m'.format(colors['bo']), \
                                       '\033[0m'
            else:
                bold_start, bold_end = '', ''
            example = ex.example_html \
                .replace('<b>', bold_start) \
                .replace('</b>', bold_end)
            print(' {}'.format(example))

    if translation.speech_part_definitions:
        print('\n{}:'.format(colorize('he', 'Definitions')))
        for speech_part_def in translation.speech_part_definitions:
            print(' {}:'.format(colorize('sp', speech_part_def.speech_part)))
            for definition in speech_part_def.definitions:
                if definition.example:
                    print('  {} -- {}'.format(
                        definition.definition,
                        colorize('ex', definition.example)))
                else:
                    print('  {}'.format(definition.definition))

    if translation.speech_part_synonyms:
        print('\n{}:'.format(colorize('he', 'Synonyms')))
        for synonyms in translation.speech_part_synonyms:
            print(' {}: {}'.format(colorize('sp', synonyms.speech_part),
                                   ', '.join(synonyms.synonyms)))

    if translation.see_also:
        print('\n{}:'.format(colorize('he', 'See also')))
        print(' {}'.format(', '.join(translation.see_also)))

if __name__ == '__main__':
    main()