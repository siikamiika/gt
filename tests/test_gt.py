import unittest
import gt

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

class Correction(unittest.TestCase):
    translation = None

    @classmethod
    def setUpClass(cls):
        cls.translation = gt.get_translation('en', 'ru', 'ehllo',
                                             correct_typos=True)

    def test_correction(self):
        self.assertEqual(self.translation.correction.corrected_text.lower(),
                         'hello')
        self.assertEqual(self.translation.correction.corrected_html.lower(),
                         '<b><i>hello</i></b>')

class LanguageSuggestions(unittest.TestCase):
    translation = None

    @classmethod
    def setUpClass(cls):
        cls.translation = gt.get_translation('ja', 'de', 'тест',
                                             suggest_language=True)

    def test_lang_suggests(self):
        suggests = [s.language for s in self.translation.lang_suggests]
        self.assertIn('ru', suggests)

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
            self.translation.translation_translit.lower(),
            'zdravstvuyte')

    def test_original_translit(self):
        self.assertEqual(
            self.translation.original_translit,
            'heˈlō,həˈlō')

    def test_source_lang(self):
        self.assertEqual(
            self.translation.source_lang,
            'en')

    def test_segments(self):
        self.assertEqual(len(self.translation.segments), 1)
        self.assertEqual(self.translation.segments[0].original_segment.lower(),
                         'hello')
        self.assertNotEqual(self.translation.segments[0].translations, [])

    def test_synonym_groups(self):
        self.assertNotEqual(self.translation.synonym_groups, [])
        for group in self.translation.synonym_groups:
            self.assertIsNotNone(group.speech_part)
            self.assertNotEqual(group.synonyms, [])
            self.assertIsNotNone(group.dict_entry)

    def test_definition_groups(self):
        self.assertNotEqual(self.translation.definition_groups, [])
        for group in self.translation.definition_groups:
            self.assertIsNotNone(group.speech_part)
            self.assertNotEqual(group.definitions, [])
            for definition in group.definitions:
                self.assertIsNotNone(definition.definition)
                self.assertIsNotNone(definition.dict_entry)
                # This is true only if include_examples=True was passed
                self.assertIsNotNone(definition.example)

    def test_examples(self):
        self.assertNotEqual(self.translation.examples, [])
        for example in self.translation.examples:
            self.assertIsNotNone(example.example_html)
            self.assertIsNotNone(example.dict_entry)

    def test_see_also(self):
        self.assertNotEqual(self.translation.see_also, [])
        self.assertIn('Hello!', self.translation.see_also)

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
