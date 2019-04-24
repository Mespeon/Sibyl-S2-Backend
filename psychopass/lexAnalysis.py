"""
Original Author: Stephen W. Thomas

Perform sentiment analysis using the MPQA lexicon.
Note, in this simple approach, we don't do anything to handle negations
or any of the other hard problems.

Adjusted for Sibyl use by: Mark Nolledo
- added manual input to accept form-based inputs
- to be adjusted for aggregated analysis mode

Sourced from: Github
"""
import os
# The NLTK heavy guns
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# For reading input files in CSV format
import csv

# For doing cool regular expressions
import re

# For sorting dictionaries
import operator
import string
from array import *

# Initialize stopwords
stops = set(stopwords.words('english'))

# Locate the dataset
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dataset =  os.path.join(BASE_DIR, 'lexicon_easy.csv')

class LexiconAnalysis():
    def returnMessage(inputComment):
        return inputComment

    def beginLexAnalysis(inputComment):
        # Intialize an empty list to hold all of our tweets
        comments = []
        negativeLex = []
        positiveLex = []

        # A helper function that removes all the non ASCII characters
        # from the given string. Retuns a string with only ASCII characters.
        def strip_non_ascii(string):
            ''' Returns the string without non ASCII characters'''
            stripped = (c for c in string if 0 < ord(c) < 127)
            return ''.join(stripped)

        # Create a data structure to hold the lexicon.
        # We will use a Python dictionary. The key of the dictionary will be the word
        # and the value will be the word's score.
        lexicon = dict()

        # Read in the lexicon.
        with open(dataset, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                lexicon[row[0]] = int(row[1])

        # Use lexicon to score comments
        comment = dict()
        # Remove punctuation marks
        comment['orig'] = inputComment
        comment['orig'] = comment['orig'].translate(str.maketrans('', '', string.punctuation))

        # Remove all non-ascii characters
        comment['clean'] = comment['orig']
        comment['clean'] = strip_non_ascii(comment['clean'])
        comment['clean'] = comment['clean'].lower()

        # Append this comment to the dictionary
        comments.append(comment)

        for c in comments:
            #print(c)
            score = 0
            for word in c['clean'].split():
                if word in lexicon:
                    score += lexicon[word]
                    #print('Found in lexicon: %s \t\t Current score: %5d' % (word, score))
                    #print('Word value: %s' % lexicon[word])
                    if lexicon[word] > 0:
                        positiveLex.append(word)
                    elif lexicon[word] < 0:
                        negativeLex.append(word)

            c['score'] = score
            if (score > 0):
                c['sentiment'] = 'positive'
            elif (score < 0):
                c['sentiment'] = 'negative'
            else:
                c['sentiment'] = 'neutral'

        # Print out summary stats
        resultText = ''
        total = float(len(comments))
        num_pos = sum([1 for c in comments if c['sentiment'] == 'positive'])
        num_neg = sum([1 for c in comments if c['sentiment'] == 'negative'])
        num_neu = sum([1 for c in comments if c['sentiment'] == 'neutral'])
        #print('Comments retrieved: %5d' % total)
        #print("Positive: %5d (%.1f%%)" % (num_pos, 100.0 * (num_pos/total)))
        #print("Negative: %5d (%.1f%%)" % (num_neg, 100.0 * (num_neg/total)))
        #print("Neutral:  %5d (%.1f%%)" % (num_neu, 100.0 * (num_neu/total)))
        if num_pos > num_neg:
            resultText = 'The phrase showed a positive polarity.'
        elif num_neg > num_pos:
            resultText = 'The phrase showed a negative polarity.'
        elif num_pos == num_neg or num_neu > (num_pos + num_neg):
            resultText = 'The phrase is neutral.'

        return [num_pos, num_neg, num_neu, resultText, positiveLex, negativeLex]
