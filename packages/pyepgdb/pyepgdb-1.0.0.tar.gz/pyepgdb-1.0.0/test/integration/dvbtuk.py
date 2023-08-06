import time
from unittest import TestCase

import pyepgdb
from pyepgdb.network import dvbtuk

from .testutil import get_resource_path


class Dvbtuk (TestCase):
    def setUp (self):
        with open(get_resource_path('single-result.epgdb'), 'rb') as f:
            self.results = list(dvbtuk.parse(pyepgdb.parse(f)))

    def test_count (self):
        self.assertEqual(len(self.results), 1, 'should be 1 result')

    def test_id (self):
        self.assertEqual(self.results[0].id_, 'crid://bds.tv/E0L97G')

    def test_genre (self):
        self.assertEqual(self.results[0].genre, dvbtuk.Genre.NEWS)

    def test_title (self):
        self.assertEqual(self.results[0].title, 'Planet Earth')

    def test_subtitle (self):
        self.assertEqual(self.results[0].subtitle, '''\
Ice Worlds: David Attenborough's awe-inspiring natural history series visits \
the frozen worlds of the Arctic and Antarctic. See polar bears negotiate the \
retreat of the ice. [S,AD]\
''')

    def test_start (self):
        self.assertEqual(self.results[0].start, time.gmtime(1565445600))

    def test_stop (self):
        self.assertEqual(self.results[0].stop, time.gmtime(1565449200))

    def test_channel (self):
        self.assertEqual(self.results[0].channel,
                         '1d72d745d4a1e046e3070c75b336a1a5')

    def test_summary (self):
        self.assertEqual(self.results[0].summary, '''\
Ice Worlds: David Attenborough's awe-inspiring natural history series visits \
the frozen worlds of the Arctic and Antarctic. See polar bears negotiate the \
retreat of the ice. [S,AD]\
''')

    def test_widescreen (self):
        self.assertEqual(self.results[0].widescreen, True)

    def test_subtitled (self):
        self.assertEqual(self.results[0].subtitled, True)

    def test_audio_desc (self):
        self.assertEqual(self.results[0].audio_desc, True)

    def test_signed (self):
        self.assertEqual(self.results[0].signed, False)
