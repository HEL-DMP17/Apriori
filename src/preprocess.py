# Global modules
import collections
from  more_itertools import unique_everseen
import itertools

# Internal modules
from utils import *

"""
This will be PREPROCESSOR class, TODO: add some explaination
"""
class PreProcessor:
    def __init__(self, file, intervals):
        self.file = file
        self.intervals = intervals
        self.transactions = []
        self.unique = {}
        self.trans_count = 0
        self.mapper = PreProcessor.Mapper()
        # Parse the file
        self.parse_file(file)
        self._print_transactions()
        print(self.unique)

    def parse_file(self, file):
        """
        File reader for student-level dataset
        :param file: Filepath for dataset
        :return:
        """
        mp = self.mapper

        with open(file, "r") as f:
            for line in f:
                chars = str(line)
                # Get all the necessary fields here
                sex = self.get_field(chars, mp.sex)
                race = self.get_field(chars, mp.race)
                # score = self.get_field(chars, mp.score)
                # Add this into transaction. Put all the fields into the list
                fields = [sex, race]
                self.add_transaction(fields)
        # Return number of transactions added
        return self.trans_count

    def get_field(self, line, mapper):
        value = line[mapper['STR'] - 1: mapper['END']]
        # Check the type and execute either disretize/binarize etc.
        if mapper['TYPE'] == 'BINARY':
            return self._is_name(mapper['COL'], mapper['VALS'][int(value)])
        elif mapper['TYPE'] == 'CATEGORICAL':
            return self.binarize(mapper, int(value)) # Change here later for OTHER field
        else:
            self.discretize()


    def add_transaction(self, fields):
        self.trans_count += 1
        items = collections.OrderedDict()
        # Add the fields here, True is only used to have
        # OrderedSet kind of data structure
        items = collections.OrderedDict({f: True for f in fields}) # more pythonic way to populate
        self.count_unique(fields) # Updates unique dict
        # Use keys to sort the dict
        items = collections.OrderedDict(sorted(items.items(), key=lambda t: t[0]))
        t = {'ID': self.trans_count, 'ITEMS': items}
        self.transactions.append(t)

    def count_unique(self, fields):
        """
        Used to increment the unique fields
        :param fields: List of fields(str). sex, gender, score ..
        :return: Increments self.unique dictionary
        """
        for f in fields:
            if f not in self.unique:
                self.unique[f] = 1
            else:
                self.unique[f] += 1

    def discretize(self):
        """
        Discretize the continious valued attributes
        :return:
        """
        print("discretize stub")
        return "imam hatipler kapatilsin"

    def binarize(self, mapper, col_data):
        """
        Binarize the attribute data using mapper
        :param col_data: Categorical data assumed to be between -9 and 25
        :param mapper: Corresponding mapper of this field
        :return: Binarized field - str
        """
        if mapper == None:
            print("Give an appropriate mapper")
            return

        if col_data < -9:
            raise ValueError('Values cannot be less than -9 - check binarize method in preprocess.py')

        # Change this, in case if we break something
        max_categorical_value = 25
        if col_data > max_categorical_value:
            raise ValueError('Values cannot be more than 25 - check binarize method in preprocess.py')

        # Return proper COL_IS_ATTR name
        if col_data in mapper['VALS'].keys():
            if mapper['OTHERS'] != None:
                if col_data in mapper['OTHERS']:
                    # Others
                    nm = self._is_name(col=mapper['COL'], attr="OTHERS")
                elif col_data in mapper['VALS']:
                    # Map as standalone field
                    nm = self._is_name(col=mapper['COL'], attr=mapper['VALS'][col_data])
                else:
                    raise Exception("Something unusual in preprocessor::binarize happened")
            else:
                # Map as standalone field
                nm = self._is_name(col = mapper['COL'], attr = mapper['VALS'][col_data])

            # Return the name
            return nm
        else:
            raise ValueError('This key is not inside our mapper VALS - check binarize method in preprocess.py')

    def _print_transactions(self):
        """
        Used to print transactions in pretty format
        :return:
        """
        # TODO: fix printing using formatted print
        print_str = "ID   ITEMS\n"
        for t in self.transactions:
            print_str += str(" " + str(t['ID']) + " |")
            for i in t['ITEMS'].keys():
                print_str += " " + i +" "

            print_str += " \n"
        print(print_str)
        """
        | ID |              ITEMS              |
        | 1 | SEX_IS_MALE, RACE_IS_BLACK ...   |
        | 2 | SEX_IS_MALE, RACE_IS_BLACK ...   |

        """

    def get_transactions(self):
        return self.transactions
        # self.pre_lines = self.file_lines
        # print(float(self.pre_lines[2][1]))
        # for values in range(len(self.pre_lines[2])):
        #     if float(self.pre_lines[2][values])>50:
        #         self.pre_lines[2][values]='>=50'
        #     else:
        #         self.pre_lines[2][values]='<50'
        #
        # '''print(collections.Counter(self.pre_lines[0]))
        # print(collections.Counter(self.pre_lines[1]))
        # print(list(unique_everseen(self.pre_lines[0])))
        # print(list(unique_everseen(self.pre_lines[1])))
        #
        # print("colections", list(itertools.zip_longest(self.pre_lines[0])))'''
        #
        # self.transactions=[]
        # print('---')
        # for field in range(0,3): #here will be replaced the total number of fields using the input list method
        #     l1=(list((collections.Counter(itertools.zip_longest(self.pre_lines[field]))).items()))
        #     for ele in range(len(l1)):
        #         self.transactions.append(l1[ele])
        #
        # l2=(list(collections.Counter(itertools.zip_longest(self.pre_lines[0], self.pre_lines[1])).items()))
        #
        # l21=(list(collections.Counter(itertools.zip_longest(self.pre_lines[1], self.pre_lines[2])).items()))
        #
        # l3=(list(collections.Counter(itertools.zip_longest(self.pre_lines[0], self.pre_lines[1],self.pre_lines[2])).items()))
        #
        #
        # for ele in range(len(l2)):
        #     self.transactions.append(l2[ele])
        #     self.transactions.append(l21[ele])
        #
        # for ele in range(len(l3)):
        #     self.transactions.append(l3[ele])
        #
        # for line in range (len(self.transactions)):
        #     print (self.transactions[line])
        #
        # """
        # Returns transaction table preprocessed from the file at start
        #
        # |TID|                   ITEMS                           |
        # | 1 | SEX_IS_MALE, RACE_IS_WHITE, SCORE_IS_40-50, ..    |
        # | 2 | a, b, c, d |
        # | 3 | a, b, c, e
        #     ...
        #     ...
        #
        # a, b, c
        # b, c
        # c
        #
        # TID LIST
        #
        # b, c
        # b, c
        # c
        #
        # 1-freq
        # ------
        # a 1
        # b 2
        # c 3
        #
        # 2-freq
        # ------
        # b c: 1
        #
        # 3-freq
        # ------
        # None
        #
        # (('MALE',), 7)
        # (('FEMALE',), 3)
        # (('HISP_RC',), 1)
        # (('WHITE',), 8)
        # (('BLACK',), 1)
        # (('<50',), 1)
        # (('>=50',), 9)
        #
        # :return: Transaction table
        # """

    # Added to construct transaction item names
    # There are some attiributes having 'MISSING_VALUE' types
    # So we cannot be sure if we only add the attr type
    # Better to combine with column name as well
    def _is_name(self, col, attr):
        return col.upper() + "_IS_" + attr.upper()

    # Until getting nice representation using files(possibly JSON) use this structure
    # later we can create the file structure and parser for that.
    class Mapper:
        def __init__(self):
            # Some fields can change
            # TODO: Add 'OTHERS' field that will have fields we want to combine
            self.sex = {'COL': 'SEX', 'TYPE': 'BINARY', 'STR': 24, 'END': 25,
                        'OTHERS': None,
                        'VALS': {1: 'MALE', 2: 'FEMALE'}}

            # Combine fields that are in others together
            self.race = {'COL': 'RACE', 'TYPE': 'CATEGORICAL', 'STR': 26, 'END': 27,
                         'OTHERS': {4: 'HISP_NR', 5: 'HISP_RC', 3: 'BLACK'},
                         'VALS': {1: 'AMER', 2: 'ASIA', 3: 'BLACK',
                                 4: 'HISP_NR', 5: 'HISP_RC', 6: 'MULT',
                                 7: 'WHITE'}}

            self.race_others = {'COL': 'RACE', 'TYPE': 'CATEGORICAL', 'STR': 26, 'END': 27,
                         'OTHERS': None,
                         'VALS': {1: 'AMER', 2: 'ASIA', 3: 'BLACK',
                                 4: 'HISP_NR', 5: 'HISP_RC', 6: 'MULT',
                                 7: 'WHITE'}}
            self.score = {'COL': 'SCORE', 'TYPE': 'CONTINIOUS', 'STR': 106, 'END': 111}
