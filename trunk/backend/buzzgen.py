#!/usr/bin/python
from random import choice, shuffle
from string import strip
import getSynonyms
import posTagger

adj = open('data/adjectives.txt','r').readlines()
adv = open('data/adverbs.txt','r').readlines()
nouns = open('data/nouns.txt','r').readlines()
verbs = open('data/verbs.txt','r').readlines()

def sc(wordlist):
    word = choice(wordlist)
    return strip(word.split('\n')[0])

def buzzify(sentence):
    # Given a sentence, first find all the part of speech tags of words
    wordsWithStems = posTagger.getWordsWithStems (sentence) # w t s = (word,tense,stem)
    sentSynonyms = []
    for wts in wordsWithStems:
        tagOfInterest = wts[1][:2]
        word = wts[0]
        # Find the synonyms of all words that can be potentially modified
        if tagOfInterest in ['NN', 'JJ', 'VB', 'RB']:
            print "tagOfInterest", tagOfInterest, "in", word
            synonymsAndRelated = getSynonyms.findSynonym(word, tagOfInterest)
            print synonymsAndRelated
            sentSynonyms.append((wts,synonymsAndRelated))
        else:
            sentSynonyms.append((wts, ([], [])))
            print "Skipping", word

    # At this time, sentSynonyms contains a list of words from 
    # the sentence in their orignial order in the following format:
    # [list of ((word, tense, stem), ([list of synonyms], [list of related words])) ]

    # Now we must compare the list of synonyms with all the possible buzzwords
    # of that tense, and pick one from the resulting list at random
    #previousWordsTense = ''
    #finalSentence = []
    #for structure in sentSynonyms:
    return str(sentSynonyms)
        


print buzzify ("A beautiful day beckons outside")
