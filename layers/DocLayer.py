from representation import *

def prep(string):
    return string.replace(',',' and ').replace('\n',' and ')

class DocLayer(RepresentationLayer):    
    def create(self,db,rep):
        results = db.execute('SELECT ID, GROUPID, TITLE, AUTHORS, PLACES From Papers' )
        for r in results:
            self.set(r[0],'Title',r[2])
            self.set(r[0],'Authors',prep(r[3]))
            self.set(r[0],'Places',prep(r[4]))
            self.set(r[0],'Year-ID',r[1][1:3])
