# Global modules
import collections
import math
import time

# Internal modules
from src.utils import *

class PreProcessor:
    """
    The preprocessor class that handles binarization and discretization of dataset
    """
    def __init__(self):
        self.transactions = []
        self.unique = collections.OrderedDict()
        self.trans_count = 0
        self.mapper = PreProcessor.Mapper()

    def get_transactions(self):
        """
        Getter method for transactions list of OrderedDict

        :return: Transactions list (list(OrderedDict))
        """
        return self.transactions

    def get_uniques(self):
        """
        Getter method for unique itemsets (dictionary)

        :return: Unique itemsets (dict), key: items, value: counts
        """
        return self.unique

    def get_transaction_count(self):
        """
        Getter method for transaction count after parsing the file

        :return: Transaction count (int)
        """
        return self.trans_count

    def parse_file(self, file):
        """ The main function to parse the file and run the preprocesser methods

        :param file: Filepath of the data
        :return: Returns number of the transaction parsed (int)
        """
        print("Preprocess begin to parse the file")
        start_t = time.clock()
        mp = self.mapper
        with open(file, "r") as f:
            for line in f:
                chars = str(line)
                # Get all the necessary fields here
                sex = self.get_field(chars, mp.sex)
                race = self.get_field(chars, mp.race)
                score = self.get_field(chars, mp.score)
                lang_native=self.get_field(chars,mp.lang_native)
                fam_comp=self.get_field(chars,mp.family_comp)

                # Add this into transaction. Put all the fields into the list
                fields = [sex, race, score,lang_native,fam_comp]
                self.add_transaction(fields)
        # Performance measurements
        total_t = str(format(time.clock() - start_t, '.4f'))
        print("Preprocessing took {:>10} seconds"
              .format(total_t))
        # Return number of transactions added
        return self.trans_count

    def get_field(self, line, mapper):
        """
        Selects the appropriate preprocessing method according to line and mapper structure
        :param line: New line of data (str)
        :param mapper: Corresponding mapper structure of the field
        :return: Preprocessed field (str)
        """
        value = line[mapper['STR'] - 1: mapper['END']]
        # Check the type and execute either discretize/binarize etc.
        if mapper['TYPE'] == 'BINARY':
            return self._is_name(mapper['COL'], mapper['VALS'][int(value)])
        elif mapper['TYPE'] == 'CATEGORICAL':
            return self.binarize(mapper, int(value))  # Change here later for OTHER field
        else:
            return self.discretize(mapper, float(value))

    def add_transaction(self, fields):
        """
        Adds the preprocessed fields into the transaction list

        :param fields: Preprocessed fields (list)
        :return:
        """
        self.trans_count += 1
        items = collections.OrderedDict()
        # Add the fields here, True is only used to have
        # OrderedSet kind of data structure
        items = collections.OrderedDict({f: True for f in fields})  # more pythonic way to populate
        self.count_unique(fields)  # Updates unique dict
        # Use keys to sort the dict
        items = collections.OrderedDict(sorted(items.items(), key=lambda _: _[0]))
        t = {'ID': self.trans_count, 'ITEMS': items}
        self.transactions.append(t)

    def count_unique(self, fields):
        """
        Updates the count of unique fields

        :param fields: List of fields
        :return:
        """
        for f in fields:
            if f not in self.unique:
                self.unique[f] = 1
            else:
                self.unique[f] += 1
        self.unique = collections.OrderedDict(sorted(self.unique.items(), key=lambda _: _[0]))

    def discretize(self, mapper, col_data):
        """
        Used to discretize the continous values from the given mapper and value
        :param mapper: Mapper of the continious field  (Mapper Class)
        :param col_data: Value of the continous field (float)
        :return: Returns discretized name of the field (string)
        """
        max = math.ceil(mapper['MAX'])
        min = math.floor(mapper['MIN'])
        interval = mapper['INTERVAL']
        step = (max - min) / interval
        # Initial check to decide in which range it belongs to
        lower = float(format(min, '.2f'))
        upper = float(format(lower + step, '.2f'))
        if col_data >= lower and col_data <= upper:
            str_interval = '[' + str(int(lower)) + '-' + str(int(upper)) + ']'
            # print('Lower : ' + str(lower) + ' Upper : ' + str(upper)
            #       + ' Value : ' + str(col_data) + ' Interval : ' + str_interval)
            return self._is_name(mapper['COL'], str_interval)

        # Check the boundries until the end of the interval value
        for i in range(1, interval):
            lower = float(format(upper, '.2f'))
            upper = float(format(upper + step, '.2f'))
            if col_data >= lower and col_data <= upper:
                str_interval = '[' + str(int(lower)) + '-' + str(int(upper)) + ']'
                # print('Lower : ' + str(lower) + ' Upper : ' + str(upper)
                #       + ' Value : ' + str(col_data) + ' Interval : ' + str_interval)
                return self._is_name(mapper['COL'], str_interval)

        raise ValueError('Value is not between the intervals check preprocessor::discretize')

    def binarize(self, mapper, col_data):
        """
        Binarize the attribute data using mapper
        :param col_data: Categorical data assumed to be between -9 and 25
        :param mapper: Corresponding mapper of this field
        :return: Binarized field (str)
        """
        if mapper is None:
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
            if mapper['OTHERS'] is not None:
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
                nm = self._is_name(col=mapper['COL'], attr=mapper['VALS'][col_data])

            # Return the name
            return nm
        else:
            raise ValueError('This key is not inside our mapper VALS - check binarize method in preprocess.py')

    def save_transactions(self, path = "transactions.csv"):
        """
        Save the preprocessed transactions into a file
        :param path: Path to be saved
        :return: Returns true on successful save
        """
        print('Saving the transactions into {}'.format(path))
        start_t = time.clock()
        with open(path, 'w') as f:
            f.write("ID,ITEMS\n")
            for t in self.transactions:
                print_str = str(t['ID'])
                for i in t['ITEMS'].keys():
                    print_str += "," + i
                print_str += "\n"
                f.write(print_str)
        # Performance measurements
        total_t = str(format(time.clock() - start_t, '.4f'))
        print("Save procedure took {:>10} seconds"
              .format(total_t))
        return True

    def _print_transactions(self):
        """
        Used to print transactions in csv format
        :return:
        """
        print_str = "ID,ITEMS\n"
        for t in self.transactions:
            print_str += str(t['ID'])
            for i in t['ITEMS'].keys():
                print_str += "," + i
            print_str += "\n"
        print(print_str)

    def _is_name(self, col, attr):
        """
        Used to construct the itemset name with combination of column and attiribute
        :param col: Column name of the data (str)
        :param attr: Attribute name of the data (str)
        :return: Itemset name (str)
        """
        return col.upper() + "_IS_" + attr.upper()

    # Until getting nice representation using files(possibly JSON) use this structure
    # later we can create the file structure and parser for that.
    class Mapper:
        """
        Used to map the fields
        """
        def __init__(self):
            # Some fields can change
            self.sex = {'COL': 'SEX', 'TYPE': 'BINARY', 'STR': 24, 'END': 25,
                        'OTHERS': None,
                        'VALS': {1: 'MALE', 2: 'FEMALE'}}

            # Combine fields that are in others together
            self.race = {'COL': 'RACE', 'TYPE': 'CATEGORICAL', 'STR': 26, 'END': 27,
                         'OTHERS': {4: 'HISP_NR', 5: 'HISP_RC', 3: 'BLACK'},
                         'VALS': {1: 'AMER', 2: 'ASIA', 3: 'BLACK',
                                  4: 'HISP_NR', 5: 'HISP_RC', 6: 'MULT',
                                  7: 'WHITE'}}

            # self.race_others = {'COL': 'RACE', 'TYPE': 'CATEGORICAL', 'STR': 26, 'END': 27,
            #              'OTHERS': None,
            #              'VALS': {1: 'AMER', 2: 'ASIA', 3: 'BLACK',
            #                      4: 'HISP_NR', 5: 'HISP_RC', 6: 'MULT',
            #                      7: 'WHITE'}}

            # SCORE_IS-20_60 , 35.12
            self.score = {'COL': 'SCORE', 'TYPE': 'CONTINIOUS', 'STR': 106, 'END': 111,
                          'MIN': 20.91, 'MAX': 81.04, 'INTERVAL': 5}

            self.lang_native = {'COL': 'ENG_LANG_NATIVE', 'TYPE': 'BINARY', 'STR': 28, 'END': 29,
                        'OTHERS': None,
                        'VALS': {0: 'NO', 1: 'YES'}}

            self.family_comp = {'COL': 'FAM', 'TYPE': 'CATEGORICAL', 'STR': 42, 'END': 43,
                         'OTHERS':{4: 'GG', 5: 'M', 6: 'F', 7: 'FEG', 8: 'MAG',9: 'HALFTIME'},
                         'VALS': {1: 'MF', 2: 'MG', 3: 'FG',
                                  4: 'GG', 5: 'M', 6: 'F',
                                  7: 'FEG', 8: 'MAG',9: 'HALFTIME'}}
