import nltk
import random
import pickle
import os

from nltk.tokenize import sent_tokenize, word_tokenize, PunktSentenceTokenizer
from nltk.classify.scikitlearn import SklearnClassifier
from nltk.classify import ClassifierI
from statistics import mode

# Locate the datasets
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
document_pickle =  os.path.join(BASE_DIR, 'documents/documents.pickle')
word_feature_pickle =  os.path.join(BASE_DIR, 'documents/word_features_5k.pickle')
featureset_pickle =  os.path.join(BASE_DIR, 'documents/featureset_1_7.pickle')
nbclassifier_pickle =  os.path.join(BASE_DIR, 'classifiers/sibyl-naive-bayes.pickle')

# Classifier Voter
class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            vote = c.classify(features)
            votes.append(vote)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            vote = c.classify(features)
            votes.append(vote)

        choice = votes.count(mode(votes))
        conf = choice / len(votes)
        return conf

def beginClassification(text):
    #Unpickle the document
    #Reset to 10K after testing with a 3K set
    #print('Opening dataset...')
    print('Beginning classification on requested text...')
    document_f = open(document_pickle, 'rb')
    documents = pickle.load(document_f)
    document_f.close()
    #print('Dataset opened.\n')

    #Unpickle word features
    #Reset to 10K after testing with a 3K set
    #print('Opening word features...')
    features_f = open(word_feature_pickle, 'rb')
    word_features = pickle.load(features_f)
    features_f.close()
    #print('Word features opened.\n')

    # Feature extraction
    def find_features(document):
        words = word_tokenize(document)
        features = {}
        for w in word_features:
            features[w] = (w in words)

        return features

    # Begin classification on this text
    classifyThis = find_features(text)

    # Feature set (unpickled, load on demand)
    ##print('Creating featureset...')
    ##featuresets = [(find_features(rev), category) for (rev, category) in documents]
    ##random.shuffle(featuresets)
    ##print('Featureset created.\n\n')

    # Feature set (pickled, load on demand)
    #print('Opening featureset...')
    featuresets_f = open(featureset_pickle, 'rb')
    featuresets = pickle.load(featuresets_f)
    featuresets_f.close()
    random.shuffle(featuresets)
    #print('Featureset opened.\n')

    #Testing and training sets
    #Reset to 10K after testing with a 3K set
    #print('Training...')
    training_set = featuresets[:10000]
    testing_set = featuresets[10000:]
    #print('Featureset length: %d \n' % len(featuresets))

    #Unpickle classifier
    #Reset after testing with a 3K set
    #print('Opening classifier...')
    classifier_f = open(nbclassifier_pickle, 'rb')
    classifier = pickle.load(classifier_f)
    classifier_f.close()
    #print('Classifier opened.\n')

    #print('Classifying...')
    voted_classifier = VoteClassifier(classifier)
    # working_accuracy = nltk.classify.accuracy(voted_classifier, testing_set) * 100
    # working_accuracy_formatted = "{0:.2f}".format(working_accuracy)
    classification = voted_classifier.classify(classifyThis)
    confidence = voted_classifier.confidence(classifyThis)

    print('Classification request completed.')
    ##for x in range(1,6,1):
    ##    print('Classification: ', voted_classifier.classify(testing_set[x][0]), "Confidence: ", voted_classifier.confidence(testing_set[x][0])*100)

    return classification, confidence

def sentiment_multiple(myList = [], *args):
    results = []
    for x in myList:
        feats = beginClassification(x)
        results.append(feats)

    return results

def sentiment_single(text):
    feats = beginClassification(text)
    return feats
