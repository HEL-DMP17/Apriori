# This is the stub for our main runner python file

import argparse
from preprocess import *
from apriori import *

if __name__ == "__main__":
    # Set Defaults
    file = "../data/samples.txt"
    # file = "../data/raw_data.txt"
    intervals = 10
    sup = 1.2
    conf = 1.5
    # Read arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="The dataset path" + file, type=str)
    parser.add_argument("-i", "--intervals",
                        help="Number of intervals to discretize the continious attributes, DEFAULT: "
                        + str(intervals), type=int)
    parser.add_argument("-s", "--support", help="The minimum support count, DEFAULT: " + str(sup), type=float)
    parser.add_argument("-c", "--confidence", help="The minimum confidence, DEFAULT: " + str(conf), type=float)

    args = parser.parse_args()

    if args.file:
        file = args.file
    if args.intervals:
        intervals = args.intervals
    if args.support:
        sup = args.support
    if args.confidence:
        conf = args.confidence
    # Preprocess the data
    pp = PreProcessor(file, intervals)

    # Run the apriori algorithm
    # apriori = Apriori(transactions, sup, conf)
    # Extract the frequent patterns - rules
    # apriori.extract()

