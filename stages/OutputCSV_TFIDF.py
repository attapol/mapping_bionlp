#Generates a CSV file from the data (based on the desired features)

from stage import *
import math

class OutputCSV_TFIDF(Stage):
    def __init__(self,name):
        Stage.__init__(self,name,'DocLayer')
        self.f = open('tfidf.csv','w')

    def pre_process(self,db,rep):
        self.f.write('id,Title')
        self.vocab = []
        for key in rep['VocabLayer']:
            if int(rep['VocabLayer'][key]['DocFreq']) > 9:
                self.f.write(','+key)
                self.vocab.append(key)

    def process(self,key,features,db,rep):
        self.f.write('\n')
        self.f.write(key)
        self.f.write(',"'+rep['DocLayer'][key]['Title']+'"');
        for v in self.vocab:
            if rep['DocVocabLayer'].has_key((key,v)):
                val = rep['DocVocabLayer'].get((key,v),'TF-IDF')
                self.f.write(','+str(val))
            else:
                self.f.write(',0')
            

        
