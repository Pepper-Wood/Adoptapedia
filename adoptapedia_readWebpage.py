'''
Basic program to take a webpage and return the number of watchers a group has
'''

import urllib2
from HTMLParser import HTMLParser
from string import whitespace

# -----------------------------------------------------------
def hasNumbers(inputString): #{
	return any(char.isdigit() for char in inputString)
#}

# -----------------------------------------------------------
def return_num_of_watchers(group_name): #{
	url_name = "http://" + group_name + ".deviantart.com"
	req = urllib2.Request(url_name)
	response = urllib2.urlopen(req)
	page_source = response.read()
	
	watch_list = []
	
	# ---------------------------------------------------
	# create a subclass and override the handler methods
	class MyHTMLParser(HTMLParser):
		def handle_data(self, data):
			if data.find("atchers") != -1:
				watch_list.append(data)
	# ---------------------------------------------------
	# instantiate the parser and fed it some HTML
	parser = MyHTMLParser()
	parser.feed(page_source)
	
	watch_integer = ''
	for i in range(0, len(watch_list)):
		watch_list[i] = watch_list[i].replace(' Watchers','')
		if hasNumbers(watch_list[i]):
			watch_integer = watch_list[i]

	if ',' in watch_integer:
		final_int = int(watch_integer.replace(',',''))
	else:
		final_int = int(watch_integer)
	return final_int
#}

# ===========================================================
text_file = open("testdata.txt", "r")
groupNames = text_file.readlines()

for i in range(0, len(groupNames)):
	groupNames[i] = groupNames[i].translate(None, whitespace)
	print str(i) + ':   ' + groupNames[i] + '   ' + str(return_num_of_watchers(groupNames[i]))