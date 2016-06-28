import json
import operator
import subprocess
import urllib2
import re

# -----------------------------------------------------------
class GROUP:
	# Base class for all adoptable groups
	# <string>|<int>|<set<string>>
	def __init__(self, name0="", categories0=[]):
		self.name = name0.lower() # lowercase entry
		self.watcher_count = 0
		self.categories = categories0
		
		# converting long phrases for categories into abbreviations
		for i in range(0, len(self.categories)):
			if self.categories[i] == "Accepts all adopt deviations without restrictions [Don't select anything else if you check this box]" or self.categories[i] == " Accepts all adopt deviations without restrictions [Don't select anything else if you check this box]" or self.categories[i] == "1":
				self.categories[i] = 'all'
			elif self.categories[i] == "Species-specific" or self.categories[i] == " Species-specific" or self.categories[i] == "2":
				self.categories[i] = 'species'
			elif self.categories[i] == "Fandom-specific" or self.categories[i] == " Fandom-specific" or self.categories[i] == "3":
				self.categories[i] = 'fandom'
			elif self.categories[i] == "Payment-specific (i.e. free adopts only; point adopts only; etc.)" or self.categories[i] == " Payment-specific (i.e. free adopts only; point adopts only; etc.)" or self.categories[i] == "4":
				self.categories[i] = 'payment'
			elif self.categories[i] == "Quality-Control group (i.e. filters deviations based on a set of artistic criteria)" or self.categories[i] == " Quality-Control group (i.e. filters deviations based on a set of artistic criteria)" or self.categories[i] == "5":
				self.categories[i] = 'quality'
			elif self.categories[i] == "Adoptable Base Group" or self.categories[i] == " Adoptable Base Group" or self.categories[i] == "6" or self.categories[i] == "Miscellaneous (adoptable bases, outfit adopts, hatchables, other)" or self.categories[i] == " Miscellaneous (adoptable bases, outfit adopts, hatchables, other)":
				self.categories[i] = 'misc'
			elif self.categories[i] == "Adoption Agencies (typically an RP group where adopts can be purchased with in-world currency)" or self.categories[i] == " Adoption Agencies (typically an RP group where adopts can be purchased with in-world currency)" or self.categories[i] == "7":
				self.categories[i] = 'agency'
			elif self.categories[i] == "Closed Species Group (don't select Species-Specific if you choose this option)" or self.categories[i] == " Closed Species Group (don't select Species-Specific if you choose this option)" or self.categories[i] == "8":
				self.categories[i] = 'closed'
	
	def addCategory(self, value):
		# value is a string
		self.categories.add(value)
	
	def delCategory(self, value):
		# value is a string
		self.categories.remove(value)

	def sortCategory(self):
		self.categories.sort()
	
	def updateWC(self):
		self.watcher_count = return_num_of_watchers(self.name)
	
	def print4journals(self):
		# :iconadoptapedia: :devadoptapedia:
		#return ":icon" + self.name + ": :dev" + self.name + ":"
		return ":icon" + self.name + ":"
	
	def merge_groups(self, obj):
		# merges the two categories while not taking into account duplicates
		self.categories = list(set(self.categories) | set(obj.categories))


# -----------------------------------------------------------
def convert_cd_file_with_spreadsheet_info(group_dict):
	cd_file = open("cd_file.txt", 'r')
	for line in cd_file:
		sentence_array = line.split()
		if len(sentence_array) >= 1:
			if group_dict.has_key(sentence_array[0].lower()): # entry is already included
				new_group = GROUP(sentence_array[0].lower(),sentence_array[1:])
				group_dict[sentence_array[0].lower()].merge_groups(new_group)
			else:
				group_dict[sentence_array[0].lower()] = GROUP(sentence_array[0].lower(),sentence_array[1:])
	cd_file.close()


def returnGroupIcon(url2):
        try:
                url = "http://www." + url2 + ".deviantart.com"
                sock = urllib2.urlopen(url)
        except urllib2.HTTPError, e:
                return ""
        else:
                data = sock.read()
                result = re.search('<link href=(.*) rel="image_src">', data)
                return result.group(1)

print "creating group_dict"
group_dict = {}
convert_cd_file_with_spreadsheet_info(group_dict)

print "creating the html_table thing"
for group in (sorted(group_dict.values(), key=operator.attrgetter('name'))):
    print returnGroupIcon(str(group.name))


