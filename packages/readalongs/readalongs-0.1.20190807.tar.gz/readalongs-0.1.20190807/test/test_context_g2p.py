from unittest import TestCase
import unittest
from readalongs.log import LOGGER

from readalongs.g2p.context_g2p import ContextG2P
from readalongs.g2p.convert_orthography import ConverterLibrary
from lxml import etree


class TestContextG2P(TestCase):
    def setUp(self):
        self.converter = ConverterLibrary()
        self.test_conversion_data = [
            {'in_lang': 'git',
             'out_lang': 'eng-arpabet',
             'in_text': "K̲'ay",
             'out_text': 'K HH AE Y'},
            {'in_lang': 'git',
             'out_lang': 'eng-arpabet',
             'in_text': "guts'uusgi'y",
             'out_text': 'G UW T S HH UW S G IY HH Y'}
        ]

    def test_conversions(self):
        for test in self.test_conversion_data:
            conversion = self.converter.convert(
                test['in_text'], test['in_lang'], test['out_lang'])
            self.assertEqual(conversion[0], test['out_text'])

    def test_reduced_indices(self):
        conversion = self.converter.convert("K̲'ay", "git", "eng-arpabet")
        self.assertEqual(conversion[1].reduced(), [
                         (2, 1), (3, 4), (4, 7), (5, 9)])


if __name__ == '__main__':
    LOGGER.setLevel('DEBUG')
    unittest.main()
