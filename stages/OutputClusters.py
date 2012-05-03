from stage import *
from parameters import *

class OutputClusters(Stage):
    def __init__(self,name):
        Stage.__init__(self,name,'DocLayer','OutputClusters')

    def pre_process(self,db,rep):
        self.best_per_clust = dict()
        self.docs_per_clust = dict()
        if not os.path.exists('clusters'):
            os.mkdir('clusters')

    def process(self,key,features,db,rep):
        clust = rep['DocLayer'][key]['Cluster']
        if not clust in self.docs_per_clust:
            self.docs_per_clust[clust] = []
        self.docs_per_clust[clust].append(key)
        
        if os.path.exists('tfidf/'+key+'.txt'):
            f = open('tfidf/'+key+'.txt')
            f.readline()
            for line in f:
                l = line.split()
                score = float(l[0])
                word = l[1]
                if not clust in self.best_per_clust:
                    self.best_per_clust[clust] = {}
                if (not word in self.best_per_clust[clust] or score >
                    self.best_per_clust[clust][word]):
                    self.best_per_clust[clust][word] = score

    def post_process(self,db,rep):
        cluster_words = dict()
        for clust in self.best_per_clust:
            cluster_words[clust] = []
            for word in self.best_per_clust[clust]:
                cluster_words[clust].append((word,self.best_per_clust[clust][word]))
        for clust in cluster_words:
            f = open('clusters/cluster_'+str(clust)+'.txt','w')
            for doc in self.docs_per_clust[clust]:
                f.write(doc+': '+rep['DocLayer'][doc]['Title']+'\n')
            f.write('\n')
            best_keys = sorted(cluster_words[clust],
                               key=lambda x:x[1],
                               reverse=True)[:get_required_int_param(
                                   'tfidf_output_top_k',rep)]
            f.write('\n'.join([str(k[1])[:5]+'\t'+k[0]
                               for k in best_keys]))
            f.close()
    

        
