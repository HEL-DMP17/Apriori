# Global modules here
import collections
import itertools
import time
# Internal modules here

"""
Add documentation about this class here
"""
class Apriori:
    def __init__(self, transactions, uniques, min_sup=2.0, min_conf=1.5):
        self.transactions = transactions
        self.transaction_count = transactions[-1]['ID'] # get the ID of the last element
        self.uniques = uniques
        self.min_sup = min_sup
        self.min_conf = min_conf
        self.itemsets_by_freq = {}
        self.freq_itemsets = []
        self.arules = []
        # Run the main algorithm
        self.apriori_run()

    def extract(self):
        # Check frequent itemset if contains valuable association rule
        # Append the rules greater than some measurements e.g. lift/confidence
        print('Frequent itemsets', self.freq_itemsets)
        # Go all over the freq_itemsets
        for dict_itemset in self.freq_itemsets:
            itemset = dict_itemset['ITEMS']
            freq = dict_itemset['FREQ']
            # Only need to do, one less length combinations group
            # Because previous groups are already extracted
            combs = list(itertools.combinations(itemset, len(itemset) - 1))
            for c in combs:
                left = list(c)
                right = self.diffelems(left, itemset)
                self._prntarule(left, right)
                # Symmetric rules must be checked too
                # self._prntarule(right, left)
                # TODO: We can use precalculated values in self.freq_itemsets and self.uniques
                # Calculate measures
                # conf = self.confidence(left, right)
                # lift = self.lift(left, right) # this is a symmetric measure no need to calculate twice
                # if conf > self.min_conf:
                # Add into arules list if greater than some value
                # rule = {'LEFT': left, 'RIGHT': right, 'CONF': conf, 'LIFT': lift}
                # rule_sym = {'LEFT': right, 'RIGHT': left, 'CONF': conf_sym, 'LIFT': lift}
                # self.arules.append(rule)
                # self.arules.append(rule_sym)

        # Return association rules
        return self.arules

    def _prntarule(self, left, right):
        """
        Helper utility for rules
        :param left: left handside rule (list)
        :param right: right handside rule (list)
        :return:
        """
        if left == [] or right == []:
            raise Exception("Rules cannot be empty - apriori::_prntarule")
        print("{}  -->  {}".format(left, right))

    def diffelems(self, list1, list2):
        """
        Extracts the difference elements in lists, symmetrically.
         For example:
            list1 = ['a','b','c'], list2 = ['b','c']
            diffelems(list1, list2)
            # regardless of order it will return same result
            returns ->  ['a']

        :param list1: First list to be compared
        :param list2: Second list to be compared
        :return: The difference elements of first and second lists
        """
        return list(set(list1).symmetric_difference(set(list2)))

    def support_count(self, itemset):
        """
        Computes the support count of the itemset
        :param itemset: itemset to be counted (list)
        :return: support count of the itemset (int)
        """
        # TODO: implement support_count measure
        return 1

    def support(self, itemset, itemset_precalculated = None):
        """
        Returns
        :param itemset: itemset (list)
        :param itemset_precalculated: Existing suppport count value
        :return: support of the itemset (float)
        """
        if itemset_precalculated is not None:
            sup_count = itemset_precalculated
        else:
            sup_count = self.support_count(itemset)
        # Calculate support
        support = sup_count / self.transaction_count

        return support

    def confidence(self, left, right, left_precalculated = None):
        """
        Calculates the confidence of the rule
        :param left: left handside of the rule (list)
        :param right: right handside of the rule (list)
        :param left_precalculated: Existing suppport count value
        :return: Confidence value (float)
        """
        print('Calculate the confidence of the eft and the right handside of the rules')
        if left_precalculated is not None:
            conf = self.support_count(left + right) / left_precalculated
        else:
            conf = self.support_count(left + right) / self.support_count(left)

        return conf

    def lift(self, left, right, right_precalculated = None):
        """
        Calculates the confidence of the rule
        :param left: left handside of the rule (list)
        :param right: right handside of the rule (list)
        :param right_precalculated: Existing suppport count value
        :return: Confidence value (float)
        """
        print('Calculate the lift of the left and the right handside of the rules')

        if right_precalculated  is not None:
            sup_right = self.support(right, itemset_precalculated = right_precalculated)
        else:
            sup_right = self.support(right)
        # Calculate lift
        lift = self.conf(left, right) / sup_right

        return lift

    def freq1_itemsets(self, f1itemsets):
        """
        Extracts the 1 length frequent itemsets

        :param f1itemsets: 1-length frequent itemsets (dict)
        :return: 1-length frequent itemsets (list) greater that self.min_sup
        """
        f1itemsets = {k: v for k, v in f1itemsets.items() if v >= self.min_sup}
        f1itemsets = list(collections.OrderedDict(sorted(f1itemsets.items())))
        itemsets=[]
        for candidates in f1itemsets:
            itemsets.append([candidates])
        return(itemsets)

    def apriori_gen(self, Fk, k):
        """
            Used to generate size k candidates based on the frequent itemsets Fk
            :param Fk list of k-1 itemsets, k:number of items that should have the new itemsets
            :return: new_candidates: list of size k-itemsets,
            """
        #print('-------Generating candidate itemsets')
        new_candidates=[]
        for i in range(len(Fk)-1):
            for j in range(i+1,len(Fk)):
                if  Fk[i][0:len(Fk[i])-k]==Fk[j][0:len(Fk[j])-k]:
                    Fk1=sorted(list(set(Fk[i]).union(Fk[j])))
                    new_candidates.append(Fk1)
        #print('-------out of Generating candidate itemsets')
        return(new_candidates)

    def apriori_run(self):
        """
        Main frequent itemset generation algorithm - Apriori.
        Returns all frequent itemsets.
        :return: Frequent itemsets (dict)
        """
        print("Apriori algorithm initiated")
        start_t = time.clock()
        k = 1
        fid = 0 # Unique frequent itemset id
        # All 1-itemsets
        Fk = self.uniques
        # Find all frequent 1-itemsets
        Fk = self.freq1_itemsets(Fk)
        # Until no more Frequent itemset is generated
        while len(Fk) > 0:
            k += 1
            # Generate candidate itemsets
            Ck = self.apriori_gen(Fk, k)
            Fk=[]
            Fk_full=[]
            #print('Ck:', len(Ck) ,Ck[0])
            for transaction in self.transactions:
                for candidate in Ck:
                    #print('cand',candidate)
                    subc=set(candidate)
                    subt=set(list(transaction['ITEMS']))
                    if subc.issubset(subt):
                        Fk_full.append(str(candidate))
            # Counting all itemsets
            count_itemsets = collections.Counter(Fk_full)
            #print('count',count_itemsets.keys())
            for item in count_itemsets.items():
                # Select just the frequent itemsets
                if item[1] >= self.min_sup:
                    # Clear the items from the string format
                    set_s = [i.replace("['","").replace(",","").replace("']","").replace("'","") for i in item[0].split()]
                    Fk.append(set_s)
                    # Save frequent itemset
                    fid += 1
                    t = {'ID': fid, 'FREQ': item[1], 'ITEMS': set_s}
                    self.freq_itemsets.append(t)
            # Sorting list to apply Fk-1 next candidates generation
            Fk.sort()
            # Print Fk
            # print('Frequent itemsets size',k,":",len(Fk))
            # for i in Fk:
            #     print(i)
        # Performance measurements
        total_t = str(format(time.clock() - start_t, '.4f'))
        print("Apriori took {:>10} seconds"
                  .format(total_t))
        # Return frequent itemsets
        return(self.freq_itemsets)

    def save_freqis(self, path = "../frequent_itemsets.csv"):
        """
        Save the frequent itemsets into a file
        :param path: Path to be saved
        :return: Returns true on successful save
        """
        print('Saving the frequent itemsets into {}'.format(path))
        start_t = time.clock()
        with open(path, 'w') as f:
            f.write("ID,FREQUENCY,ITEMS\n")
            for t in self.transactions:
                print_str = str(t['ID']) + ',' + str(t['FREQ'])
                for i in t['ITEMS'].keys():
                    print_str += "," + i
                print_str += "\n"
                f.write(print_str)
        # Performance measurements
        total_t = str(format(time.clock() - start_t, '.4f'))
        print("Save procedure took {:>10} seconds"
              .format(total_t))
        return True

    def save_rules(self, path="../arules.csv"):
        """
        Saves the association rules into a file
        :param path: Path to be saved
        :return: Returns true on successful action
        """
        # TODO: Add a proper saver for the association rules
        print('Rules saved to {}'.format(path))
        return True

    def _print_freq_is(self):
        """
        Helper function to print frequent itemsets
        :return:
        """
        print_str = "ID,FREQUENCY,ITEMS\n"
        for t in self.freq_itemsets:
            print_str += str(t['ID']) + ',' + str(t['FREQ'])
            for i in t['ITEMS']:
                print_str += "," + i
            print_str += "\n"
        print(print_str)
