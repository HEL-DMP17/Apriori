import random

def sample_file(file="../data/raw_data.txt", count=10):
    """
    Samples the main dataset and writes content to samples.txt, used for unitest
    :param file:  Main dataset
    :param count: How many samples need
    :return:
    """
    input("Do you actually want to sample new file? Press to continue..")
    lines = None
    samples = None
    with open(file, 'r') as fr:
        lines = fr.readlines()
    with open("../data/samples.txt", 'w+') as fw:
        samples = random.sample(lines, count)
        for item in samples:
            fw.write(item)

# Private method, no need to add doc string
# Added to construct transaction item names
def _is_name(col, attr):
    return col.upper() + "_IS_" + attr.upper()
