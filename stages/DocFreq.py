#Counts how many documents each term in the vocabulary appears in and
#adds this to the VocabLayer as a feature

from stage import *
from collections import * 

class DocFreq(Stage):
    def __init__(self,name):
        Stage.__init__(self,name,'VocabLayer','DocFreq')

    def pre_process(self,db,rep):
        self.counts = defaultdict(int)
        for key in rep['DocVocabLayer']:
            self.counts[key[1]] += 1

    def process(self,key,features,db,rep):
        return self.counts[key]
