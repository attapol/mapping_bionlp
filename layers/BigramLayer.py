from representation import *
import nltk, string, re
from nltk.corpus import stopwords
from collections import Counter

class BigramLayer(RepresentationLayer):
    def create(self,db,rep):
        punctuation = [p for p in string.punctuation]
        sw = stopwords.words('english')
        trailing_punct = re.compile('[%s]$' % re.escape(string.punctuation))
        results = db.execute('SELECT ID From Papers')
        for r in results:
            doc = nltk.word_tokenize(get_doc_contents(r[0],db).lower())
            bigrams = [tuple([re.sub(trailing_punct, "", word) for word in doc[i:i+2]])
                        for i in range(len(doc)-1)
                       if not (doc[i] in sw or doc[i+1] in sw
                               or doc[i] in punctuation or doc[i+1] in punctuation)]
            for bigram in bigrams:
                self.add(bigram)
