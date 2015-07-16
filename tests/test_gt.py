import unittest

try:
    import gt
except ImportError: # hack for pylint
    from .. import gt # pylint: disable=import-self

class FiveElementsPerSentence(unittest.TestCase):
    translation = None

    @classmethod
    def setUpClass(cls):
        cls.translation = gt.get_translation(
            'ru', 'en', 'одновременный')

    def test_translation(self):
        self.assertEqual(
            self.translation.translation.lower(),
            'simultaneous')

class SingleWordTranslation(unittest.TestCase):
    translation = None

    @classmethod
    def setUpClass(cls):
        cls.translation = gt.get_translation(
            'en', 'ru', 'hello',
            include_translit=True, include_variants=True,
            include_segments=True, include_examples=True,
            include_definitions=True, include_see_also=True,
            include_synonyms=True, suggest_language=True,
            correct_typos=True, interface_lang='ru')

    def test_original(self):
        self.assertEqual(
            self.translation.original,
            'hello')

    def test_translation(self):
        self.assertEqual(
            self.translation.translation.lower(),
            'здравствуйте')

    def test_translation_translit(self):
        self.assertEqual(
            self.translation.translation_translit,
            'zdravstvuyte')

    def test_original_translit(self):
        self.assertEqual(
            self.translation.original_translit,
            'heˈlō,həˈlō')

    def test_source_lang(self):
        self.assertEqual(
            self.translation.source_lang,
            'en')
