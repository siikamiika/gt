#!/usr/bin/env python2
import notify2
import subprocess
import argparse
from cgi import escape as html_escape
from gt import glue

def main():
    parser = argparse.ArgumentParser(
        description='xsel/libnotify Google Translate client')
    parser.add_argument('-s', '--selection',
                        choices=['primary', 'secondary', 'clipboard'],
                        default='primary',
                        help='specify a selection buffer to read from')
    parser.add_argument('-t', '--timeout', type=float, default=0,
                        help='notification timeout or 0 (default) to show '
                             'forever')

    parser.add_argument('source_lang',
                        help='source language code, or \'auto\' to auto-detect')
    parser.add_argument('target_lang',
                        help='target language code')

    args = parser.parse_args()

    text = subprocess.check_output(['xsel', '--output', '--' + args.selection],
                                   universal_newlines=True)

    translation = glue.get_translation(source_lang=args.source_lang,
                                       target_lang=args.target_lang,
                                       text=text)

    summary = ''
    if args.source_lang == 'auto':
        summary += u'(Language detected: {})'.format(
            html_escape(translation.source_lang))

    if translation.speech_parts:
        message = u'<b>{}</b>'.format(translation.translation)
    else:
        message = html_escape(translation.translation)

    for speech_part in translation.speech_parts:
        variants = [v.variant for v in speech_part.variants]
        message += u'\n\n<u>{}s</u>: {}'.format(
            html_escape(speech_part.name),
            html_escape(', '.join(variants)))

    notify2.init('gt_notify')

    notification = notify2.Notification(summary=summary, message=message)
    notification.timeout = args.timeout or notify2.EXPIRES_NEVER

    notification.show()

if __name__ == '__main__':
    main()
