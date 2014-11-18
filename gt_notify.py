#!/usr/bin/env python2
import notify2
import subprocess
import argparse
import atexit
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

    notify2.init('gt_notify')
    notification = notify2.Notification(summary=u'(Translating...)')
    notification.set_timeout(args.timeout or notify2.EXPIRES_NEVER)
    notification.show()

    translation_done = False

    def exit_hook():
        if translation_done:
            return
        notification.update('An error occurred during translation',
                            'Please re-run gt_notify from terminal in '
                            'order to identify the problem')
        notification.set_timeout(notify2.EXPIRES_NEVER)
        notification.set_urgency(notify2.URGENCY_CRITICAL)
        notification.show()

    atexit.register(exit_hook)

    translation = glue.get_translation(source_lang=args.source_lang,
                                       target_lang=args.target_lang,
                                       text=text)

    summary = ''
    if args.source_lang == 'auto':
        summary += u'(Language detected: {})'.format(
            html_escape(translation.source_lang))

    message = html_escape(translation.translation)

    for speech_part in translation.speech_parts:
        variants = [v.variant for v in speech_part.variants]
        message += u'\n\n<u>{}s</u>: {}'.format(
            html_escape(speech_part.name),
            html_escape(', '.join(variants)))

    translation_done = True
    notification.update(summary, message)
    notification.show()

if __name__ == '__main__':
    main()
