'''
Basic program to take a webpage and return the number of watchers a group has
'''

import urllib2
from HTMLParser import HTMLParser

# -----------------------------------------------------------
def hasNumbers(inputString):
	return any(char.isdigit() for char in inputString)

# -----------------------------------------------------------
def return_num_of_watchers(group_name):
	url_name = "http://" + group_name + ".deviantart.com"
	req = urllib2.Request(url_name)
	response = urllib2.urlopen(req)
	page_source = response.read()
	
	watch_list = []
	# -----------------------------------------------------------
	# create a subclass and override the handler methods
	class MyHTMLParser(HTMLParser):
		def handle_data(self, data):
			if data.find("atchers") != -1:
				watch_list.append(data)

	# instantiate the parser and fed it some HTML
	parser = MyHTMLParser()
	parser.feed(page_source)
	
	for i in range(0, len(watch_list)):
		watch_list[i] = watch_list[i].replace(' Watchers','')
		if hasNumbers(watch_list[i]):
			watch_integer = watch_list[i]
		#print "ITEM " + str(i) + ':  "' + watch_list[i] + '"'

	print 'BEFORE:' + str(watch_integer)
	final_int = int(watch_integer.replace(',',''))
	print 'AFTER: ' + str(final_int)
	
	
return_num_of_watchers("adoptapedia")