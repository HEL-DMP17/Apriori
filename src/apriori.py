# This is the stub for our main Apriori algorithm
import collections
import itertools
"""
This is a apriori class
"""

class Apriori:
    def __init__(self, transactions, uniques, min_sup=1.2, min_conf=1.5):
        self.transactions = transactions
        self.uniques = uniques
        self.min_sup = min_sup
        self.min_conf = min_conf
        self._print("This is a stub for our Apriori class")
        self.apriori_exe()

    def _print(self, msg):
       print(msg)

    def extract(self):
        """
        Some methd to test out this
        :param some_arg: Some not serious argument
        :return:
        """
        print("Extract the frequent patterns")

    def compute_support(self):
        print('Computing itemsets support')

    def compute_confidence(self):
        print('Computing itemsets support')

    def prune(self, candidates):
        candidates = {k: v for k, v in candidates.items() if v > self.min_sup}
        return (collections.OrderedDict(sorted(candidates.items())))

    def get_itemsets(self,size):
        print('Getting itemsets of size x', size)
        return(size)

    def apriori_gen(self, Fk, k):
        print('-------Generating candidate itemsets')
        list_Fk=list(Fk.keys())
        print(list_Fk)
        for F in list_Fk:
            print(F)
            for Fc in list_Fk:
                print(F,Fc)
        print('-------out of Generating candidate itemsets')
        return(1)

    def apriori_exe(self):
        k=1
        Fk=self.uniques               #Find all frequent 1-itemsets
        Fk = Apriori.prune(self, Fk)  #Find all frequent 1-itemsets
        #print ('Fk:', Fk)

        '''while len(Fk) > 0:
            k+=1
            Ck = Apriori.apriori_gen(self, Fk, k) # Generate candidate itemsets
            print('Ck',Ck)
            for transaction in self.transactions:
                    Ct = subset(Ck,t)
            Fk = Apriori.prune(self, Fk)'''

        '''print('I0 keys',self.transactions[1].values())
        print('Pruning itemsets lower than support threshold', self.min_sup)
        dicc={}
        print('Before pruning #of uniques', len(self.uniques))
        self.uniques = self.prune(self.uniques)
        print('After pruning #of uniques',len(self.uniques))
        k=5
        l=list(itertools.combinations(list(self.uniques.keys()), k))
        d = dict(itertools.zip_longest(*[iter(l)] * 2, fillvalue=""))
        print('d Keys',len(d.keys()))
        print('d Keys', d.keys())
        #print('I0 keys',self.transactions[1])'''


        '''print('Implementing Apriori algorithm')
        size=2
        while self.candidates:
            self.candidates=Apriori.generate_new_candidates(self.candidates, size)
            self.Apriori.compute_support()
            self.candidates=Apriori.prune()
            size+=1'''
        return(Apriori.get_itemsets(self, k))
