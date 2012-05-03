from stage import *
from parameters import *
import gzip

class BasicLDA(Stage):
    def __init__(self,name):
        Stage.__init__(self,name,'DocLayer')

    def pre_process(self,db,rep):
        if not os.path.exists('LDA'):
            os.mkdir('LDA')

    def process(self,key,features,db,rep):
        #get all the tokens in the document
        k = [rep['TokenLayer'].get(k,'Token') for k in rep['TokenLayer']
             if k[0] == key]
        f = open('LDA/'+key,'w')
        f.write(' '.join(k))
        f.close()
        pass

    def load_topics(self,filename,rep):
        f = gzip.open(filename)
        #three not needed lines
        f.readline()
        f.readline()
        f.readline()
        for l in f:
            [doc,source,pos,typeindex,type_c,topic] = l[:-1].split()
            document = source[4:]
            rep['TokenLayer'].set((document,int(pos)),'Topic',int(topic))
        f.close()

    def post_process(self,db,rep):
        os.environ['MALLET_HOME'] = get_required_param('mallet_home',rep)
        if shell_command(get_required_param('mallet_bin',rep)+\
                         ' import-dir --input LDA '+\
                         '--output topic-input.mallet --remove-stopwords '+\
                         '--keep-sequence'):
            shell_command(get_required_param('mallet_bin',rep)+\
                         ' train-topics '+\
                         '--input topic-input.mallet '+\
                         '--num-topics '+\
                         str(get_required_int_param('num_topics',rep))+' '\
                         '--output-state topic_state.gz '+\
                         '--num-top-words 50 '+\
                         '--output-topic-keys topic_keys_'+\
						 str(get_required_int_param('num_topics',rep)) + 'topics.txt '+\
                         '--output-doc-topics doc_topics.txt '+\
                         '--optimize-interval '+\
                         str(get_required_int_param('optimize_interval',
                                                    rep))+' '+\
                         '--num-iterations '+\
                         str(get_required_int_param('num_iterations',rep)))
            print 'loading in topic results...'
            self.load_topics('topic_state.gz',rep)
            
        
