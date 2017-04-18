##########################################
# Import the path to see the other files
import sys
sys.path.append('../arules')
# Import core unittest
import unittest
##########################################

# Import modules to be tested here
from apriori import Apriori


class TestPreprocess(unittest.TestCase):

    def setUp(self):
        print('Test apriori')

if __name__ == '__main__':
    unittest.main()