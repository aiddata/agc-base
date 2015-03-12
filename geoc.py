# call from bash script for each prep output txt file
# process / geocode prep text
# (may need separate processing for csv's)

import sys
import os
import string
import nltk
import nltk.data

from pymongo import MongoClient

# from geopy.geocoders import GeoNames


reload(sys)
sys.setdefaultencoding('utf8')

in_cbase = sys.argv[1]
in_country = sys.argv[2]
in_prep = sys.argv[3]
in_geoc = sys.argv[4]
in_full = sys.argv[5]
in_file = os.path.basename(in_full)

out_full = in_cbase+'/geoc/'+in_prep+'_'+in_geoc+'/'+in_prep+'_'+in_geoc+'_raw.tsv'

print "geoc.py : " + in_file 


# geolocator = GeoNames(username='jpowell')

client = MongoClient()
db = client.geonames
collection = db[in_country]


finput = open(in_full, 'r')
foutput = open(out_full, 'a')


raw = finput.read()

# tokens = nltk.sent_tokenize(raw)
content = nltk.word_tokenize(raw)
# print content
# text = nltk.Text(tokens)

out_string = ""

for w in content:
	query = w


	# location = geolocator.geocode(query, False, 120)


	# --------------------------------

	# search mongo for query in asciiname
	for location in collection.find({"asciiname": query}).limit(1):

		out_string += location['asciiname']+"\t"+str(location['longitude'])+"\t"+str(location['latitude'])+"\t"+in_file+"\t"+query+"\n"


	# --------------------------------


	# print location
	
	# if location != None and location[0].latitude < -9.00 and location[0].latitude > -18.00 and location[0].longitude < 37.00 and location[0].longitude > 32.00:
		# foutput.write(str(location[0])+"\t"+str(location[0].longitude)+"\t"+str(location[0].latitude)+"\t"+in_file+"\t"+w+"\n")
		# out_string += str(location[0])+"\t"+str(location[0].longitude)+"\t"+str(location[0].latitude)+"\t"+in_file+"\t"+w+"\n"

	# if location != None:
		# for loc in location:
			# if loc.latitude < -9.00 and loc.latitude > -18.00 and loc.longitude < 37.00 and loc.longitude > 32.00:
				# print loc
				# foutput.write(str(loc)+"\t"+str(loc.longitude)+"\t"+str(loc.latitude)+"\t"+in_file+"\t"+w+"\n")

foutput.write(out_string)

finput.close()
foutput.close()

print "geoc.py : Geocoding done"
