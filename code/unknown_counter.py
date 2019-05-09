import collections
import pprint

lines = open('unknowns.txt', 'r').readlines()

unknowns = []

for line in lines:
    line_parts = line.split()
    unknowns.append(line_parts)
    if len(line_parts) < 4:
        print(line_parts)

changed = 0
correct = 0

uniq_unk = collections.Counter()
tag_count = collections.Counter()

for item in unknowns:
    word, pred, gold, final_tag = item
    if pred != final_tag:
        changed += 1
        if final_tag == gold:
            correct += 1
    uniq_unk[word.lower()] += 1
    tag_count[gold]+=1
            
t_ac = (correct/len(unknowns)) * 100
unk_ac = (correct/changed) * 100


print('All Unkowns: ', len(unknowns))
print('Changed: ', changed)
print('Correct: ', correct)
print('Total Unknown Accuracy', round(t_ac,2),'%')
print('Changed Accuracy: ', round(unk_ac,2), '%')
print('Number of Unique Unknown Words: ', len(uniq_unk))
print('Tag Distribution: ')
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(tag_count)
