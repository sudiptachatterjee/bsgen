#!/usr/bin/python
from random import choice, shuffle
from string import strip
import getSynonyms
import posTagger
from sets import Set
import operator
import cgi,json

adj = open('data/adjectives.txt','r').readlines()
adv = open('data/adverbs.txt','r').readlines()
nouns = open('data/nouns.txt','r').readlines()
verbs = open('data/verbs.txt','r').readlines()

def sc(wordlist):
    word = choice(wordlist)
    return strip(word.split('\n')[0])

def highestScorer(buzzwords, wordlist):
    """ Return a list of tuples (buzzword, score) sorted by score """
    # Very crude algorithm that just looks at the overlap between candidates
    # and uses that to assign a score, and then just picks the one within
    # the ones that have the highest score
    scoreboard = {}
    for buzz in buzzwords:
        b = set(buzz)
        scoreboard[buzz] = 0
        for word in wordlist:
            w = set(word)
            score = len(b & w)
            if score > scoreboard[buzz]:
                scoreboard[buzz] = score

    # If there are no matches at all
    # NOTE: a bug, possible
    # select a word at random from the wordlist, assign it a score of 0
    if len(scoreboard) == 0:
        return (sc(buzzwords), 0)

    # Return the highest scoring buzzword
    sorted_buzzwords = sorted(scoreboard.iteritems(), key=operator.itemgetter(1), reverse=True)
    highestScore = sorted_buzzwords[0][1]
    bestWords = []
    for i in sorted_buzzwords:
        if i[1] < highestScore:
            break
        else:
            bestWords.append(i[0])
    highestScoringWord = choice(bestWords).split('\n')[0]
    return (highestScoringWord, highestScore)



def pickABuzzword(synonyms, related, tense):
    """ From a set of synonyms and related words, 
    find the "closest" match among buzzwords of the same tense """
    
    buzzwords = []
    if tense == 'JJ':
        buzzwords = adj
    if tense == 'RB':
        buzzwords = adv
    if tense == 'NN':
        buzzwords = nouns
    if tense == 'VB':
        buzzwords = verbs

    # First preference is to find a word in the buzzwordlist
    # as close to any of the synonyms as possible
    syn = highestScorer(buzzwords, synonyms)
    rel = highestScorer(buzzwords, related)

    if syn[1] > rel[1]:
        return syn[0]
    else:
        return rel[0]
    



def buzzify(sentence):
    # Given a sentence, first find all the part of speech tags of words
    wordsWithStems = posTagger.getWordsWithStems (sentence) # w t s = (word,tense,stem)
    sentSynonyms = []
    for wts in wordsWithStems:
        tagOfInterest = wts[1][:2]
        word = wts[0]
        # Find the synonyms of all words that can be potentially modified
        if tagOfInterest in ['NN', 'JJ', 'VB', 'RB']:
            #print "tagOfInterest", tagOfInterest, "in", word
            synonymsAndRelated = getSynonyms.findSynonym(word, tagOfInterest)
            #print synonymsAndRelated
            sentSynonyms.append((wts,synonymsAndRelated))
        else:
            sentSynonyms.append((wts, ([], [])))
            #print "Skipping", word

    # At this time, sentSynonyms contains a list of words from 
    # the sentence in their orignial order in the following format:
    # [list of ((word, tense, stem), ([list of synonyms], [list of related words])) ]

    # Now we must compare the list of synonyms with all the possible buzzwords
    # of that tense, and pick one from the resulting list at random
    previousWordsTense = ''
    finalSentence = []
    for structure in sentSynonyms:
        # If there are no synonyms for this word,
        # just add it directly to the final sentence 
        word = structure[0][0]
        tense = structure[0][1]
        synonyms = structure[1][0]
        related = structure[1][1]
        if len(structure[1][0]) == 0:
            finalSentence.append(word)
            previousWordsTense = tense
            continue

        # Send the entire set of synonyms and related + tense to get a buzzword
        buzzword = pickABuzzword(synonyms, related, tense)

        # If this was a noun without an adjective before,
        # or a verb without an adverb before this, select a
        # qualifier at random from the lists
        if tense == 'NN' and previousWordsTense != 'JJ':
            adjective = sc(adj) # 'adj' is a global variable declared above
            finalSentence.append(adjective)
        if tense == 'VB' and previousWordsTense != 'RB':
            adverb = sc(adv) # 'adv' is a global variable declared above
            finalSentence.append(adverb)

        finalSentence.append(buzzword)

    # Finally, return the upgraded sentence
    return ' '.join(finalSentence)

#if __name__ == "__main__":
#    print buzzify("Hello my name is Sudipta")

if __name__ == "__main__":
    try:
        form = cgi.FieldStorage()
        sentence = form['sentence'].value
        buzz = buzzify(sentence)
        output = {"sentence": sentence, "buzzified": buzz}
        with open('buzzlog.log', 'a') as logFile:
            logFile.write(str(output)+'\n\n')
        print "Content-type: text/html\n\n"
        print json.dumps(output)
    except:
        print "Content-type: text/html\n\n"
        print json.dumps("No cookie for you tonight")
        

