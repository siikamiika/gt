# What´s that?

* A library that parses Google Translate response intended for evaluation as JavaScript. Its features include:

    * Transliteration of original (IPA) and translated (latin symbols) texts

    * Word translation variants by part of speech, translation variants of text segments

    * Examples, definitions, synonyms, “see also” list

    * Original language and typo correction

* A nice command-line interface (`gt_console.py`) makes use of all library features;

* A xsel+libnotify interface (`gt_notify.py`) that translates the content of X selection and shows a notification with html-formatted translation;

* A simple debug tool (`dump_as_json.py`) that dumps Google Translate response as well-formatted JSON.

The `languages.sh` script can be used for fetching the abbreviation/language list.

# Screenshots

### Command-line interface

![1](https://cloud.githubusercontent.com/assets/5462697/5557491/3427f084-8d11-11e4-8dc1-03401ad9fd89.png)

![2](https://cloud.githubusercontent.com/assets/5462697/5557493/44c76942-8d11-11e4-8bca-fbd550c1a2f4.png)

![3](https://cloud.githubusercontent.com/assets/5462697/5557495/63c2587a-8d11-11e4-88fe-76b21c3f3a10.png)

### xsel+libnotify interface
![1](https://cloud.githubusercontent.com/assets/5462697/5102702/8ae4583a-6fdf-11e4-91ed-259bf8f5a051.png)

# Usage tips

## Command-line interface

Set up an alias for `gt_console.py` (your shell .rc file, bash syntax used):
```bash
alias gt='/path/to/gt_console.py'
```

You can supply custom colors and a set of default options (can be overrided later by passing the opposite option):
```bash
alias gt='/path/to/gt_console.py --colors="3:3:4;1;37:0:1;37:0" -s'
```

You can also add more fast-to-type aliases:
```bash
alias enru='gt en ru'
alias ruen='gt ru en'
```

## xsel+libnotify interface

 * Make sure you have installed `xsel` binary and `notify2` python2 library.

Set up a keybind for `/path/to/gt_notify.py <soruce_lang> <target_lang>`. This usually can be done in your DE/WM settings.

* You can specify `auto` as a source language code to enable auto-detection (this applies to `gt_console.py` as well);

* Check out [an example of language guesser script](https://github.com/shdown/gt/wiki/Language-guesser-script) for two languages use different char sets.

# TODO

- Document everything

- Add tests
