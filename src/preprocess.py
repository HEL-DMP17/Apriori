# For global modules
from utils import *

# For private modules and methods
from src.utils import _is_name
import collections
from  more_itertools import unique_everseen
import itertools


"""
This will be PREPROCESSOR class, TODO: add some explaination
"""
class PreProcessor:
    def __init__(self, file, intervals):
        self.file = file
        self.intervals = intervals
        # Example end results
        # self.transactions = {'COUNT': 2, 'T': {'SEX_IS_FEMALE': 1, 'SEX_IS_MALE': 1, 'RACE_IS_WHITE': 2}}
        self.transactions = {'COUNT': 0, 'T': {}}
        self.mapper = PreProcessor.Mapper()
        # Call this to sample main raw_data helper
        self.read_file(file)
        self.file_lines = self.read_file(file)
        self.get_transactions()

    def read_file(self, file):
        """
        File reader for student-level dataset
        :param file: Filepath for dataset
        :return:
        """
        #_is_name(field="ali", attr="veli")
        mp = self.mapper

        items_matrix=[]
        sex_matrix=[]
        race_matrix=[]
        score_matrix=[]

        with open(file, "r") as f:
            for line in f:
                chars = str(line)
                # Get all the necessary fields here
                sex = chars[mp.sex['STR'] - 1: mp.sex['END']]
                race = chars[mp.race['STR'] - 1: mp.race['END']]
                score = chars[mp.score['STR'] - 1 : mp.score['END']]

                print("Sex: " + mp.sex['VALS'][int(sex)] +
                      " Race: " + mp.race['VALS'][int(race)] +
                      " Score: " + score)

                sex_matrix.append(mp.sex['VALS'][int(sex)])
                race_matrix.append(mp.race['VALS'][int(race)])
                score_matrix.append(score)

        items_matrix.extend((sex_matrix,race_matrix,score_matrix))
        return items_matrix

    def discretize(self):
        """
        Discretize the continious valued attributes
        :return:
        """
        print("discretize stub")

    def binarize(self, col_data, mapper_col):
        """
        Binarize the attribute data using mapper
        :param col_data: Categorical data assumed to be between -9 and 25
        :param mapper_col: Corresponding mapper of this field
        :return: Binarized field - str
        """
        if mapper_col == None:
            print("Give an appropriate mapper")
            return

        if col_data < -9:
            raise ValueError('Values cannot be less than -9 - check binarize method in preprocess.py')

        # Change this, if we break something
        max_categorical_value = 25
        if col_data > max_categorical_value:
            raise ValueError('Values cannot be more than 25 - check binarize method in preprocess.py')

        # Return proper COL_IS_ATTR name
        if col_data in mapper_col['VALS'].keys():
            nm = _is_name(col = mapper_col['COL'],
                      attr = mapper_col['VALS'][col_data])
            print(nm)
        else:
            raise ValueError('This key is not inside our mapper VALS - check binarize method in preprocess.py')

    def get_transactions(self):
        self.pre_lines = self.file_lines
        print(float(self.pre_lines[2][1]))
        for values in range(len(self.pre_lines[2])):
            if float(self.pre_lines[2][values])>50:
                self.pre_lines[2][values]='>=50'
            else:
                self.pre_lines[2][values]='<50'

        '''print(collections.Counter(self.pre_lines[0]))
        print(collections.Counter(self.pre_lines[1]))
        print(list(unique_everseen(self.pre_lines[0])))
        print(list(unique_everseen(self.pre_lines[1])))

        print("colections", list(itertools.zip_longest(self.pre_lines[0])))'''

        self.transactions=[]
        print('---')
        for field in range(0,3): #here will be replaced the total number of fields using the input list method
            l1=(list((collections.Counter(itertools.zip_longest(self.pre_lines[field]))).items()))
            for ele in range(len(l1)):
                self.transactions.append(l1[ele])

        l2=(list(collections.Counter(itertools.zip_longest(self.pre_lines[0], self.pre_lines[1])).items()))

        l21=(list(collections.Counter(itertools.zip_longest(self.pre_lines[1], self.pre_lines[2])).items()))

        l3=(list(collections.Counter(itertools.zip_longest(self.pre_lines[0], self.pre_lines[1],self.pre_lines[2])).items()))


        for ele in range(len(l2)):
            self.transactions.append(l2[ele])
            self.transactions.append(l21[ele])

        for ele in range(len(l3)):
            self.transactions.append(l3[ele])

        for line in range (len(self.transactions)):
            print (self.transactions[line])

        """
        Returns transaction table preprocessed from the file at start

        |TID|                   ITEMS                           |
        | 1 | SEX_IS_MALE, RACE_IS_WHITE, SCORE_IS_40-50, ..    |
            ...
            ...

        :return: Transaction table
        """
        return self.transactions

    # Until getting nice representation using files(possibly JSON) use this structure
    # later we can create the file structure and parser for that.
    class Mapper:
        def __init__(self):
            # Some fields can change
            self.sex = {'COL': 'SEX', 'CONT': 0, 'STR': 24, 'END': 25,
                        'VALS': {1: 'MALE', 2: 'FEMALE'}}

            self.race = {'COL': 'RACE', 'CONT': 0, 'STR': 26, 'END': 27,
                         'VALS': {1: 'AMER', 2: 'ASIA', 3: 'BLACK',
                                 4: 'HISP_NR', 5: 'HISP_RC', 6: 'MULT',
                                 7: 'WHITE'}}
            self.score = {'COL': 'SCORE', 'CONT': 1, 'STR': 106, 'END': 111}