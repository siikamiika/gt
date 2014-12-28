#!/usr/bin/env python2
import notify2
import subprocess
import argparse
from cgi import escape as html_escape
from gt import glue

def main():
    parser = argparse.ArgumentParser(
        description='xsel/libnotify Google Translate client',
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-S', '--selection',
                        choices=['primary', 'secondary', 'clipboard'],
                        default='primary',
                        help='specify a selection buffer to read from')

    parser.add_argument('-T', '--timeout', type=float, default=0,
                        help='notification timeout or 0 (default) to show '
                             'forever')

    parser.add_argument('-t', '--translit', action='store_true',
                        help='include translation transliteration')

    parser.add_argument('source_lang',
                        help='source language code, or \'auto\' to auto-detect')
    parser.add_argument('target_lang',
                        help='target language code')

    args = parser.parse_args()

    selection = subprocess.check_output(['xsel', '-o', '--' + args.selection],
                                        universal_newlines=True)

    notify2.init('gt_notify')

    def get_translation(source_lang, target_lang, text):
        return glue.get_translation(
            source_lang=source_lang, target_lang=target_lang, text=text,
            include_translit=args.translit, include_variants=True,
            include_segments=False, include_examples=False,
            include_definitions=False, include_see_also=False,
            include_synonyms=False, suggest_language=True,
            correct_typos=False, interface_lang=None)

    translation = get_translation(args.source_lang, args.target_lang, selection)

    notification = notify2.Notification(summary=None)
    notification.timeout = args.timeout or notify2.EXPIRES_NEVER

    summary = ''
    if args.source_lang == 'auto':
        summary += u'(Language detected: {})'.format(
            html_escape(translation.source_lang))

    if translation.speech_part_variants:
        message = u'<b>{}</b>'.format(html_escape(translation.translation))
    else:
        message = html_escape(translation.translation)

    if translation.translation_translit:
        message += u'\n<i>{}</i>'.format(html_escape(
            translation.translation_translit))

    for speech_part_variant in translation.speech_part_variants:
        variants = [v.translation for v in speech_part_variant.variants]
        message += u'\n\n<u>{}s</u>: {}'.format(
            html_escape(speech_part_variant.speech_part),
            html_escape(', '.join(variants)))

    notification.update(summary, message)
    notification.show()

if __name__ == '__main__':
    main()
