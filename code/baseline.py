import tag_dictionary_generator
import collections
import csv

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
'''
def get_tag(word):
    print(word)
    try:
        print("searching for", word)
        tags = tag_dict[word]
        print(tags)
    except:
        pass
'''

modified_tagged_sentences = []

for sentence in tagged_sentences:
    new_sent = []
    for obj in sentence:
        word = obj[0]
        pred = obj[1]
        gold = obj[2]
        if pred == 'Unk':
            #final_tag = get_tag(word)
            pred = 'N'
            new_sent.append([word, pred, gold])
        else:
            new_sent.append([word, pred, gold])
    modified_tagged_sentences.append(new_sent)
    
# Counting scores
word_count = 0
right = 0
wrong = 0
unk = 0

for sentence in modified_tagged_sentences:
    for obj in sentence:
        pred = obj[1]
        gold = obj[2]
        word_count += 1
        if pred == gold:
            right += 1
        else:
            wrong += 1
        if pred == 'Unk':
            unk += 1

print(word_count, right, wrong, unk, (word_count-(right+wrong)))
