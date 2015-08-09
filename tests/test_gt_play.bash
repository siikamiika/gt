#!/usr/bin/env bash

./gt_play -d en_US hello || exit "$?"
if ! [[ -f hello.mp3 ]]; then
    echo >&2 "E: 'hello.mp3' does not exist."
    exit 1
fi
rm -v hello.mp3 || exit "$?"
