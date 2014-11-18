#!/bin/sh
# USAGE: languages.sh [DOMAIN]
#
# Dumps Google Translate language list. You can specify a custom domain to
# change the language of language names.
#
# Default DOMAIN is 'com' (English language).

useragent='Mozilla/5.0'
url=http://translate.google."${1:-com}"

if hash wget 2>/dev/null; then
    wget -O- -U"$useragent" "$url"
else
    curl -A"$useragent" "$url"
fi \
    | grep -o '<option value=[^ >]*>[^<]*</option>' \
    | sed -r 's;^<option value=([^ >]*)>([^<]*)</option>$;\1 \2;' \
    | sort -t' ' -k1,1 -u
