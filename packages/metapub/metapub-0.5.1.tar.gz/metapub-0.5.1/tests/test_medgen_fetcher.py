import unittest, os

from metapub import MedGenFetcher

hugos = ['ACVRL1', 'FOXP3', 'ATM']

TEST_CACHEDIR = 'tests/testcachedir'


class TestMedGenFetcher(unittest.TestCase):

    def setUp(self):
        self.fetch = MedGenFetcher()

    def tearDown(self):
        pass

    def test_fetch_concepts_for_known_gene(self):
        hugo = 'ACVRL1'
        result = self.fetch.uids_by_term(hugo+'[gene]')
        assert result is not None
        assert result[0] == '324960'
    
    def test_fetch_concepts_for_incorrect_term(self):
        term = 'AVCRL'
        result = self.fetch.uids_by_term(term+'[gene]')
        assert result == []
