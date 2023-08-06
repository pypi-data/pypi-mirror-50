from unittest import TestCase, skip
from languageflow.data_fetcher import DataFetcher, NLPData


@skip
class TestDataSets(TestCase):

    def test_uts2017_bank_sa(self):
        corpus = DataFetcher.load_corpus(NLPData.UTS2017_BANK_SA)
        print(corpus)

    def test_uts2017_bank_tc(self):
        corpus = DataFetcher.load_corpus(NLPData.UTS2017_BANK_TC)
        print(corpus)

    def test_vlsp2016_sa(self):
        corpus = DataFetcher.load_corpus(NLPData.VLSP2016_SA)
        print(corpus)

    def test_vntc(self):
        corpus = DataFetcher.load_corpus(NLPData.VNTC)
        print(corpus)
