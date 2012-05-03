#Generates a CSV file from the data (based on the desired features)

from stage import *
import math

class OutputCSV_Topics(Stage):
    def __init__(self,name):
        Stage.__init__(self,name,'DocLayer')

    def pre_process(self,db,rep):
        self.f = open('doc_'+str(int(rep['Global']['num_topics']))+'topics.csv','w')
        self.f.write('id\tTitle\tAuthors\tPlaces')
        num_topics = float(rep['Global']['num_topics'])
        for i in range(0,int(num_topics)):
            self.f.write('\ttopic'+str(i))

    def process(self,key,features,db,rep):
        self.f.write('\n')
        self.f.write(key)
        self.f.write('\t"'+rep['DocLayer'][key]['Title']+'"');
        self.f.write('\t"'+rep['DocLayer'][key]['Authors']+'"');
        self.f.write('\t"'+rep['DocLayer'][key]['Places']+'"');
        for prob in rep['DocLayer'][key]['TopicDistribution']:
            self.f.write('\t'+str(prob))
            
