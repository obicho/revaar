
asin = 'mixed'
fread = open(asin+'.txt','r')
w = 0
b = ''
helpful='helpful'
stars =''
review_counter = 1

for line in fread:
	if line.find('people found the following review helpful') > -1:
		#print line
		words = line.split(' ', 1)

		# separating good reviews from the mediocre ones.
		if int(words[0]) > 20:
			helpfulness = 'helpful'
		else:
			helpfulness = 'ok'

		w = 1
		b = b + line

	elif w == 0 and line.find('out of 5 stars') > -1:

		# this is when we have to process reviews without the any helpful rating from user	
		helpfulness = 'ok'
		w = 1
		b = b + line

	elif line.find('Help other customers find the most helpful reviews') > -1:
		
		# done going through reviews. now write the file out
		#print line
		f = open('reviews' + '/' + helpfulness +'/' + asin + '_' + str(review_counter) + '_' + stars + '.txt', 'w')
		w = 0
		f.write(b)
		f.close()
		#print '*********-----**** \n' + b
		b = ''
		review_counter += 1

	else:
		if w:

			# Only write relevant parts out. skip links

			if (line[0:21] != '**This review is from') and \
				 not 'nbsp_place_holder' in line and \
				 not 'http://' in line and \
				 not 'sort_by' in line and \
				 line[0:28] != '**Amazon Verified Purchase**':
				b = b + line
				#print b

			# Need to find out how many stars was given to this review
			# This is appended to
			if line.find('out of 5 stars') > 0:
				starswords = line.split(' ', 1)
				stars = starswords[0]
				#print str(stars)



 #   fwrite.write("insert into wp_users ( ID, user_login, user_name ) values (%s, '%s', '%s')\n" % (line[0], line[1], line[2]))
fread.close()
print str(review_counter) + ' reviews extracted'
#fwrite.close()