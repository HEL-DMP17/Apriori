# This is the stub for our main runner python file

import argparse
from preprocess import *
from apriori import *

if __name__ == "__main__":
    # Set Defaults
    path = "data/"
    intervals = 10

    # Read arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", help="The location of dataset" + path, type=str)
    parser.add_argument("-i", "--intervals",
                        help="Number of intervals to discretize the continious attributes, DEFAULT: "
                        + str(intervals), type=int)

    args = parser.parse_args()

    if args.path:
        path = args.path
    if args.intervals:
        intervals = args.intervals

    # Preprocess the data
    PP = PreProcessor()
    # Run the apriori algorithm
    apriori = Apriori()
    # Extract the frequent patterns - rules
    apriori.extract()

