from stage import *

class DocLength(Stage):
    def __init__(self,name):
        Stage.__init__(self,name,'DocLayer','Length')

    def process(self,key,features,db,rep):
        result = db.execute('SELECT CONTENT FROM Papers WHERE ID=?',[key])
        data = result.fetchone()
        if data != None and data[0] != None:
            return len(data[0])
        else:
            return 0
        
