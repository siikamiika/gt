#!/usr/bin/env bash

./gt_play -d en_US hello || exit "$?"
if ! [[ -f hello.mp3 ]]; then
    echo >&2 "E: 'hello.mp3' does not exist."
    exit 1
fi
if ! file hello.mp3 | grep -q 'MPEG .* layer III'; then
    echo >&2 "E: 'file' does not identify 'hello.mp3' as MP3 file."
    exit 1
fi
rm -v hello.mp3 || exit "$?"
