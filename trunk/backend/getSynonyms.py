#!/usr/bin/python

# Contact dictionaryapi.com and find synonyms for a word

import urllib2
from xml.dom import minidom
import string

codeToTense = {     \
    'NN':'noun',    \
    'JJ':'adjective',\
    'RB':'adverb',  \
    'VB':'verb'     \
}

def formURL(word):
    """Build a URL to attach to dictionaryapi.com"""
    keyFile = open("data/.keys.txt").readlines()
    key = ""
    for line in keyFile:
        tup = line.split('=')
        if tup[0] == "dictionaryapi":
            key = tup[1]
            break
    # Make sure we found something
    if key == "":
        return -1
    #print "http://www.dictionaryapi.com/api/v1/references/thesaurus/xml/"+word+"?key="+key
    return "http://www.dictionaryapi.com/api/v1/references/thesaurus/xml/"+word+"?key="+key

def findSynonym(word, tenseCode):
    """Find the synonym for a word"""
    url = formURL(word)
    xmlResult = minidom.parse(urllib2.urlopen(url))

    synonyms = []
    related = []

    for entry in xmlResult.getElementsByTagName('entry'):

        # To avoid cases where the word "live" returns results for "live wire" as well
        if entry.getAttribute("id") != word:
            continue

        # Make sure we are looking at the right tense to find a synonym
        tenseNode = entry.getElementsByTagName("fl")[0]
        tenseOfEntry = getText(tenseNode.childNodes)
        if tenseOfEntry != codeToTense[tenseCode]:
            continue
        
        # Examine each sense and find the list of synonyms
        allSenses = entry.getElementsByTagName('sens')
        for sense in allSenses:
            # Direct synonyms first
            synNode = sense.getElementsByTagName('syn')[0]
            synSet  = getText(synNode.childNodes)
            # Weirdly enough, this list is separated by comma at some places
            # and by a semi-colon at others
            for synSemiColon in synSet.split(','):
                if string.find(synSemiColon, ';') != -1:
                    for syn in synSemiColon.split(';'):
                        synonyms.append(string.strip(syn))
                else:
                    synonyms.append(string.strip(synSemiColon))

            # Related words next
            relNode = sense.getElementsByTagName('rel')[0]
            relSet  = getText(relNode.childNodes)
            # Weirdly enough, this list is separated by comma at some places
            # and by a semi-colon at others
            for relSemiColon in relSet.split(','):
                if string.find(relSemiColon, ';') != -1:
                    for rel in relSemiColon.split(';'):
                        related.append(string.strip(rel))
                else:
                    related.append(string.strip(relSemiColon))


    return (synonyms,related)


def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

if __name__ == "__main__":
    print findSynonym("music","JJ")
