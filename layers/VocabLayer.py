from representation import *
import nltk

class VocabLayer(RepresentationLayer):
    def create(self,db,rep):
        results = db.execute('SELECT ID From Papers')
        for r in results:
            #go through the tokens and add them as vocab elements
            for word in nltk.word_tokenize(get_doc_contents(r[0],db)):
                self.add(word)
