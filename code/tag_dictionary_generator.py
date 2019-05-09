import collections
import pprint

def dict_generator(): 
    ''' CHANGE FOR TRAINING # '''
    # Import Swahili training data for tag dicitonary
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
    
    
    # Create dataset from parsed files
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
    
    word_dict = {}
    
    # Count tag occurences by word
    for sentence in training_sentences:
        for word in sentence:
            word_dict[word[0]] = collections.Counter()
                    
    for sentence in training_sentences:
        for word in sentence:
            token = word[0]
            tag = word[1]
            word_dict[token][tag] += 1
            
    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(word_dict)
    return word_dict
       
