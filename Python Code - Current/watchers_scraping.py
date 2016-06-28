from BeautifulSoup import BeautifulSoup
import urllib2
import re

rep = ['<div class="pbox pppbox">','<b>','</b','<br />','</div>','>',',']

def get_stats(group_name):
	url = "http://" + group_name + ".deviantart.com"
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page.read())
	stats = soup.find("div", {"class": "pbox pppbox"})
	stats = (str(stats).replace(rep[0],'').replace(rep[1],'').replace(rep[2],'').replace(rep[3],'').replace(rep[4],'').replace(rep[5],'').replace(rep[6],'')).split()
	if len(stats) == 6:
		return (int(stats[0]), int(stats[2]), int(stats[4]))
	else:
		return (0,0,0)

print get_stats('adoptapedia')
print get_stats('pepper-wood')