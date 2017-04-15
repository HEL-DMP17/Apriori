# This is the stub for our main Apriori algorithm

"""
This is a apriori class
"""

class Apriori:
    def __init__(self, data=None, sup=None, conf=None):
        self.data = data
        self.sup = sup
        self.conf= conf
        self.candidates = {}
        #self._print("This is a stub for our Apriori class")
        print('Data',data)
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

    def generate_new_candidates(self):
        print('Pruning and generating new candidates')

    def compute_support(self):
        print('Computing itemsets support')

    def prune(self):
        print('Pruning itemsets lower than support threshold', self.sup)

    def compute_confidence(self):
        print('Computing itemsets support')

    def get_itemsets(self,size):
        print('Getting itemsets of size x', size)
        return(size)

    def apriori_exe(self):
        print('Implementing Apriori algorithm')
        print(self.data.get_transactions())
        self.data._print_transactions()
        size=2
        while self.candidates:
            self.candidates=Apriori.generate_new_candidates(self.candidates, size)
            self.Apriori.compute_support()
            self.candidates=Apriori.prune()
            size+=1
        return(Apriori.get_itemsets(self, size-1))
