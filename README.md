# Description

This is…

* A library that parses Google Translate response intended for evaluation as JavaScript;

* A command-line interface (`gt_console.py`) with features including colors and pronouncing the translation;

* A xsel+libnotify interface (`gt_notify.py`) that translates a content of X selection and and then shows a notification with html-formatted translation;

* A `say.py` tool to pronounce a text using Google Translate speech synthesizer;

* A simple debug tool (`dump_as_json.py`) that dumps Google Translate response as well-formatted JSON.

The `languages.sh` script can be used for fetching the abbreviation/language list.

# Screenshots

## Command-line interface
![Screenshot](https://cloud.githubusercontent.com/assets/5462697/5102897/4d3d8a12-6fe2-11e4-9380-2cc81d795188.png)

![Screenshot](https://cloud.githubusercontent.com/assets/5462697/5102877/ec07fb92-6fe1-11e4-9916-9784c97c7615.png)

![Screenshot](https://cloud.githubusercontent.com/assets/5462697/5102880/efb1483e-6fe1-11e4-9a33-cecbc33da590.png)

## xsel+libnotify interface
![Screenshot](https://cloud.githubusercontent.com/assets/5462697/5102702/8ae4583a-6fdf-11e4-91ed-259bf8f5a051.png)

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

- Support for more Google Translate features such as definitions, examples, "see also"…

- Add tests
