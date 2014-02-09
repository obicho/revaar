
import nltk, random, string
from nltk.collocations import *
from nltk.corpus.reader import CategorizedPlaintextCorpusReader 
from nltk.corpus import stopwords

bigram_measures = nltk.collocations.BigramAssocMeasures()
reader = CategorizedPlaintextCorpusReader('./', r'.*\.txt', cat_pattern=r'(\w+)/*')
print reader.categories()
print reader.fileids()

documents = [(list(reader.words(fileid)), category)
	for category in reader.categories()
	for fileid in reader.fileids(category)]
random.shuffle(documents)

# Remove stopwords & punc from content
table = string.maketrans("","")
stopwords = nltk.corpus.stopwords.words('english')
filtered_words = [w for w in reader.words() if not w in stopwords]
filtered_words_nopunc = [w for w in filtered_words if not w in string.punctuation]
#all_words = nltk.FreqDist(w.lower() for w in filtered_words_nopunc)
finder = BigramCollocationFinder.from_words(filtered_words_nopunc)
#scored = finder.score_ngrams(bigram_measures.raw_freq)
#a = sorted(bigram for bigram, score in scored) 
 	
finder.apply_freq_filter(3)
a = finder.nbest(bigram_measures.pmi, 50)  
print finder

