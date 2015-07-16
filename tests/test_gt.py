import unittest

try:
    import gt
except ImportError: # hack for pylint
    from .. import gt # pylint: disable=import-self

class MaxWeight(unittest.TestCase):
    translation = None

    @classmethod
    def setUpClass(cls):
        cls.translation = gt.get_translation(
            'en', 'ru', 'jar',
            include_variants=True)

    def test_max_weight(self):
        self.assertNotEqual(
            self.translation.variant_groups[0].max_weight, 0)

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

    def test_variant_groups(self):
        self.assertNotEqual(
            self.translation.variant_groups,
            [])
        for group in self.translation.variant_groups:
            self.assertIsNotNone(group.speech_part)
            self.assertNotEqual(group.variants, [])
            for variant in group.variants:
                self.assertIsNotNone(variant.translation)
                self.assertNotEqual(variant.synonyms, [])

    def test_interface_language(self):
        speech_part_names = [g.speech_part
                             for g in self.translation.variant_groups]
        self.assertIn('имя существительное', speech_part_names)
        self.assertIn('глагол', speech_part_names)
