#!/usr/bin/env python3
import notify2
import subprocess
import argparse
from cgi import escape as html_escape
from gt import glue

class SeeAlso:
    NO = -1
    YES = -2

    def __init__(self, arg):
        if arg == 'no':
            self.value = SeeAlso.NO
        elif arg == 'yes':
            self.value = SeeAlso.YES
        else:
            self.value = int(arg)
            if self.value < 0:
                raise ValueError('--see-also argument is negative')

    def __bool__(self):
        return self.value != SeeAlso.NO

    def slice_off(self, see_also):
        if self.value == SeeAlso.NO:
            return []
        elif self.value == SeeAlso.YES:
            return see_also
        else:
            return see_also[:self.value]

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
    parser.add_argument('-a', '--see-also', metavar='{no,yes,<number>}',
                        type=SeeAlso, default='no', help='''\
map the "see also" list to notification actions.
    "no": do not map;
    "yes": map all;
    <number>: map first <number> entries only.''')

    parser.add_argument('source_lang',
                        help='source language code, or \'auto\' to auto-detect')
    parser.add_argument('target_lang',
                        help='target language code')

    args = parser.parse_args()

    selection = subprocess.check_output(['xsel', '-o', '--' + args.selection],
                                        universal_newlines=True)

    messing_with_mainloop = bool(args.see_also)

    params_stack = [(args.source_lang, args.target_lang, selection)]

    notify2.init('gt_notify',
                 mainloop='glib' if messing_with_mainloop else None)

    def get_translation(source_lang, target_lang, text):
        return glue.get_translation(
            source_lang=source_lang, target_lang=target_lang, text=text,
            include_translit=args.translit, include_variants=True,
            include_segments=False, include_examples=False,
            include_definitions=False, include_see_also=bool(args.see_also),
            include_synonyms=False, suggest_language=True,
            correct_typos=False, interface_lang=None)

    def show_notification(source_lang, target_lang, text):
        translation = get_translation(source_lang, target_lang, text)

        notification = notify2.Notification(summary=None)
        notification.timeout = args.timeout or notify2.EXPIRES_NEVER

        summary = ''
        if args.source_lang == 'auto':
            summary += '(Language detected: {})'.format(
                html_escape(translation.source_lang))

        if translation.speech_part_variants:
            message = '<b>{}</b>'.format(html_escape(translation.translation))
        else:
            message = html_escape(translation.translation)

        if translation.translation_translit:
            message += '\n<i>{}</i>'.format(html_escape(
                translation.translation_translit))

        for speech_part_variant in translation.speech_part_variants:
            variants = [v.translation for v in speech_part_variant.variants]
            message += '\n\n<u>{}s</u>: {}'.format(
                html_escape(speech_part_variant.speech_part),
                html_escape(', '.join(variants)))

        if args.see_also:
            see_also = args.see_also.slice_off(translation.see_also)

            def callback(_notification, action):
                notification.close()

                command, arg = action.split('_', 1)
                if command == 'sa':
                    index = int(arg)
                    new_params = (source_lang, target_lang, see_also[index])
                    params_stack.append(new_params)

            for index, word in enumerate(see_also):
                notification.add_action('sa_{}'.format(index), word, callback)

        notification.update(summary, message)
        notification.show()

        if messing_with_mainloop:
            from gi.repository import GLib
            main_loop = GLib.MainLoop()
            notification.connect('closed', lambda reason: main_loop.quit())
            main_loop.run()

    for source_lang, target_lang, text in params_stack:
        show_notification(source_lang, target_lang, text)

if __name__ == '__main__':
    main()