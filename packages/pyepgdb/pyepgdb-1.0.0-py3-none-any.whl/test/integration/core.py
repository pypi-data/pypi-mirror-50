from unittest import TestCase

import pyepgdb

from .testutil import get_resource_path


class SingleResult (TestCase):
    def setUp (self):
        with open(get_resource_path('single-result.epgdb'), 'rb') as f:
            self.results = list(pyepgdb.parse(f))

    def test_count (self):
        self.assertEqual(len(self.results), 1, 'should be 1 result')

    def test_episode_int_field (self):
        self.assertEqual(self.results[0].episode['id'], 3261217)

    def test_episode_string_field (self):
        self.assertEqual(self.results[0].episode['uri'], 'crid://bds.tv/E0L97G')

    def test_episode_binary_field (self):
        self.assertEqual(self.results[0].episode['genre'],
                         b'\x02\x00\x00\x00\x00\x01\x20')

    def test_episode_object_field (self):
        self.assertEqual(self.results[0].episode['title'],
                         {'eng': 'Planet Earth'})

    def test_episode_empty_object_field (self):
        self.assertEqual(self.results[0].episode['epnum'], {})

    def test_broadcast_int_field (self):
        self.assertEqual(self.results[0].broadcast['start'], 1565445600)

    def test_broadcast_string_field (self):
        self.assertEqual(self.results[0].broadcast['channel'],
                         '1d72d745d4a1e046e3070c75b336a1a5')


class MultipleEpisodes (TestCase):
    def setUp (self):
        with open(get_resource_path('multiple-episodes.epgdb'), 'rb') as f:
            self.results = list(pyepgdb.parse(f))

    def test_count (self):
        self.assertEqual(len(self.results), 2, 'should be 2 results')

    def test_1_episode(self):
        self.assertEqual(self.results[0].episode['id'], 3267319,
                         'should correspond to first broadcast')

    def test_1_broadcast(self):
        self.assertEqual(self.results[0].broadcast['id'], 3267317,
                         'should be first broadcast')

    def test_2_episode(self):
        self.assertEqual(self.results[1].episode['id'], 3261217,
                         'should correspond to second broadcast')

    def test_2_broadcast(self):
        self.assertEqual(self.results[1].broadcast['id'], 3261216,
                         'should be second broadcast')


class MultipleBroadcasts (TestCase):
    def setUp (self):
        with open(get_resource_path('multiple-broadcasts.epgdb'), 'rb') as f:
            self.results = list(pyepgdb.parse(f))

    def test_count (self):
        self.assertEqual(len(self.results), 2, 'should be 2 results')

    def test_1_episode(self):
        self.assertEqual(self.results[0].episode['id'], 3261217,
                         'should be the episode')

    def test_1_broadcast(self):
        self.assertEqual(self.results[0].broadcast['id'], 3261216,
                         'should be first broadcast')

    def test_2_episode(self):
        self.assertEqual(self.results[1].episode['id'], 3261217,
                         'should be the episode')

    def test_2_broadcast(self):
        self.assertEqual(self.results[1].broadcast['id'], 3261251,
                         'should be second broadcast')


class BroadcastsFirst (TestCase):
    def setUp (self):
        with open(get_resource_path('broadcasts-first.epgdb'), 'rb') as f:
            self.results = list(pyepgdb.parse(f))

    def test_count (self):
        self.assertEqual(len(self.results), 1, 'should be 1 result')

    def test_episode(self):
        self.assertEqual(self.results[0].episode['id'], 3261217,
                         'episode ID should match')

    def test_broadcast(self):
        self.assertEqual(self.results[0].broadcast['id'], 3261216,
                         'broadcast ID should match')
