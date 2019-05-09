from nltk.tag import tnt
import csv

''' CHANGE FOR TRAINING # '''
# Import TNT tagger Swahili training data
print('Parsing training data...')
bunge = open('hcs2_new_bunge.vrt', 'r').readlines()
new_news = open('hcs2_new_news.vrt', 'r').readlines()
old_news = open('hcs2_old_news.vrt', 'r').readlines()


''' CHANGE FOR TRAINING # '''
# Parse Swahili training files
POS_training = [bunge, new_news, old_news]
line_list = []

for lines in POS_training: 
    for line in lines:
        line_parts = line.split()
        if 'text' in line_parts[0]:
            pass
        else:
            line_list.append(line_parts[:3])


# Create training dataset from parsed files
# for loop splits text into sentences
training_sentences = []
sentence = []

for item in line_list:
    if '<sentence' in item[0]:
        sentence = []
    elif '/sentence' in item[0]:
        training_sentences.append(sentence)
    else:
        sentence.append((item[0], item[2]))


# initialize and train tagger
print('Training tagger...')
tnt_tagger = tnt.TnT()
tnt_tagger.train(training_sentences)


# Single sentence tagging test
'''tagged_test_sent = [('Kwa','PREP'),
('thuluthi','N'),
('ya_kwanza','NUM'),
('alikuwa','V'),
('msuluhifu','ADJ'),
('akapendwa', 'N'),
('na','CC'),
('watu','N'),
(',','COMMA'),
('kwa','PREP'),
('thuluthi','N'),
('ya_pili','GEN-CON'),
('alifanana','V'),
('na','PREP'),
('Daud','PROPNAME'),
('akaheshimiwa','N'),
('kama','ADV'),
('mtunzaji','N'),
('mkuu','ADJ'),
('wa','GEN-CON'),
('wanyama','N'),
(',','COMMA'),
('na','CC'),
('kwa','PREP'),
('thuluthi','N'),
('ya_tatu','GEN-CON'),
('alikuwa','V'),
('kama','ADV'),
('Suleman','PROPNAME'),
('akatiiwa','N'),
('na','CC'),
('majini','N'),
('.','_')]

test_sent = []

for obj in tagged_test_sent:
    test_sent.append(obj[0])

# run tagger on single test sentence
tnt_tagger_preds = tnt_tagger.tag(test_sent)

# print tagger output for single test sentence
for index, word in enumerate(tnt_tagger_preds):
    print(word, tagged_test_sent[index])'''



# Import Swahili development and testing data
print('Parsing test/dev data...')
old_books = open('hcs2_old_books.vrt', 'r').readlines()

# Parse Swahili development and testing files
POS_test_dev = [old_books]

# training and dev sets must be split by text first
# not just sentences like the training data
all_texts = []
text = []

for lines in POS_test_dev:
    for line in lines:
        line_parts = line.split()
        if '<text' in line_parts[0]:
            text = []
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

for text in dev_texts:
    for item in text:
        if '<sentence' in item[0]:
            dev_sent = []
        elif '/sentence' in item[0]:
            gold_dev_sentences.append(dev_sent)
        else:
            dev_sent.append((item[0], item[2]))

# Create untagged dev dataset from gold set
untagged_dev_sentences = []

for sentence in gold_dev_sentences:
    untagged_sentence = []
    for word in sentence:
        untagged_sentence.append(word[0])
    untagged_dev_sentences.append(untagged_sentence)

# Create test dataset from parsed texts
gold_test_sentences = []
test_sent = []

for text in test_texts:
    for item in text:
        if '<sentence' in item[0]:
            test_sent = []
        elif '/sentence' in item[0]:
            gold_test_sentences.append(test_sent)
        else:
            test_sent.append((item[0], item[2]))

# Create untagged test dataset from gold set
untagged_test_sentences = []

for sentence in gold_test_sentences:
    untagged_sentence = []
    for word in sentence:
        untagged_sentence.append(word[0])
    untagged_test_sentences.append(untagged_sentence)
    
    
# Use development set for model tuning
# Tag dev set
print('Tagging dev set...')
tnt_dev_output = tnt_tagger.tagdata(untagged_dev_sentences)

''' CHANGE FOR TRAINING # '''
print('Writing CSV output file...')
f = open('dev_output_3_training.csv', 'w')

with f:

    writer = csv.writer(f)

    for index, sentence in enumerate(tnt_dev_output):
        writer.writerow('')
        for count, word in enumerate(sentence):
            row = [word[0],word[1],gold_dev_sentences[index][count][0],gold_dev_sentences[index][count][1]]
            writer.writerow(row)

