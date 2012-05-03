#Generates a CSV file from the data (based on the desired features)

from stage import *
import math

class OutputCSV_YearTopics(Stage):
    def __init__(self,name):
        Stage.__init__(self,name,'YearLayer')

    def pre_process(self,db,rep):
        filename = 'year_topics_'+str(int(rep['Global']['num_topics']))+'topics.txt';
        self.f = open(filename, 'w')
        self.f.write('year')
        num_topics = float(rep['Global']['num_topics'])
        for i in range(0,int(num_topics)):
            self.f.write(','+str(i))
        self.f.write('\n')
        for year in sorted(rep['YearLayer'].keys()):
            self.f.write(str(int(year)+2000))
            for val in rep['YearLayer'][year]['TopicDistribution']:
                self.f.write(','+str(val))
            self.f.write('\n')

    def post_process(self,db,rep):
        self.f.close()
            

        
