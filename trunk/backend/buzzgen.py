#!/usr/bin/python
from random import choice

adj = open('adjectives.txt','r').readlines()
adv = open('adverbs.txt','r').readlines()
nouns = open('nouns.txt','r').readlines()
verbs = open('verbs.txt','r').readlines()

def sc(wordlist):
    return strip(choice(wordlist))

print ' '.join([choice(adv), choice(verbs), choice(adj), choice(nouns)])
