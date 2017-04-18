##########################################
# Import the path to see the other files
import sys
sys.path.append('../arules')
# Import core unittest
import unittest
##########################################

# Import modules to be tested here
from preprocess import PreProcessor


class TestPreprocess(unittest.TestCase):

    def setUp(self):
        self.pp = PreProcessor()
        self.pp.parse_file("../data/samples.txt")

    def test_file_parser(self):
        """ Test routine for file parser """
        count = self.pp.trans_count
        self.assertEqual(count, 10, "Sample file size must be 10")
        print("PreProcessor::file_parser")

    def test_unique_counts(self):
        """ Test unique field counters """
        uq = self.pp.unique
        # self.assertEqual(uq['RACE_IS_HISP_RC'], 1, "Must be equal")
        # self.assertEqual(uq['RACE_IS_BLACK'], 1, "Must be equal")
        self.assertEqual(uq['RACE_IS_WHITE'], 8, "Must be equal")
        self.assertEqual(uq['SEX_IS_FEMALE'], 3, "Must be equal")
        self.assertEqual(uq['SEX_IS_MALE'], 7, "Must be equal")
        print("PreProcessor.unique_counts")

    def test_mapping(self):
        """ Test discretize/binarize here """
        import collections
        self.pp._print_transactions()
        trans = self.pp.get_transactions()
        t1 = trans[0]
        is_others = self.pp.mapper.race['OTHERS'] != None
        self.assertEqual(t1['ID'], 1, "Must be first transaction")
        if is_others:
            self.assertEqual(t1['ITEMS']
                             , collections.OrderedDict([('RACE_IS_OTHERS', True), ('SCORE_IS_[44-57]', True),
                                                        ('SEX_IS_MALE', True)])
                             , "Must be first transaction")
        else:
            self.assertEqual(t1['ITEMS']
                             , collections.OrderedDict([('RACE_IS_HISP_RC', True), ('SCORE_IS_[44-57]', True),
                                                       ('SEX_IS_MALE', True)])
                             , "Must be first transaction")

        print("PreProcessor::mappers")

if __name__ == '__main__':
    unittest.main()