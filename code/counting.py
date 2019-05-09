from nltk.tag import tnt
import csv
import collections

tagset = collections.Counter()

''' CHANGE FOR TRAINING # '''
# Import TNT tagger Swahili training data
bunge = open('hcs2_new_bunge.vrt', 'r').readlines()
new_news = open('hcs2_new_news.vrt', 'r').readlines()
old_news = open('hcs2_old_news.vrt', 'r').readlines()


''' CHANGE FOR TRAINING # '''
# Parse Swahili training files
POS_training = [old_news]
line_list = []

text_counter = 0

for lines in POS_training: 
    for line in lines:
        line_parts = line.split()
        if 'text' in line_parts[0]:
            text_counter += 1
        else:
            line_list.append(line_parts[:3])


# Create training dataset from parsed files
# for loop splits text into sentences
training_sentences = []
sentence = []
sentence_counter = 0
word_counter = 0
uniq_words = collections.Counter()

for item in line_list:
    if '<sentence' in item[0]:
        sentence_counter += 1
        sentence = []
    elif '/sentence' in item[0]:
        training_sentences.append(sentence)
    else:
        sentence.append((item[0], item[2]))
        word_counter += 1
        uniq_words[item[0]] += 1
        tagset[item[2]] += 1



# Import Swahili development and testing data
print('Parsing test/dev data...')
old_books = open('hcs2_old_books.vrt', 'r').readlines()

# Parse Swahili development and testing files
POS_test_dev = [old_books]

# training and dev sets must be split by text first
# not just sentences like the training data
all_texts = []
text = []

test_text_counter = 0

for lines in POS_test_dev:
    for line in lines:
        line_parts = line.split()
        if '<text' in line_parts[0]:
            text = []
            test_text_counter += 1
        elif '/text' in line_parts[0]:
            all_texts.append(text)
        else:
            text.append(line_parts[:3])

# Now to split into dev and test set equally
text_num = len(all_texts)
dev_texts = all_texts[:(int(text_num/2))]
test_texts = all_texts[(int(text_num/2)):]

# Create gold dev dataset from parsed texts
gold_dev_sentences = []
dev_sent = []

test_sentence_counter = 0
test_word_counter = 0
test_uniq_words = collections.Counter()


for text in dev_texts:
    for item in text:
        if '<sentence' in item[0]:
            dev_sent = []
            test_sentence_counter += 1
        elif '/sentence' in item[0]:
            gold_dev_sentences.append(dev_sent)
        else:
            dev_sent.append((item[0], item[2]))
            test_word_counter += 1
            test_uniq_words[item[0]] += 1
            tagset[item[2]] += 1

            

            


# Create test dataset from parsed texts
gold_test_sentences = []

for text in test_texts:
    for item in text:
        if '<sentence' in item[0]:
            test_sent = []
            test_sentence_counter += 1
        elif '/sentence' in item[0]:
            gold_test_sentences.append(test_sent)
        else:
            test_sent.append((item[0], item[2]))
            test_word_counter += 1
            test_uniq_words[item[0]] += 1
            tagset[item[2]] += 1

print('Tagset: ', tagset)

'''print('Texts:', test_text_counter, 'Sentences:', test_sentence_counter, 'Words:', test_word_counter, 'Unique:', len(list(test_uniq_words)))'''
