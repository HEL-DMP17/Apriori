# This is the stub for our main Apriori algorithm
import collections
from collections import Counter
import itertools
from operator import itemgetter
"""
This is a apriori class
"""

class Apriori:
    def __init__(self, transactions, uniques, min_sup=1.2, min_conf=1.5):
        self.transactions = transactions
        self.uniques = uniques
        self.min_sup = min_sup
        self.min_conf = min_conf
        self.itemsetsByFrec={}
        self.itemsetsBySize={}
        self.fitemsets =[]
        self._print("This is a stub for our Apriori class")
        self.apriori_exe()
        print('Frequent itemsets organized by frequency',self.itemsetsByFrec)
        print('Frequent itemsets organized by size', self.itemsetsBySize)

    def _print(self, msg):
       print(msg)

    def extract(self):
        """
        Some methd to test out this
        :param some_arg: Some not serious argument
        :return:
        """
        #print("Extract the frequent patterns")

    def compute_confidence(self):
        print('Computing itemsets support')

    def f1_itemsets(self, f1itemsets):
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

    def apriori_exe(self):
        """
            Used to perform apriori algorithm
            :return: self.fitemsets: full set of frequent itemsets with different k-size
            """
        k = 1
        Fk = self.uniques                   #All 1-itemsets
        Fk = Apriori.f1_itemsets(self, Fk)  #Find all frequent 1-itemsets
        #print('Fk0:', len(Fk), Fk)
        while len(Fk) > 0:                 #Until Fk: frequent items more than 0
            k += 1
            Ck = Apriori.apriori_gen(self, Fk, k) #Generate candidate itemsets
            Fk=[]
            Fk_full=[]
            #print('Ck:', len(Ck) ,Ck[0])
            for transaction in self.transactions:
                for candidate in Ck:
                    #print('cand',candidate)
                    subc=set(candidate)
                    # TODO: Debug line 82 "random" running error.
                    subt=set(list(list(transaction.items())[0][1]))
                    if subc.issubset(subt):
                        Fk_full.append(str(candidate))
            count_itemsets = Counter(Fk_full)   #Counting all itemsets
            #print('count',count_itemsets.keys())
            for item in count_itemsets.items():
                if item[1]>=self.min_sup:       #Select just the frequent itemsets
                    set_s=[]
                    item_s = item[0].split()
                    for i in item_s:
                        set_s.append(i.replace("['","").replace(",","").replace("']","").replace("'",""))
                    Fk.append(set_s)
                    if not item[1]  in self.itemsetsByFrec:     #Saving into itemset by frequency dicctionary
                        self.itemsetsByFrec[item[1]] = [set_s]
                    else:
                        self.itemsetsByFrec[item[1]].append([set_s])
            Fk.sort()                   #Sorting list to apply Fk-1 next candidates generation
            self.itemsetsBySize[k]=[Fk] #Saving into itemset by size dicctionary
            print('Frequent itemsets size',k,":",len(Fk))
            for i in Fk:
                print(i)
            self.fitemsets.append(Apriori.f_itemsets(k,Fk)) #Saving into self.datastructure, this step could be not neccessary
        return(self.fitemsets)

    class f_itemsets:
            def __init__(self,size,items):
                self.size=size
                self.items=items