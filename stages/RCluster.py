from stage import *
from parameters import *
import gzip

class RCluster(Stage):
    def __init__(self,name):
        Stage.__init__(self,name,'DocLayer')

    def pre_process(self,db,rep):
        shell_command('RScript hier_clust.R' + ' ' +\
                      get_required_param('csv_to_cluster',rep) + ' ' +\
                      get_required_param('cluster_out_file',rep) + ' ' +\
                      str(get_required_param('num_clusters',rep)))
            
        
