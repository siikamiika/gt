#!/usr/bin/env python2
import os
import subprocess
import argparse
from gt import network

def say(lang, text, player=None):
    opts = (player or
            os.getenv('GT_PLAYER') or
            os.getenv('PLAYER') or
            'mplayer').split()
    opts.append(network.get_speech_url(lang, text))
    subprocess.check_call(opts)

def main():
    parser = argparse.ArgumentParser(
        description='Pronounces text using Google Translate speech synthesizer',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-p', '--player', dest='player', default=None, help='''\
choose a player.
If not specified or empty, GT_PLAYER environment variable is used;
if unset or empty, PLAYER environment variable is used;
if unset or empty too, 'mplayer' is used.''')

    parser.add_argument('lang',
                        help='language code')
    parser.add_argument('text',
                        help='text to say')
    args = parser.parse_args()

    say(args.lang, args.text, player=args.player)

if __name__ == '__main__':
    main()
