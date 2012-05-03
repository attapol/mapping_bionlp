from representation import *
import nltk, string, re
from nltk.corpus import stopwords
from collections import Counter, defaultdict

class BigramCountLayer(RepresentationLayer):
    def create(self,db,rep):
        punctuation = [p for p in string.punctuation]
        sw = stopwords.words('english')
        trailing_punct = re.compile('[%s]$' % re.escape(string.punctuation))
        results = db.execute('SELECT ID From Papers')
        total_bigrams = defaultdict(int)
        for r in results:
            doc = nltk.word_tokenize(get_doc_contents(r[0],db).lower())
            bigrams = [tuple([re.sub(trailing_punct, "", word) for word in doc[i:i+2]])
                        for i in range(len(doc)-1)
                       if not (doc[i] in sw or doc[i+1] in sw or
                               doc[i] in punctuation or doc[i+1] in punctuation)]
            counts = Counter(bigrams)
            for key in counts.iterkeys():
                total_bigrams[key] += counts[key]
        for (bigram,count) in total_bigrams.iteritems():
                self.set(bigram,'BigramCount',count)
