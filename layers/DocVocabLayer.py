from representation import *
from collections import defaultdict
import nltk

class DocVocabLayer(RepresentationLayer):
    def create(self,db,rep):
        results = db.execute('SELECT ID From Papers')
        for r in results:
            word_counts = defaultdict(int)
            total_counts =0
            #gather all the unique vocab words from each document
            for word in nltk.word_tokenize(get_doc_contents(r[0],db)):
                word_counts[word] += 1
                total_counts += 1
            for key in word_counts:
                self.set((r[0],key),'TF',float(word_counts[key])/float(total_counts))
        
                
