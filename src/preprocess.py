# This is the stub file our preprocessor python file

"""
This will be PREPROCESSOR class
"""
class PreProcessor:
    def __init__(self, file, intervals):
        self.file = file
        self.intervals = intervals
        self.transactions = None
        self.mapper = PreProcessor.Mapper()
        # Call the reader
        self.read_file(self.file)

    def read_file(self, file):
        """
        File reader for student-level dataset
        :param file: Filepath for dataset
        :return:
        """
        mp = self.mapper
        with open(file, "r") as f:
            for line in f:
                chars = str(line)
                sex = chars[mp.sex['STR'] - 1: mp.sex['END']]
                race = chars[mp.race['STR'] - 1: mp.race['END']]
                score = chars[mp.score['STR'] - 1 : mp.score['END']]
                print("Sex: " + mp.sex['VALS'][int(sex)] +
                      " Race: " + mp.race['VALS'][int(race)] +
                      " Score: " + score)
                input("")

    def discretize(self):
        """
        Discretize the continious valued attributes
        :return:
        """
        print("discretize stub")

    def binarize(self):
        """
        Binarize the categorical attributes
        :return:
        """
        print("binarize stub")

    def get_transactions(self):
        """
        Returns transaction table preprocessed from the file at start

        |TID|                   ITEMS                           |
        | 1 | SEX_IS_MALE, RACE_IS_WHITE, SCORE_IS_40-50, ..    |
            ...
            ...
            
        :return: Transaction table
        """
        return self.transactions

    # Until getting nice representation using files use this structure
    # later we can create the file structure and parser for that
    class Mapper:
        def __init__(self):
            self.sex = {'COL': 'SEX', 'CONT': 0, 'STR': 24, 'END': 25,
                        'VALS': {1: 'MALE', 2: 'FEMALE'}}

            self.race = {'COL': 'RACE', 'CONT': 0, 'STR': 26, 'END': 27,
                         'VALS': {1: 'AMER', 2: 'ASIA', 3: 'BLACK',
                                 4: 'HISP_NR', 5: 'HISP_RC', 6: 'MULT',
                                 7: 'WHITE'}}
            self.score = {'COL': 'SCORE', 'CONT': 1, 'STR': 106, 'END': 111}