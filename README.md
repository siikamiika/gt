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

Simple usage:

![alt](https://cloud.githubusercontent.com/assets/5462697/7939935/6a51aee0-0956-11e5-831f-d55745c37cf5.png)

If no text given, the program starts in interactive mode:

![alt](https://cloud.githubusercontent.com/assets/5462697/7939983/a5a314a2-0956-11e5-91d5-76ae38fb8119.png)

`--correct`. Note that additional text arguments are joined by space, so you don’t need to quote phrases:

![alt](https://cloud.githubusercontent.com/assets/5462697/8271850/ffd445c6-1834-11e5-9261-b49a612fb86b.png)

Bells and whistles:

![alt](https://cloud.githubusercontent.com/assets/5462697/7940006/cfc4d7d4-0956-11e5-9728-2bba2aa4ecba.png)

`--segments`:

![alt](https://cloud.githubusercontent.com/assets/5462697/8569162/3929eeca-257d-11e5-86da-f5a1cb58e969.png)

Transliteration (`-tTr` is for `--translit --source-translit --result-only`):

![alt](https://cloud.githubusercontent.com/assets/5462697/7939943/76d44092-0956-11e5-8b0a-7d19d4f78317.png)

Language detection:

![alt](https://cloud.githubusercontent.com/assets/5462697/7940291/a106e4da-0958-11e5-893d-16a41184227e.png)

Custom interface language:

![alt](https://cloud.githubusercontent.com/assets/5462697/7939975/9bcb580e-0956-11e5-949f-05c5af1b6bb9.png)

### xsel+libnotify interface

(with a keybind set up)

![1](https://cloud.githubusercontent.com/assets/5462697/5102702/8ae4583a-6fdf-11e4-91ed-259bf8f5a051.png)
