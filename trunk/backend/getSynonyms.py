#!/usr/bin/python

# Contact dictionaryapi.com and find synonyms for a word

import urllib2
from xml.dom import minidom

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

    print "http://www.dictionaryapi.com/api/v1/references/thesaurus/xml/"+word+"?key="+key
    return "http://www.dictionaryapi.com/api/v1/references/thesaurus/xml/"+word+"?key="+key

def findSynonym(word, tense):
    """Find the synonym for a word"""

    url = formURL(word)
    xmlResult = minidom.parse(urllib2.urlopen(url))
    for node in xmlResult.getElementsByTagName('syn'):
        print getText(node.childNodes)

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)



findSynonym("live","")
