import csv
from gensim.models import Word2Vec
import string
import pickle
import numpy

model = Word2Vec.load('sw/sw.bin')

words = list(model.wv.vocab)

print(model.wv.similar_by_word('divai', 5))
    


# Pickle is in python 2, using encoding to open pickle with python 3
with open('polyglot-sw.pkl', 'rb') as f:
    words, embeddings = pickle.load(f, encoding='bytes')

# To print embeddings shape to test embeddings
# print("Embeddings shape is {}".format(embeddings.shape))


########################################################################
# This is the K-nearest neighbor code from Polyglot for these word     #
# embeddings. I converted it from python 2 to python 3                 #
# source: https://sites.google.com/site/rmyeid/projects/polyglot       #
########################################################################

from operator import itemgetter
import re

# Special tokens
Token_ID = {"<UNK>": 0, "<S>": 1, "</S>":2, "<PAD>": 3}
ID_Token = {v:k for k,v in Token_ID.items()}

# Map words to indices and vice versa
word_id = {w:i for (i, w) in enumerate(words)}
id_word = dict(enumerate(words))

# Noramlize digits by replacing them with #
DIGITS = re.compile("[0-9]", re.UNICODE)

# Number of neighbors to return.
# Number modified to return 5 NN in addition to the item itself
# Number should be changed to 3 for 2 NN
k = 6


def case_normalizer(word, dictionary):
  """ In case the word is not available in the vocabulary,
     we can try multiple case normalizing procedure.
     We consider the best substitute to be the one with the lowest index,
     which is equivalent to the most frequent alternative."""
  w = word
  lower = (dictionary.get(w.lower(), 1e12), w.lower())
  upper = (dictionary.get(w.upper(), 1e12), w.upper())
  title = (dictionary.get(w.title(), 1e12), w.title())
  results = [lower, upper, title]
  results.sort()
  index, w = results[0]
  if index != 1e12:
    return w
  return word


def normalize(word, word_id):
    """ Find the closest alternative in case the word is OOV."""
    if not word in word_id:
        word = DIGITS.sub("#", word)
    if not word in word_id:
        word = case_normalizer(word, word_id)

    if not word in word_id:
        return None
    return word


def l2_nearest(embeddings, word_index, k):
    """Sorts words according to their Euclidean distance.
       To use cosine distance, embeddings has to be normalized so that their l2 norm is 1."""

    e = embeddings[word_index]
    distances = (((embeddings - e) ** 2).sum(axis=1) ** 0.5)
    sorted_distances = sorted(enumerate(distances), key=itemgetter(1))
    return zip(*sorted_distances[:k])


def knn(word, embeddings, word_id, id_word):
    word = normalize(word, word_id)
    if not word:
        #print("OOV word")
        return
    word_index = word_id[word]
    indices, distances = l2_nearest(embeddings, word_index, k)
    neighbors = [id_word[idx] for idx in indices]
    
    # modified here to return list
    return neighbors
    # for i, (word, distance) in enumerate(zip(neighbors, distances)):  
    #    print(i, '\t', word, '\t\t', distance)
    

########################################################################
# End of KNN code from Polyglot                                        #                                                          
########################################################################

print(knn('divai', embeddings, word_id, id_word))

print(model.wv.similar_by_vector('divai', 5))

