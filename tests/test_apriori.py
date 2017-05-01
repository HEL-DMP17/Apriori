##########################################
# Import the path to see the other files
import sys
sys.path.append('../src')
# Import core unittest
import unittest
##########################################

# Import modules to be tested here
from apriori import Apriori
from preprocess import PreProcessor

class TestPreprocess(unittest.TestCase):

    def setUp(self):
        pp = PreProcessor()
        pp.parse_file("../data/samples.txt")
        transactions = pp.get_transactions()
        uniques = pp.get_uniques()
        sup = 2.0
        conf = 0.374
        self.apriori = Apriori(transactions, uniques, sup, conf)

    def test_frequent_itemsets(self):
        # fis = self.apriori.freq_itemsets[0:3]
        # expected = [{'ID': 1, 'FREQ': 2, 'ITEMS': ['RACE_IS_OTHERS', 'SEX_IS_MALE']},
        #             {'ID': 2, 'FREQ': 2, 'ITEMS': ['SCORE_IS_[44-57]', 'SEX_IS_MALE']},
        #             {'ID': 3, 'FREQ': 5, 'ITEMS': ['RACE_IS_WHITE', 'SEX_IS_MALE']}]
        # self.assertEqual(expected, fis, "Freuquent itemsets are incorrect")
        print("Apriori::apriori_run")

    def test_arules(self):
        # arules = self.apriori.extract()
        # crop_2 = arules[0:2] # get only 2 elements, # LIFT is symmetric measure
        # expected = [{'LEFT': ['RACE_IS_WHITE'], 'RIGHT': ['SEX_IS_FEMALE'], 'CONF': 0.375, 'LIFT': 1.25},
        #             {'LEFT': ['SEX_IS_FEMALE'], 'RIGHT': ['RACE_IS_WHITE'], 'CONF': 1.0, 'LIFT': 1.25}]
        # self.assertEqual(crop_2, expected, "Association rules are incorrect")
        print("Apriori::extract")

if __name__ == '__main__':
    unittest.main()