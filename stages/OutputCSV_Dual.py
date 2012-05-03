#Generates a CSV file from the data (based on the desired features)

from stage import *
import math

class OutputCSV_Dual(Stage):
    def __init__(self,name):
        Stage.__init__(self,name,'DocLayer')
        self.f = open('dual.csv','w')

    def pre_process(self,db,rep):
        self.f.write('id')
        num_topics = float(rep['Global']['num_topics'])
        for i in range(0,int(num_topics)):
            self.f.write(','+str(i))
        self.vocab = []
        for key in rep['VocabLayer']:
            if int(rep['VocabLayer'][key]['DocFreq']) > 9:
                self.f.write(','+key)
                self.vocab.append(key)

    def process(self,key,features,db,rep):
        self.f.write('\n')
        self.f.write(key)
        for prob in rep['DocLayer'][key]['TopicDistribution']:
            self.f.write(','+str(prob))
        for v in self.vocab:
            if rep['DocVocabLayer'].has_key((key,v)):
                val = rep['DocVocabLayer'].get((key,v),'TF-IDF')
                self.f.write(','+str(val))
            else:
                self.f.write(',0')
            

        
