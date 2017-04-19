# Global modules here
import collections
import itertools

# Internal modules here

"""
Add documentation about this class here
"""
class Apriori:
    def __init__(self, transactions, uniques, min_sup=2, min_conf=1.5):
        self.transactions = transactions
        self.uniques = uniques
        self.min_sup = min_sup
        self.min_conf = min_conf
        self.itemsets_by_freq={}
        self.freq_itemsets =[]
        self.apriori_run()

    def extract(self):
        # Go all over the freq_itemsets
        # Check frequent itemset if contains valuable association rule
        # Append the rules greater than some measurements e.g. lift/confidence
        print('Extract method is called')
        print('Frequent itemsets', self.freq_itemsets)

    def diffelems(self, list1, list2):
        """
        Extracts the difference elements in lists, symmetrically.
         For example:
            list1 = ['a','b','c'], list2 = ['b','c']
            diffset(list1, list2)
            # regardless of order it will return same result
            returns ->  ['a']

        :param list1: First list to be compared
        :param list2: Second list to be compared
        :return: The difference elements of first and second lists
        """
        return list(set(list1).symmetric_difference(set(list2)))

    def save_rules(self, path):
        """
        Saves the association rules into a file
        :param path: Path to be saved
        :return: Returns true on successful action
        """
        print('Rules saved to {}'.format(path))

    def compute_confidence(self):
        print('Computing itemsets support')

    def freq1_itemsets(self, f1itemsets):
        f1itemsets = {k: v for k, v in f1itemsets.items() if v > self.min_sup}
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
                    t = {'ID': fid, 'FREQ': item[1], 'ITEMS': [set_s]}
                    self.freq_itemsets.append(t)
            # Sorting list to apply Fk-1 next candidates generation
            Fk.sort()
            # Print Fk
            # print('Frequent itemsets size',k,":",len(Fk))
            # for i in Fk:
            #     print(i)
        # Return frequent itemsets
        return(self.freq_itemsets)