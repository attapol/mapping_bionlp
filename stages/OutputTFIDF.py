from stage import *
from parameters import *

class OutputTFIDF(Stage):
    def __init__(self,name):
        Stage.__init__(self,name,'DocVocabLayer','OutputTFIDF')

    def pre_process(self,db,rep):
        self.best_per_doc = dict()
        if not os.path.exists('tfidf'):
            os.mkdir('tfidf')

    def process(self,key,features,db,rep):
        if not key[0] in self.best_per_doc:
            self.best_per_doc[key[0]] = []
        self.best_per_doc[key[0]].append([key[1],features['TF-IDF']])

    def post_process(self,db,rep):
        for doc in self.best_per_doc:
            f = open('tfidf/'+doc+'.txt','w')
            best_keys = sorted(self.best_per_doc[doc],
                               key=lambda x:x[1],
                               reverse=True)[:get_required_int_param(
                                   'tfidf_output_top_k',rep)]
            f.write(rep['DocLayer'][doc]['Title']+'\n')
            f.write('\n'.join([str(k[1])[:5]+'\t'+k[0]
                               for k in best_keys]))
            f.close()
    

        
