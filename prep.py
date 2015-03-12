# call from bash script for each ocr output txt file
# process raw text
# (may need to add separate processing for csv's)

import sys
import os
import string
import nltk
import nltk.data
from nltk.corpus import wordnet
import numpy

reload(sys)
sys.setdefaultencoding('utf8')

in_cbase = sys.argv[1]
in_ocr = sys.argv[2]
in_prep = sys.argv[3]
in_type = sys.argv[4]
in_full = sys.argv[5]

in_file = os.path.basename(in_full)

out_full = in_cbase+'/prep/'+in_ocr+'_'+in_prep+'/'+in_type+'/'+in_file

print "prep.py : " + in_file 

finput = open(in_full, 'r')
foutput = open(out_full, 'w')

raw = finput.read()

# get rid of non utf8 charts
raw = ''.join(i for i in raw if ord(i)<128)

# strip punctuation

# add spaces instead of removing (mainly for csv's)
#
raw = raw.translate(None, string.punctuation)

# strip numbers
raw = raw.translate(None, string.digits)

# strip newlines
raw = raw.replace("\n", " ")



# tokenize raw text

# tokens = nltk.sent_tokenize(raw)
tokens = nltk.word_tokenize(raw)
# print tokens
# text = nltk.Text(tokens)


# split strings using uppercase letters as markers (start at end of word)
# 

# get rid of strings with >50% uppercase
# 


# get rid of stopwords, all uppercase words, all lowercase words
stopwords = nltk.corpus.stopwords.words('english')
months = ('january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december')
content = [w for w in tokens if w.lower() not in stopwords and w.lower() not in months and not w.islower() and not w.isupper() and len(wordnet.synsets(w)) < 2]

content = [w for w in content if len(wordnet.synsets(w)) == 0 or (len(wordnet.synsets(w)) == 1 and string.find(str(wordnet.synsets(w)[0].root_hypernyms()[0]), 'entity.n.01') != -1 ) ]


# get rid of words base on frequency
# may be useful if done earlier
# too few words left - ends up getting rid of placenames

# freq = {}
# for w in content:
# 	if not w in freq:
# 		freq[w] = 1
# 	else:
# 		freq[w] += 1
# # print freq

# fvals = [freq[x] for x in freq]
# print fvals

# fmean = numpy.mean(fvals)
# fsd = numpy.std(fvals)
# print fmean + fsd * 2

# fover = [x for x in freq if freq[x] > fmean + fsd * 3]
# print fover

# content = [w for w in content if w not in fover]


out = ' '.join(content)
foutput.write(out)

finput.close()
foutput.close()

print "prep.py : OCR text preprocessing done"
