from stage import *
from parameters import *
from collections import *

class DocTopicDistributions(Stage):
    def __init__(self,name):
        Stage.__init__(self,name,'DocLayer','TopicDistribution')
    """    
    def process(self,key,features,db,rep):
        #collect counts for all the topics in the document
        counts = defaultdict(int)
        total_count = 0.0
        for k in rep['TokenLayer']:
            if k[0] == key:
                if 'Topic' in rep['TokenLayer'][k]:
                    counts[rep['TokenLayer'].get(k,'Topic')] += 1
                    total_count += 1.0
        num_topics = get_required_int_param('num_topics',rep)
        if total_count == 0:
            print 'Error: 0 topic count while getting distribution for '+\
                  'document '+str(key)
            return [0.0]*num_topics 
        else:
            return [float(counts[t])/total_count for t in range(num_topics)]
    """

    def pre_process(self,db,rep):
        self.doc_topics = dict()
        self.num_topics = get_required_int_param('num_topics',rep)
        f = open('doc_topics.txt','r')
        f.readline()
        for l in f:
            parts = l[:-1].split('\t')
            doc = parts[1].split('/')[-1]
            if not doc in self.doc_topics:
                self.doc_topics[doc] = defaultdict(float)
            for i in range(2,len(parts)-1,2):
                topic = int(parts[i])
                val = float(parts[i+1])
                self.doc_topics[doc][topic] = val

    def process(self,key,features,db,rep):
        return [self.doc_topics[key][i] for i in range(self.num_topics)]

        
