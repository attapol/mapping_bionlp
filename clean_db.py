import re, sqlite3, sys, nltk, string
from nltk.corpus import stopwords

def clean_db(db_location):
    con = sqlite3.connect(db_location)
    c=con.cursor()
    ids=[]
    x=c.execute("select ID from Papers")
    for i in x:
        ids.append(i[0])
    raw =c.execute("select CONTENT from Papers").fetchall()
    clean_content=[clean(t[0]) for t in raw]
    args = zip(clean_content,ids)
    c.executemany("update Papers set CLEAN_CONTENT=(?) where ID=(?)", args)
    con.commit()
    con.close()

def clean(text):
    #rejoin words split by line breaks
    text = re.sub("-[\\n,\\r]\d?\s?", "", text)
    lines=text.splitlines()
    #remove blanks and lowercase
    lines = [l.lower() for l in lines if len(l) > 5]
    #remove non-ascii characters
    lines = [''.join([x for x in l if ord(x) < 128]) for l in lines]

    #filter only abstract and main section
    content = lines
    #remove lines under 35 chars long unless they end with a period
    #and are at least 15 characters long
    #strip whitespace too
    content = [l.strip() for l in content if not (l.lower().startswith("table")
                                                  or l.lower().startswith("proceedings"))
               and (len(l) > 35
             or (len(l) > 15 and l.endswith("."))
                    or "##" in l
               or re.match(r"^\d\s+[A-Z]", l))]
    #remove trailing numbers (such as footnotes) and trailing punctuation
    punctuation = "".join([p for p in string.punctuation if p != "#"])
    trailing_punct = re.compile('[%s]$' % re.escape(punctuation))
    trailing_digit = re.compile(r'[0-9]$')
    content = [re.sub(trailing_punct, "", l) for l in content]
    content = [re.sub(trailing_digit, "", l) for l in content]
    words = [line.split() for line in content]
    #remove urls
    url_pat1 = re.compile(r"\s.*?/.*?\s")
    url_pat2 = re.compile(r".*?/.*?$")
    content = [re.sub(url_pat1, "", line) for line in content if not
               re.match(url_pat2, line)]
    #remove lines with mostly numbers or ones likely to be formulas
    filtered = []
    symbols = "( ) ^ + = < > - * / ? _ # .".split()
    for line in content:
        numbers = [x.isdigit() for x in line]
        symbol_count = [x in symbols for x in line]
        ratio_numbers = numbers.count(True)/float(len(line))
        ratio_symbols = symbol_count.count(True)/float(len(line))
        if ((not (ratio_numbers > 0.4 or ratio_symbols > 0.1
                or ratio_numbers+ratio_symbols > 0.25)) or
            line.startswith("##:")):
            filtered.append(line)
    words = [line.split() for line in filtered]
    cleaned_words=[]
    for i in xrange(len(words)):
        for j in xrange(len(words[i])):
            word  = words[i][j]
            numbers = [x.isdigit() for x in word]
            symbol_count = [x in symbols for x in word]
            ratio_numbers = numbers.count(True)/float(len(word))
            ratio_symbols = symbol_count.count(True)/float(len(word))
            if ((not (ratio_numbers > 0.2 or ratio_symbols > 0.2
                    or ratio_numbers+ratio_symbols > 0.1))
                or word.startswith("##:")):
                try:
                    cleaned_words[i].append(word)
                except IndexError:
                    cleaned_words.append([word])
    #remove stop words
    sw = stopwords.words('english')
    cleaned_words = [[w for w in sent if w not in sw] for sent in cleaned_words]
    cleaned_lines = [" ".join(w) for w in cleaned_words]
    #rejoin sections
    return "\n".join(cleaned_lines)

if __name__ == '__main__':
    filename = sys.argv[1];
    clean_db(filename);

