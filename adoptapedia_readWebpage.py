'''
Basic program to take a webpage and return the number of watchers a group has
'''

import time
import urllib2
from HTMLParser import HTMLParser
from string import whitespace

# -----------------------------------------------------------
def hasNumbers(inputString): #{
	return any(char.isdigit() for char in inputString)
#}

# -----------------------------------------------------------
# https://github.com/Gullimama/urllib2/blob/master/urltests/linkcheck.py
def checklink(link):
	#right = []
	#wrong = []
	#for link in links:
	try:
		req = urllib2.Request(link, headers={'User-Agent' : "Magic Browser"}) 
		con = urllib2.urlopen( req )
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

# -----------------------------------------------------------
def return_num_of_watchers(group_name): #{
	#time.sleep(10)
	url_name = "http://www." + group_name + ".deviantart.com"
	#print url_name + '   ',
	print group_name + " checklink returned " + str(checklink(url_name))
	if checklink(url_name) == 1: #{
		#response = urllib2.Request(url_name, postBackData, { 'User-Agent' : 'My User Agent' })
		req = urllib2.Request(url_name, headers={'User-Agent' : "Magic Browser"}) 
		con = urllib2.urlopen( req )
		page_source = con.read()
		
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
			#print "THIS IS AN ACCOUNT-----------------------"
			return 0
		
		watch_integer = []
		for i in range(0, len(account_check_array)):
			if ("atchers" in account_check_array[i]) and hasNumbers(account_check_array[i]):
				account_check_array[i] = account_check_array[i].replace(' Watchers','')
				watch_integer.append(account_check_array[i-1])
				watch_integer.append(account_check_array[i])
				#print "..." + account_check_array[i] + "..."
				#print "..." + account_check_array[i-1] + "..."
		#for i in range(0, len(watch_integer)):
		#	print watch_integer[i],
		#print "\n-----------------"
		
		for i in range(0, len(watch_integer)): #{
			if ',' in watch_integer[i]: #{
				watch_integer[i] = watch_integer[i].replace(',','')
				if watch_integer[i].isdigit(): #check if the remaining string is only numbers
					return int(watch_integer[i])
					#print "---------------------Value found -----------------------"
			#}
			else: #{
				if watch_integer[i].isdigit(): #check if the remaining string is only numbers
					return int(watch_integer[i])
					#print "---------------------Value found -----------------------"
			#}
		#}
	#}
	else:
		print "URL NOT FOUND -----------------------"
		return 0
	#	except urllib2.HTTPError, e: #{
	#		print "ERROR - COULD NOT LOAD " + group_name
	#		return 0
		#}
#}
# ===========================================================
text_file = open("error_output.txt", "r")
groupNames = text_file.readlines()

for i in range(0, len(groupNames)):
	if (groupNames[i][0] == "'"):
		print "' means that it returned None"
		#groupNames[i] = groupNames[i].translate(None, whitespace)
		print str(i) + ':   ' + groupNames[i][1:] + '   ' + str(return_num_of_watchers(groupNames[i][1:]))
	else:
		if (groupNames[i][0] == ";"):
			print "; means that it returned URL NOT FOUND"
			print str(i) + ':   ' + groupNames[i][1:] + '   ' + str(return_num_of_watchers(groupNames[i][1:]))
		else:
			print "  means that it returned 0"
			print str(i) + ':   ' + groupNames[i] + '   ' + str(return_num_of_watchers(groupNames[i]))
