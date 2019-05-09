lines = open('hcs2_new_bunge.vrt', 'r').readlines()

line_list = []

for line in lines:
    line_parts = line.split()
    if 'text' in line_parts[0]:
        pass
    else:
        line_list.append(line_parts[:3])

training_sentences = []
sentence = []

for item in line_list:
    if '<sentence' in item[0]:
        sentence = []
    elif '/sentence' in item[0]:
        training_sentences.append(sentence)
    else:
        sentence.append((item[0], item[2]))


