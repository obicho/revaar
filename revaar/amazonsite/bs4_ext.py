from bs4 import BeautifulSoup
import MySQLdb, time, logging
from urllib2 import Request, urlopen, URLError, HTTPError

# ++++++++++++++++++++++++ Enter Parameter
p_name = "Kindle Fire HD 8.9 Tablet"
p_code = "B008GFRB9E"		# prod code on amazon
category = "Tablet"			# set up the category for this p
num_page = 4 				# number of pages to grab

def db_insert_p_image():
	
	# downloag image
	url_str = "http://www.amazon.com/dp/" + p_code + "/"
	mysoup = BeautifulSoup(urlopen(url_str))
	a = mysoup.find("div", {"id": "rwImages_hidden"})
	print a.img['src']
	save_img(a.img['src'])
	print "Image saved!"

	# insert img_path to db
	connection=MySQLdb.connect(
	    host='localhost',user='root',
	    passwd='abc123abc',db='reva2')
	cursor=connection.cursor()
	sql = 'update prods set img_path = %s where p_name = %s'
	args = [p_code+'.jpg', p_name]

	try:
		cursor.execute(sql, args)
		connection.commit()
		print 'img path updated (if p_name was found in prods table)'
	except Exception,e:
		connection.rollback()
		print str(e)
		print 'img path update failed'

	cursor.close()
	connection.close()

def save_img(url_str):
	#create the url and the request
	url = url_str
	req = Request(url)
	file_name = '/Users/cho/Sites/dev/reva2/reva2/reva2/static/' + p_code + '.jpg'
	
	# Open the url
	try:
		f = urlopen(req)
		print "downloading " + url
		
		# Open our local file for writing
		local_file = open(file_name, "wb")
		#Write to our local file
		local_file.write(f.read())
		local_file.close()
		
	#handle errors
	except HTTPError, e:
		print "HTTP Error:",e.code , url
	except URLError, e:
		print "URL Error:",e.reason , url

def db_update_category():
	connection=MySQLdb.connect(
	    host='localhost',user='root',
	    passwd='abc123abc',db='reva2')
	cursor=connection.cursor()

	sql = 'update prods set category = %s where p_name = %s'
	args = [category, p_name]
	try:
		cursor.execute(sql, args)
		connection.commit()
		print 'category updated'
	except Exception,e:
		connection.rollback()
		print str(e)
		print 'category update failed'

	cursor.close()
	connection.close()

def db_update_review():

	# update p_id field in reviews table
	connection=MySQLdb.connect(
	    host='localhost',user='root',
	    passwd='abc123abc',db='reva2')
	cursor=connection.cursor()

	sql = 'UPDATE reviews r, prods p SET r.p_id = p.id where r.p_name = p.p_name'

	try:
		cursor.execute(sql)
		connection.commit()
		print 'review updated'
	except Exception,e:
		connection.rollback()
		print str(e)
		print 'reviews update failed'

	cursor.close()
	connection.close()

def db_review_insert (soup):
	connection=MySQLdb.connect(
	    host='localhost',user='root',
	    passwd='abc123abc',db='reva2')
	cursor=connection.cursor()


	#print soup.body.findAll('div')

	for a in soup.body.findAll('div', style = ["margin-left:0.5em;"]):
		print '******************'
		#print a
		
		# skipping when necessary
		try:
			b = a.contents[1].string.split(" ")[8] # # people find this useful
			c = a.contents[1].string.split(" ")[10] #  total # people
			d = a.contents[3].span.span.string.split(" ")[0] # rating
			e = a.contents[3].find('b').string.strip() # review title
			f = a.contents[3].find('nobr').string # review date
			g = a.contents[5].findAll('a')[1]['href'] # source . author review page
			i = p_name # product name



			if len(a.contents[8].string.strip()) == 0:

				h = a.contents[10].string.strip() # review text
			else:
				h = a.contents[8].string.strip() # review text
			
			if len(h) == 0:
				h = a.contents[12].string.strip()
				#print 'inside'
				#print h

			# print e
			# print '&&&&'
			# print a.contents[12]
			# print '^^^'
			# print a.contents


		
		except Exception, ex:
			logging.exception("Something awful happened!")
			# if something went wrong, then skip a loop. Go on to the next review
			continue
			#print e

		sql='INSERT IGNORE INTO review_ingest ( \
									useful_count, \
									total_count, \
									rating, \
									review_title, \
									review_date, \
									source_url, \
									review_text, \
									p_name ) VALUES ( \
									%s, %s, %s, %s, %s, %s, %s, %s \
									)'
		x = time.strptime(f, "%B %d, %Y")
		y = time.strftime("%Y-%m-%d", x)
		args=[b, c, d, e, y, g, h, i]
		#print f, time.strptime(f, "%B %d, %Y")
		#print args

		try:
			cursor.execute(sql, args)
			connection.commit()
			print 'committed'
		except Exception,e:
			connection.rollback()
			print str(e)
			print 'db commit failed'

	cursor.close()
	connection.close()


# Insert reviews
for i in range(0, num_page):
	print i
	url_str = "http://www.amazon.com/product-reviews/" + p_code + "/ref=cm_cr_pr_top_link_" + str(i+1) + "?ie=UTF8&pageNumber=" + str(i+1) + "&showViewpoints=0"
	mysoup = BeautifulSoup(urlopen(url_str))
	print mysoup.head.title.string.split(':')[2]
	db_review_insert(mysoup)


# update category
db_update_category()

# update pid in review
db_update_review()

# grab image
db_insert_p_image()

