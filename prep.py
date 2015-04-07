# call from bash script for each ocr output txt file
# process raw text

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

# add spaces instead of removing punctuation (mainly for csv's)
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


# *****
# (may need to add separate processing for csv's)
# *****


# split strings using uppercase letters as markers (start at end of word)
# 


# get rid of stopwords, all uppercase words, all lowercase words
stopwords = nltk.corpus.stopwords.words('english')
months = ('january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december')
# additional stopwords list (see junk2geo)
general_stops = open('junk2geo/stopwords/stopwords_en_es_fr_pt_de_it.txt','r').read().split('\n')

content = [w for w in tokens if w.lower() not in stopwords and w.lower() not in months and w.lower() not in general_stops]

# remove all lowercase words, all uppercase words and words with over 2 synsets
content = [w for w in content if not w.islower() and not w.isupper() and len(wordnet.synsets(w)) < 2]

# remove words with a synset other than entity
content = [w for w in content if len(wordnet.synsets(w)) == 0 or (len(wordnet.synsets(w)) == 1 and string.find(str(wordnet.synsets(w)[0].root_hypernyms()[0]), 'entity.n.01') != -1 ) ]

# remove words under 2 char and over 30
content = [w for w in content if len(w) > 3 or len(w) < 30]

# remove all words with over 50% uppercase chars and words with 12+char with over 33% uppercase chars
content = [w for w in content if float(sum(1 for c in w if c.isupper()))/float(len(w)) < 0.5 or (len(w) > 12 and float(sum(1 for c in w if c.isupper()))/float(len(w)) < 0.33)]


# remove words with same char 3+ times in a row

def char_count(word):
	prev_c = ''
	same_c = 1
	for c in word:
		if c == prev_c:
			same_c += 1
		else:
			same_c = 1

		if same_c > 2:
			return False

		prev_c = c

	return True


content = [w for w in content if char_count(w)]

# sort uniq
content = sorted(set(content))



# fuzzy search names for tmp geonames list
# find each occurence of each tmp geoname in original text
# fuzzy check for match






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


out = '\n'.join(content)
foutput.write(out)

finput.close()
foutput.close()

print "prep.py : OCR text preprocessing done"
