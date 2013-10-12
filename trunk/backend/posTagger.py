#!/usr/bin/python

# Create part of speech tags from simple sentences

import nltk

def tagged(sentence):
    """ Tag each word in a sentence with a part of speech """
    tokens = nltk.word_tokenize(sentence)
    pos_tagged = nltk.pos_tag(tokens)
    return pos_tagged

wnl = nltk.stem.WordNetLemmatizer()
def findStem(word):
    """ Find the word stem """
    return wnl.lemmatize(word)

def getWordsWithStems(sentence):
    taggedWords = tagged(sentence)
    wordsWithStems = []
    for i in taggedWords:
        lemma = ''
        if i[1][:2] in ('NN', 'VB', 'JJ' 'RB'):
            # Those are the only tokens we are interested in
            lemma = findStem(i[0])
        else:
            lemma = i[0]
        wordsWithStems.append((i[0],i[1],lemma))
    return wordsWithStems


if __name__ == "__main__":
    print getWordsWithStems("The gardener reaping his dogs and churches")
