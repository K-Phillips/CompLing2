import csv

'''Change for different document scoring '''
doc = open('dev_output_3_improved.csv', 'r')

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


# Counting scores
word_count = 0
right = 0
wrong = 0
unk = 0

for sentence in tagged_sentences:
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
