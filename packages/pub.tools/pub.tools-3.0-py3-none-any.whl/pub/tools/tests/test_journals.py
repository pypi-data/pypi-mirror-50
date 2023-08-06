import unittest

from ..journals import atoj, cache, jtoa


class TestJournals(unittest.TestCase):

    def test_atoj(self):
        self.assertEqual(atoj('J Cancer'), 'Journal of Cancer')

    def test_jtoa(self):
        self.assertEqual(jtoa('Journal of Cancer'), 'J Cancer')

    def test_cache(self):
        # just verify it runs, for test coverage
        cache()


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
