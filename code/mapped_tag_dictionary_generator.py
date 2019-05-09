import collections
import pprint

def dict_generator(): 
    ''' CHANGE FOR TRAINING # '''
    # Import Swahili training data for tag dicitonary
    bunge = open('hcs2_new_bunge.vrt', 'r').readlines()
    old_books = open('hcs2_old_books.vrt', 'r').readlines()
    old_news = open('hcs2_old_news.vrt', 'r').readlines()
    
    
    ''' CHANGE FOR TRAINING # '''
    # Parse Swahili training files
    POS_training = [bunge, old_books, old_news]
    line_list = []
    
    for lines in POS_training: 
        for line in lines:
            line_parts = line.split()
            if 'text' in line_parts[0]:
                pass
            else:
                line_list.append(line_parts[:3])
    
    mapping = {
        'N': 'N',
        'V': 'V',
        'V-BE':'V',
        'V-DEF': 'V',
        'GEN-CON-KWA': 'GEN-CON',
        'GEN-CON': 'GEN-CON',
        'PROPNAME': 'PROPNAME',
        'PRON': 'PRON', 
        'POSS-PRON': 'PRON', 
        'DEM': 'PRON',
        'ADV': 'ADV',
        'PREP': 'PREP', 
        'PREP/ADV': 'PREP',
        'STOP': 'STOP',
        '_': 'STOP', 
        'QUESTION-MARK': 'STOP', 
        'EXCLAM': 'STOP',
        'COMMA': 'COMMA',
        'ADJ': 'ADJ',
        'A-UNINFL': 'ADJ',
        'CC': 'CONJ', 
        'CONJ': 'CONJ', 
        'CONJ/CC': 'CONJ',
        'NUM': 'NUM', 
        'NUM-ROM': 'NUM',
        'AG-PART': 'PARTICLE',
        'DOUBLE-QUOTE-OPENING': 'QUOTATION', 
        'DOUBLE-QUOTE-CLOSING': 'QUOTATION', 
        'SINGLE-QUOTE-OPENING': 'QUOTATION', 
        'SINGLE-QUOTE-CLOSING': 'QUOTATION', 
        'SINGLE-QUOTE': 'QUOTATION', 
        'DOUBLE-QUOTE': 'QUOTATION',
        'LEFT-PARENTHESIS': 'PUNCT', 
        'RIGHT-PARENTHESIS': 'PUNCT',
        'INTERROG': 'INTERROG',
        'REL-LI-VYO': 'RELATIVE', 
        'REL-LI': 'RELATIVE', 
        'REL-SI': 'RELATIVE', 
        'REL-SI-VYO': 'RELATIVE',
        'SLASH': 'PUNCT', 
        'AMPERSAND': 'PUNCT', 
        'PERCENT-MARK': 'PUNCT', 
        'COLON': 'PUNCT', 
        'SEMI-COLON': 'PUNCT',  
        'HYPHEN': 'PUNCT', 
        'PLUS-SIGN': 'PUNCT', 
        'DOLLAR-SIGN': 'PUNCT', 
        'EQUAL-MARK': 'PUNCT', 
        'BACK-SLASH': 'PUNCT',
        'LEFT-CURLYBRACKET': 'PUNCT', 
        'RIGHT-ANGLEBRACKET': 'PUNCT', 
        'RIGHT-CURLYBRACKET': 'PUNCT', 
        'RIGHT-SQUAREBRACKET': 'PUNCT',
        'ABBR': 'ABBR',
        'MWE': 'MWE'
    }

    
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
            mapped_tag = mapping.get(item[2])
            sentence.append((item[0], mapped_tag))
    
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
       
