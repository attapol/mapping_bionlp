#Gets the TF-IDF scores for every item int he vocabulary

from stage import *
import math

class TFIDF(Stage):
    def __init__(self,name):
        Stage.__init__(self,name,'DocVocabLayer','TF-IDF')

    def pre_process(self,db,rep):
        self.total_docs = float(len(rep['DocLayer']))
        
    def process(self,key,features,db,rep):
        tf = rep['DocVocabLayer'].get(key,'TF')
        doc_freq = rep['VocabLayer'].get(key[1],'DocFreq')
        idf = math.log(self.total_docs/doc_freq,10)**2
        return tf*idf
        

        
