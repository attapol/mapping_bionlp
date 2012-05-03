from representation import *
import nltk

class TokenLayer(RepresentationLayer):
    def create(self,db,rep):
        results = db.execute('SELECT ID From Papers')
        for r in results:
            #go through the tokens and add them as the Token feature
            count = 0
            for word in nltk.word_tokenize(get_doc_contents(r[0],db)):
                self.set((r[0],count),'Token',word)
                count += 1
