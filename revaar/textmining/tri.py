import nltk
from nltk.corpus import brown
def process(sentence):
    for (w1,t1), (w2,t2), (w3,t3) in nltk.trigrams(sentence):
        if t2.startswith('RB') and t3.startswith('JJ'):
            print w1, w2, w3

#for tagged_sent in brown.tagged_sents():
#	process(tagged_sent)
sentence = """At eight o'clock on Thursday morning 
	Arthur is quite sleepy. He is happy. However, he was quite strong so he got up."""
tokens = nltk.word_tokenize(sentence)
tagged = nltk.pos_tag(tokens)
print tagged
process(tagged)