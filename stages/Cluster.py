from stage import *
from parameters import *

class Cluster(Stage):
    def __init__(self,name):
        Stage.__init__(self,name,'DocLayer','Cluster')

    def pre_process(self,db,rep):
        self.clusters = []
        f = open(get_required_param('cluster_out_file',rep))
        for line in f.readlines():
            words = line.split()
            for w in words:
                self.clusters.append(w)

    def process(self,key,features,db,rep):
        result = self.clusters[0]
        self.clusters = self.clusters[1:]
        return result
        
