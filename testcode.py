import urllib2

url = "http://www.google.com"
da_groups = ["http://www.adoptapedia.deviantart.com", "http://www.adoptable-network.deviantart.com", "http://www.adoptableagencies.deviantart.com" ]


def extractpage(link = url):
	response = urllib2.urlopen(link)
	html = response.read()
	#print html
	return html

def extractlinks(page):
	links = []
	while True:
		startlink = page.find("a href=")
		startquote = page.find('"' , startlink)
		if startquote == -1:
			break
		endquote = page.find('"', startquote+1)
		links.append(page[startquote+1 : endquote])
		page = page[ endquote+1 : ]
		#print links
	return links

def checklink(link):
	#right = []
	#wrong = []
	#for link in links:
	try:
		yes = urllib2.urlopen(link)
		return 1 # TRUE - Link does exist
		#right.append(link)
	except :
		return 0 # FALSE - Link does not work
		#wrong.append(link)
	#print "right links are \n"
	#for link in right:
	#	print link
	#print "wrong links are \n"
	#for link in wrong:
	#	print link	

h = extractpage()
l = extractlinks(h)
for i in range(0, len(da_groups)):
	print checklink(da_groups[i]),
