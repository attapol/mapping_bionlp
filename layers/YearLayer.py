from representation import *
from parameters import *

def average(lst):
    return sum(lst)/len(lst)

class YearLayer(RepresentationLayer):
    def create(self,db,rep):
        topic_dist = dict()
        for doc in rep['DocLayer']:
            year = rep['DocLayer'][doc]['Year-ID']
            if not year in topic_dist:
                topic_dist[year] = []
            topic_dist[year].append(rep['DocLayer'][doc]['TopicDistribution'])
        for year in topic_dist:
            topic_dist[year] = [average(
                [topic_dist[year][d][i] for d in range(len(topic_dist[year]))]) for
                i in range(get_required_int_param('num_topics',rep))]
            self.set(year,'TopicDistribution',topic_dist[year])
