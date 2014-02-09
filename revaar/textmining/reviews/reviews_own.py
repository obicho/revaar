
import nltk, random, string
from nltk.corpus.reader import CategorizedPlaintextCorpusReader 
from nltk.corpus import stopwords

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
all_words = nltk.FreqDist(w.lower() for w in filtered_words_nopunc)

print all_words

word_features = all_words.keys()[:2000]




def document_features(document):
	document_words = set(document)
	features = {}
	for word in word_features:
		features['contains(%s)' % word] = (word in document_words)
	return features

featuresets = [(document_features(d), c) for (d,c) in documents]
print len(featuresets)

train_set, test_set = featuresets[25:], featuresets[:25]
classifier = nltk.NaiveBayesClassifier.train(train_set)

print nltk.classify.accuracy(classifier, test_set)

#print documents[50]

print 'classify ' + classifier.classify(document_features(documents[50][0]))
a = classifier.prob_classify(document_features(documents[50][0]))
print a.samples()
classifier.show_most_informative_features(5)
