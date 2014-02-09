import nltk
text = nltk.word_tokenize("And now for something completely different")
b=nltk.pos_tag(text)
print b