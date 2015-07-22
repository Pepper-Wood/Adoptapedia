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

# -----------------------------------------------------------
class GROUP: #{
	'Base class for all adoptable groups'
	def __init__(self, name="", watcher_count=0, categories=[]):
		self.name = name
		self.watcher_count = watcher_count
		self.categories = categories
	def addCategory(self, value):
		self.categories.append(value)
	
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
empty_array = [31,32,33]

for i in range(0, len(groupNames)):
	groupNames[i] = groupNames[i].translate(None, whitespace)
	exec_string = 'x = GROUP(' + groupNames[i] + ')'
	exec exec_string
	#x = GROUP(groupNames[i],i,empty_array)
	#x.updateWC()
	object_array.append(x)
	#print str(i) + ':   ' + groupNames[i] + '   ' + str(return_num_of_watchers(groupNames[i]))

text_file = open("testdata.txt", "r")
all_adopts_names = text_file.readlines()
text_file.close()

for i in range(0,len(all_adopts_names)):
	all_adopts_names[i] = all_adopts_names[i].translate(None, whitespace)

for i in range(0, len(object_array)):
	#groupNames[i] = obj[i].translate(None, whitespace)
	if (object_array[i].name in all_adopts_names):
		object_array[i].addCategory(3)
		

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
