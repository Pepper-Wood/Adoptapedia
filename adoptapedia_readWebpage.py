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
	try: #{
		response = urllib2.urlopen(req)
		page_source = response.read()
		
		watch_list = []
		account_check_array = []
		
		# ---------------------------------------------------
		# create a subclass and override the handler methods
		class MyHTMLParser(HTMLParser):
			def handle_data(self, data):
				account_check_array.append(data)
				#if data.find("atchers") != -1:
				#	watch_list.append(data)
		# ---------------------------------------------------
		# instantiate the parser and fed it some HTML
		parser = MyHTMLParser()
		parser.feed(page_source)
		
		#determine if an entry is an account or a group
		if page_source.find('content="&nbsp;">') != -1:
			# watcher count will be set at 0
			return 0
		
		watch_integer = []
		for i in range(0, len(account_check_array)):
			if ("atchers" in account_check_array[i]) and hasNumbers(account_check_array[i]):
				account_check_array[i] = account_check_array[i].replace(' Watchers','')
				watch_integer.append(account_check_array[i-1])
				watch_integer.append(account_check_array[i])
				#print "..." + account_check_array[i] + "..."
				#print "..." + account_check_array[i-1] + "..."
		for i in range(0, len(watch_integer)):
			print watch_list[i],
		print "\n-----------------"
		
		for i in range(0, len(watch_integer)): #{
			if ',' in watch_integer[i]: #{
				watch_integer[i] = watch_integer[i].replace(',','')
				if watch_integer[i].isdigit(): #check if the remaining string is only numbers
					return int(watch_integer[i])
			#}
			else: #{
				if watch_integer[i].isdigit(): #check if the remaining string is only numbers
					return int(watch_integer[i])
			#}
		#}
	except: #{
		print "ERROR - COULD NOT LOAD " + group_name
		return 0
	#}
#}

# ===========================================================
text_file = open("testdata.txt", "r")
groupNames = text_file.readlines()

for i in range(0, len(groupNames)):
	#if groupNames[i][0] != "#":
	groupNames[i] = groupNames[i].translate(None, whitespace)
	print str(i) + ':   ' + groupNames[i] + '   ' + str(return_num_of_watchers(groupNames[i]))
