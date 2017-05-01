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
                fam_comp=self.get_field(chars,mp.fam_comp)
                par_edu=self.get_field(chars,mp.par_edu)
                income=self.get_field(chars,mp.income)
                s_expect=self.get_field(chars,mp.s_expect)
                control=self.get_field(chars,mp.control)
                sc_loc=self.get_field(chars,mp.sc_loc)
                fight=self.get_field(chars,mp.fight)
                late = self.get_field(chars, mp.late)
                homework = self.get_field(chars, mp.homework)
                sh_accomp = self.get_field(chars, mp.sh_accomp)
                sh_poorp = self.get_field(chars, mp.sh_poorp)
                good_grec = self.get_field(chars, mp.good_grec)
                likes_s = self.get_field(chars, mp.likes_s)
                library = self.get_field(chars, mp.library)

                # Add this into transaction. Put all the fields into the list
                fields = [sex, race, score, lang_native, fam_comp,
                          par_edu,income, s_expect, control, sc_loc,
                          fight, late, homework, sh_accomp, sh_poorp,
                          good_grec, likes_s, library]

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

            # Whether English is student's native language-composite
            self.lang_native = {'COL': 'ENG_LANG_NATIVE', 'TYPE': 'BINARY', 'STR': 28, 'END': 29,
                        'OTHERS': None,
                        'VALS': {0: 'NO', 1: 'YES'}}

            # Family composition
            self.fam_comp = {'COL': 'FAM', 'TYPE': 'CATEGORICAL', 'STR': 42, 'END': 43,
                         'OTHERS':{4: 'GG', 5: 'M', 6: 'F', 7: 'FEG', 8: 'MAG',9: 'HALFTIME'},
                         'VALS': {1: 'MF', 2: 'MG', 3: 'FG',
                                  4: 'GG', 5: 'M', 6: 'F',
                                  7: 'FEG', 8: 'MAG',9: 'HALFTIME'}}

            # Parents' highest level of education
            self.par_edu = {'COL': 'PAR_EDU', 'TYPE': 'CATEGORICAL', 'STR': 44, 'END': 45,
                                'OTHERS': None,
                                'VALS': {1: 'UHS', 2: 'HS', 3: 'US',
                                         4: 'S', 5: 'UC', 6: 'C',
                                         7: 'M', 8: 'PHD'}}

            # Total family income from all sources 2001-composite
            self.income = {'COL': 'INCOME', 'TYPE': 'CATEGORICAL', 'STR': 54, 'END': 55,
                            'OTHERS': {1: 'NONE', 2: '0-1K', 3: '1-5K'},
                            'VALS': {1: 'NONE', 2: '0-1K', 3: '1-5K',
                                     4: '5-10K', 5: '10-15K', 6: '15-20K',
                                     7: '20-25K', 8: '25-35K', 9: '35-50K',
                                     10: '50-75K', 11: '75-100K',12: '100-200K',
                                     13: '200K-more'}}

            # How far in school student thinks will get-composite
            self.s_expect = {'COL': 'S_EXPEC', 'TYPE': 'CATEGORICAL', 'STR': 72, 'END': 73,
                                'OTHERS': None,
                                'VALS': {-1:'UK',
                                         1: 'UHS', 2: 'HS', 3: 'S',
                                         4: 'UC', 5: 'C', 6: 'M',
                                         7: 'PHD'}}

            # School control
            self.control = {'COL': 'SC_CTRL', 'TYPE': 'CATEGORICAL', 'STR': 253, 'END': 253,
                             'OTHERS': None,
                             'VALS': {1: 'PUB', 2: 'CAT', 3: 'PRI'}}

            # School urbanicity
            self.sc_loc = {'COL': 'SC_LOC', 'TYPE': 'CATEGORICAL', 'STR': 254, 'END': 254,
                          'OTHERS': None,
                          'VALS': {1: 'UR', 2: 'SUB', 3: 'RU'}}

            # Got into a physical fight at school
            self.fight = {'COL': 'FIGHT', 'TYPE': 'CATEGORICAL', 'STR': 336, 'END': 337,
                             'OTHERS': {-9: 'MISSING', -7: 'NOT_INTERV', -6: 'MUL_RESP'},
                             'VALS': {-9: 'MISSING', -7: 'NOT_INTERV', -6: 'MUL_RESP',
                                      1: 'NEVER', 2: '1-2', 3: '2-MORE'}}

            # Got into a physical fight at school
            self.late = {'COL': 'LATE', 'TYPE': 'CATEGORICAL', 'STR': 358, 'END': 359,
                          'OTHERS': {-9: 'MISSING', -7: 'NOT_INTERV', -6: 'MUL_RESP'},
                          'VALS': {-9: 'MISSING', -7: 'NOT_INTERV', -6: 'MUL_RESP',
                                   1: 'NEVER', 2: '1-2', 3: '3-6',
                                   4: '7-9', 5: '10-more'}}

            # How often student completes homework
            self.homework = {'COL': 'HOMEWORK', 'TYPE': 'CATEGORICAL', 'STR': 1610, 'END': 1611,
                         'OTHERS': {-9: 'MISSING', -6: 'MUL_RESP', -4: 'NO_ASW',
                                    -3: 'SKIP_ANS',-1 : 'DONT_K'},
                         'VALS': {-9: 'MISSING', -6: 'MUL_RESP', -4: 'NO_ASW',
                                  -3: 'SKIP_ANS',-1 : 'DONT_K',
                                  1: 'NEVER', 2: 'RARELY', 3: 'SOMET',
                                  4: 'MOSTT', 5: 'ALLT'}}

            # Spoke to parents about accomplishments (English)
            self.sh_accomp = {'COL': 'SH_ACCOMP', 'TYPE': 'CATEGORICAL', 'STR': 1590, 'END': 1591,
                         'OTHERS': {-9: 'MISSING', -4: 'NO_ASW', -3: 'SKIP_ANS'},
                         'VALS': {-9: 'MISSING', -4: 'NO_ASW', -3: 'SKIP_ANS',
                                  0: 'NO', 1: 'YES'}}

            #Spoke to parents about poor performance (English)
            self.sh_poorp = {'COL': 'SH_POORP', 'TYPE': 'CATEGORICAL', 'STR': 1582, 'END': 1583,
                              'OTHERS': {-9: 'MISSING', -6: 'MUL_RESP', -4: 'NO_ASW',
                                         -3: 'SKIP_ANS'},
                              'VALS': {-9: 'MISSING', -6: 'MUL_RESP', -4: 'NO_ASW',
                                       -3: 'SKIP_ANS',
                                       0: 'NO', 1: 'YES'}}

            # Recognized for good grades
            self.good_grec = {'COL': 'RECOG', 'TYPE': 'CATEGORICAL', 'STR': 350, 'END': 351,
                         'OTHERS': {-9: 'MISSING', -7: 'NOT_INTERV', -6: 'MUL_RESP'},
                         'VALS': {-9: 'MISSING', -7: 'NOT_INTERV', -6: 'MUL_RESP',
                                  0: 'NO', 1: 'YES'}}

            # How much likes school
            self.likes_s = {'COL': 'LIKES_S', 'TYPE': 'CATEGORICAL', 'STR': 428, 'END': 429,
                         'OTHERS': {-9: 'MISSING', -6: 'MUL_RESP',-1 : 'DONT_K'},
                         'VALS': {-9: 'MISSING', -6: 'MUL_RESP', -1 : 'DONT_K',
                                  1: 'NO', 2: 'SOME', 3: 'YES'}}

            # Use of school library for assignments
            self.library = {'COL': 'LIBRARY', 'TYPE': 'CATEGORICAL', 'STR': 708, 'END': 709,
                            'OTHERS': {-9: 'MISSING', -7: 'NOT_INTERV', -6: 'MUL_RESP',
                                       -3: 'SKIP_ANS'},
                            'VALS': {-9: 'MISSING', -6: 'MUL_RESP', -1: 'DONT_K',
                                     1: 'NEVER', 2: 'RARELY', 3: 'SOMET', 4: 'OFTEN'}}