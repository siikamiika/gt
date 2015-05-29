# What’s that?

* A library that parses Google Translate response intended for evaluation as JavaScript. Its features include:

    * Transcription/transliteration

    * Word translation variants by part of speech, translation variants of text segments

    * Usage examples, definitions, synonyms, “see also” list

    * Language detection and original language suggestion

    * Typo correction

* A nice command-line interface (`gt_console`) with interactive shell mode support;

* An xsel+libnotify interface (`gt_notify`) that translates the content of X selection and then shows a notification with translation;

* A simple debug tool (`gt_dump_json`) that dumps Google Translate response as well-formatted JSON.

The `languages` script can be used for fetching the abbreviation/language list (or you can just see [the table](https://github.com/shdown/gt/wiki/Abbreviation%E2%86%92language-correspondence-table)).

The `gt_play` script can be used for playing back/downloading voice using Google Translate voice synthesizer.

# Screenshots

### Command-line interface

(with `alias gt=gt_console`)

![1](https://cloud.githubusercontent.com/assets/5462697/5557491/3427f084-8d11-11e4-8dc1-03401ad9fd89.png)

![2](https://cloud.githubusercontent.com/assets/5462697/5557493/44c76942-8d11-11e4-8bca-fbd550c1a2f4.png)

![3](https://cloud.githubusercontent.com/assets/5462697/5557495/63c2587a-8d11-11e4-88fe-76b21c3f3a10.png)

### xsel+libnotify interface

(with a keybind set up)

![1](https://cloud.githubusercontent.com/assets/5462697/5102702/8ae4583a-6fdf-11e4-91ed-259bf8f5a051.png)
