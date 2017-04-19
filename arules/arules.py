# This is the stub for our main runner python file

import argparse
from preprocess import *
from apriori import *

if __name__ == "__main__":
    # Set Defaults
    file = "../data/samples.txt"
    # file = "../data/raw_data.txt"
    sup = 1.2
    conf = 1.5
    # Read arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="The dataset path" + file, type=str)
    parser.add_argument("-s", "--support", help="The minimum support count, DEFAULT: " + str(sup), type=float)
    parser.add_argument("-c", "--confidence", help="The minimum confidence, DEFAULT: " + str(conf), type=float)

    args = parser.parse_args()

    if args.file:
        file = args.file
    if args.support:
        sup = args.support
    if args.confidence:
        conf = args.confidence

    # Preprocess the data
    pp = PreProcessor()
    # If transaction count greater than 0
    if pp.parse_file(file) > 0:
        transactions = pp.get_transactions()
        uniques = pp.get_uniques()
        # pp._print_transactions()
        # print(uniques)
        # Extract association rules using apriori
        apriori = Apriori(transactions, uniques, sup, conf)
        apriori.extract()
