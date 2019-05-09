import tag_dictionary_generator
import pprint
import csv
from gensim.models import Word2Vec
import string
import pickle
import numpy
import collections

# import first set of word embeddings
model = Word2Vec.load('sw/sw.bin')

words = list(model.wv.vocab)    

# import second set of word embeddings
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


# generate tag dictionary
tag_dict = tag_dictionary_generator.dict_generator()

'''Change for different document scoring '''
doc = open('dev_output_3_training.csv', 'r')

tagged_sentences = []

# Open and read CSV file
with doc:
    csv_reader = csv.reader(doc)
    sentence = []
    # Process text from CSV file
    for row in csv_reader:
        if row == []:
            tagged_sentences.append(sentence)
            sentence = []
        else:
            word = row[0]
            pred = row[1]
            gold = row[3]
            sentence.append([word, pred, gold])
    tagged_sentences.append(sentence)

# find similar words for unkown tags
def fix_unk(word):
    similar_words = knn(word, embeddings, word_id, id_word)
    if similar_words != None:
        # remove original word
        similar_words = similar_words[1:]
    else:
        try:
            similar_words = model.wv.similar_by_vector(word, 5)
        except:
            similar_words = None
    return similar_words

# choose best tag
def tag_scoring(options):
    # scores taken from only the best counter
    tag_choices = []
    for item in options:
        tag_choices.append(item.most_common(1)[0][0])
    try:    
        tag = collections.Counter(tag_choices).most_common(1)[0][0]
    except:
        tag = 'Unk'
    # scores by the combined counter scores of every word
    '''final_counter = collections.Counter()
    for item in options:
        final_counter += item
    tag = final_counter.most_common(1)
    try:
        tag = tag[0][0]
    except:
        tag = 'Unk'
        '''
    return tag

# find the similar words in the tag dictionary
def check_similar_words(similar_words):
    options = []
    if similar_words == None:
        return 'Unk'
    else:
        for word in similar_words:
            try:
                options.append(tag_dict[word])
            except:
                pass
        tag = tag_scoring(options)
    return tag

# updating sentence tags for unknowns
modified_tagged_sentences = []

counter = 0

unknown_words = []

for sentence in tagged_sentences:
    new_sent = []
    for obj in sentence:
        word = obj[0]
        pred = obj[1]
        gold = obj[2]
        if pred == 'Unk':
            counter += 1
            similar_words = fix_unk(word)
            final_tag = check_similar_words(similar_words)
            unknown_words.append([word, pred, gold, final_tag])
            pred = final_tag
            new_sent.append([word, pred, gold])
        else:
            new_sent.append([word, pred, gold])
    modified_tagged_sentences.append(new_sent)

#print(counter)
           
# Generate new tagging output
f = open('dev_output_3_improved.csv', 'w')

with f:

    writer = csv.writer(f)

    for index, sentence in enumerate(modified_tagged_sentences):
        writer.writerow('')
        for count, word in enumerate(sentence):
            row = [word[0],word[1],word[0],word[2]]
            writer.writerow(row)
            
for item in unknown_words:
    print(item[0], '\t', item[1], '\t', item[2], '\t', item[3])
