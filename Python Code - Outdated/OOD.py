'''
Program that structures the group data in Object-Oriented Design
'''

'''
STRUCTURE:
Adoptable Group:
	- Name (string)
	- Watcher Count (integer)
	- Categories (array of integers)
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
	time.sleep(10)
	url_name = "http://www." + group_name + ".deviantart.com"
	#print url_name + '   ',
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

# -----------------------------------------------------------
class GROUP: #{
	'Base class for all adoptable groups'
	def __init__(self, name="", watcher_count=0, categories=[]):
		self.name = name
		self.watcher_count = watcher_count
		self.categories = categories
	def addCategory(self, value):
		self.categories.append(value)
	
	def delCategory(self, value):
		self.categories.remove(value)

	def sortCategory(self):
		self.categories.sort()
	
	def updateWC(self):
		self.watcher_count = return_num_of_watchers(self.name)
	
	def print4txts(self):
		# 'adoptapedia',1290,[1,3,5,]
		temp_string = "'" + self.name + "'," + str(self.watcher_count) + ",["
		for i in range(0, len(self.categories)):
			temp_string += str(self.categories[i]) + ","
		temp_string = temp_string[:-1] + "]\n"
		return temp_string
	
	def print4journals(self):
		# :iconadoptapedia: :devadoptapedia:
		temp_string2 = ":icon" + self.name + ": :dev" + self.name + ": \n"
		return temp_string2
#}

# ===========================================================
object_array = []
text_file = open("all_data.txt", "r")
groupNames = text_file.readlines()
text_file.close()
#empty_array = [31,32,33]
t0 = time.time()
for i in range(0, len(groupNames)):
	groupNames[i] = groupNames[i].translate(None, whitespace)
	exec_string = 'x = GROUP(' + groupNames[i] + ')'
	exec exec_string
	#x = GROUP(groupNames[i],i,empty_array)
	#x.updateWC()
	groupNames[i] = groupNames[i].translate(None, whitespace)
	#print str(i) + ':   ' + groupNames[i] + '   ' + str(return_num_of_watchers(x.name)) + "   || " + str((i/float(len(groupNames)))*100) + "%"
	print groupNames[i] + '\t\t' + str(return_num_of_watchers(x.name))# + "   || " + str((i/float(len(groupNames)))*100) + "%"
	object_array.append(x)
	#print str(i) + ':   ' + groupNames[i] + '   ' + str(return_num_of_watchers(groupNames[i]))
t1 = time.time()
'''
text_file = open("testdata.txt", "r")
all_adopts_names = text_file.readlines()
text_file.close()

for i in range(0,len(all_adopts_names)):
	all_adopts_names[i] = all_adopts_names[i].translate(None, whitespace)


for i in range(0, len(object_array)):
	#groupNames[i] = obj[i].translate(None, whitespace)
	object_array[i].delCategory(31)
	object_array[i].delCategory(32)
	object_array[i].delCategory(33)
	object_array[i].sortCategory()
'''

#obj1 = GROUP("adopt-sugar",123,[1,2,3])
#obj2 = GROUP("adopt-supermarket",456,[4,5,6])
#obj3 = GROUP("adopt-to-ya-drop",789,[7,8,9])

#print obj1.watcher_count
#obj1.updateWC()
#print obj1.watcher_count

#print("-------")
text_file = open("testdata2.txt", "w")
for i in range(0, len(object_array)):
	#temp_string3 = str(object_array[i].categories[0]) + "\n"
	text_file.write(object_array[i].print4txts())
text_file.close()
t2 = time.time()

print "updateWC    " + str(t1-t0)
print "text_file   " + str(t2-t1)
print "TOTAL TIME  " + str(t2-t0)