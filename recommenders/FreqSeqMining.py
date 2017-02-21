from recommenders.ISeqRecommender import ISeqRecommender
from pymining import seqmining
from tree.Tree import SmartTree
import logging


class FreqSeqMiningRecommender(ISeqRecommender):
    """Frequent sequence mining recommender"""

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    def __init__(self,minsup,minconf,verbose=False):
        """minsup is interpreted as percetage if [0-1] or as count if > 1 """

        super(FreqSeqMiningRecommender, self).__init__()
        logging.basicConfig(level=logging.DEBUG) if verbose else logging.basicConfig(level=logging.WARNING)
        self.minsup = minsup
        self.minconf = minconf

    def fit(self,seqs):
        """Takes a list of list of seqeunces ."""

        msup = self.minsup * len(seqs) if 0 <= self.minsup <=1 else self.minsup

        logging.debug('Mining frequent sequences')
        self.freq_seqs = seqmining.freq_seq_enum(seqs, msup)
        logging.debug('{} frequent sequences found'.format(len(self.freq_seqs)))

        logging.debug('Building frequent sequence tree')
        self.tree = SmartTree()
        self.rootNode = self.tree.set_root()
        for tuple in self.freq_seqs:
            if len(tuple[0]) == 1:
                #add node to root
                self.tree.create_node(tuple[0][0],parent=self.rootNode,data={"support":tuple[1]})
            elif len(tuple[0]) > 1:
                #add entire path starting from root
                self.tree.add_path((self.rootNode,) + tuple[0],tuple[1],self.rootNode)
            else:
                raise NameError('Frequent sequence of length 0')
        logging.debug('Tree completed')


    def get_freq_seqs(self):
        return self.freq_seqs

    def get_sequence_tree(self):
        return self.tree

    def show_tree(self):
        self.tree.show()