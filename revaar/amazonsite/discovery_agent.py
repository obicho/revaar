from bs4 import BeautifulSoup
import MySQLdb, time, logging
from urllib2 import Request, urlopen, URLError, HTTPError



url_str = "http://www.amazon.com/gp/rss/new-releases/wireless/2407749011/ref=zg_bsnr_2407749011_rsslink"
mysoup = BeautifulSoup(urlopen(url_str))
a = mysoup.findAll("title")

print a