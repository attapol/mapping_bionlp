from representation import *
import nltk, string,re 
from nltk.corpus import stopwords
from collections import Counter, defaultdict

class TrigramLayer(RepresentationLayer):
    def create(self,db,rep):
        punctuation = [p for p in string.punctuation]
        sw = stopwords.words('english')
        trailing_punct = re.compile('[%s]$' % re.escape(string.punctuation))
        results = db.execute('SELECT ID From Papers')
        for r in results:
            doc = nltk.word_tokenize(get_doc_contents(r[0],db).lower())
            trigrams = [tuple([re.sub(trailing_punct, "", word) for word in doc[i:i+3]])
                        for i in range(len(doc)-2)
                       if not (doc[i] in sw or doc[i+1] in sw or doc[i+2] in sw
                               or doc[i] in punctuation or doc[i+1] in punctuation
                               or doc[i+2] in punctuation)]
            for trigram in trigrams:
                self.add(trigram)
