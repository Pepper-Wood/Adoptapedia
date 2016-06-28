import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
import operator
import subprocess
from BeautifulSoup import BeautifulSoup
import urllib2
import re

rep = ['<div class="pbox pppbox">','<b>','</b','<br />','</div>','>']

# -----------------------------------------------------------
class GROUP:
	# Base class for all adoptable groups
	# <string>|<int>|<set<string>>
	def __init__(self, name0="", categories0=[], member_count0=0, watcher_count0=0, pageview_count0=0):
		self.name = name0.lower() # lowercase entry
		self.watcher_count = 0
		self.categories = categories0
		
		self.member_count = member_count0
		self.watcher_count = watcher_count0
		self.pageview_count = pageview_count0
		
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
				new_group_stats = get_stats(sentence_array[0].lower())
				new_group = GROUP(sentence_array[0].lower(),sentence_array[1:], new_group_stats[0], new_group_stats[1], new_group_stats[2])
				group_dict[sentence_array[0].lower()].merge_groups(new_group)
			else:
				group_dict[sentence_array[0].lower()] = GROUP(sentence_array[0].lower(),sentence_array[1:])
	cd_file.close()

# -----------------------------------------------------------
# returns the members, watchers, and pageview count for groups
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
	
# -----------------------------------------------------------
def remove_groups(group_dict):
	delete_file = open("delete.txt", 'r')
	for line in delete_file:
		if group_dict.has_key((line.lower())): # entry is already included
			del group_dict[(line.lower())]
	delete_file.close()
	open("delete.txt", 'w').close() # erases the text file

# -----------------------------------------------------------
def write_to_cd_file(group_dict):
	cd_file = open("cd_file.txt", 'w')
	for group in (sorted(group_dict.values(), key=operator.attrgetter('name'))):
		cd_file.write(str(group.name) + " " + str((' '.join(group.categories))) + "\n")
	cd_file.close()

	'all'
	"\n\n\n===ALL ADOPTS ACCEPTED=========================================================\n"
# -----------------------------------------------------------
def write_to_output_file_group(NUM_PER_ROW, NUM_PER_JOURNAL, group_dict, output, GROUP_STRING, GROUP_STRING_LONG):
	counting = 0
	output.write(GROUP_STRING_LONG)
	for group in (sorted(group_dict.values(), key=operator.attrgetter('name'))):
		if GROUP_STRING in group.categories:
			counting += 1
			output.write(group.print4journals().rstrip('\n'))
			output.write("    ".rstrip("\n"))
			if counting % NUM_PER_ROW == 0:
				output.write("\n")
			if counting % NUM_PER_JOURNAL == 0:
				output.write("\n\n")
	
# -----------------------------------------------------------
def write_to_output_file(group_dict):
	output = open("output.txt", 'w')
	output.write(str(len(group_dict)) + "\n\n")
	output.write("\n\n\n===DIRECTORY OF ALL GROUPS=====================================================\n")
	NUM_PER_ROW = 5
	NUM_PER_JOURNAL = 300
	counting = 0
	for group in (sorted(group_dict.values(), key=operator.attrgetter('name'))):
		counting += 1
		output.write(group.name.rstrip('\n'))
		output.write("    ".rstrip("\n"))
		if counting % NUM_PER_ROW == 0:
			output.write("\n")
		#if counting % NUM_PER_JOURNAL == 0:
		#	output.write("\n\n")
	# printout for data on the rest of the groups	
	write_to_output_file_group(NUM_PER_ROW, NUM_PER_JOURNAL, group_dict, output, 'all', "\n\n\n===ALL ADOPTS ACCEPTED=========================================================\n")
	write_to_output_file_group(NUM_PER_ROW, NUM_PER_JOURNAL, group_dict, output, 'species', "\n\n\n===SPECIES SPECIFIC============================================================\n")
	write_to_output_file_group(NUM_PER_ROW, NUM_PER_JOURNAL, group_dict, output, 'closed', "\n\n\n===CLOSED SPECIES==============================================================\n")
	write_to_output_file_group(NUM_PER_ROW, NUM_PER_JOURNAL, group_dict, output, 'fandom', "\n\n\n===FANDOM SPECIFIC=============================================================\n")
	write_to_output_file_group(NUM_PER_ROW, NUM_PER_JOURNAL, group_dict, output, 'payment', "\n\n\n===PAYMENT SPECIFIC============================================================\n")
	write_to_output_file_group(NUM_PER_ROW, NUM_PER_JOURNAL, group_dict, output, 'quality', "\n\n\n===QUALITY SPECIFIC============================================================\n")
	write_to_output_file_group(NUM_PER_ROW, NUM_PER_JOURNAL, group_dict, output, 'agency', "\n\n\n===ADOPTABLE AGENCIES==========================================================\n")
	write_to_output_file_group(NUM_PER_ROW, NUM_PER_JOURNAL, group_dict, output, 'misc', "\n\n\n===MISCELLANEOUS===============================================================\n")
	output.close()

# -----------------------------------------------------------
def write_to_stats_file(group_dict):
	output = open("stats.txt", 'w')
	output.write(str(len(group_dict)) + "\n\n")
	
	output.write("\n\n\n===DIRECTORY OF ALL GROUPS=====================================================\n")
	NUM_PER_ROW = 5
	NUM_PER_JOURNAL = 300
	counting = 0
	for group in (sorted(group_dict.values(), key=operator.attrgetter('name'))):
		counting += 1
		output.write(group.name.rstrip('\n'))
		output.write("    ".rstrip("\n"))
		if counting % NUM_PER_ROW == 0:
			output.write("\n")
		#if counting % NUM_PER_JOURNAL == 0:
		#	output.write("\n\n")
	# printout for data on the rest of the groups	
	write_to_output_file_group(NUM_PER_ROW, NUM_PER_JOURNAL, group_dict, output, 'all', "\n\n\n===ALL ADOPTS ACCEPTED=========================================================\n")
	write_to_output_file_group(NUM_PER_ROW, NUM_PER_JOURNAL, group_dict, output, 'species', "\n\n\n===SPECIES SPECIFIC============================================================\n")
	write_to_output_file_group(NUM_PER_ROW, NUM_PER_JOURNAL, group_dict, output, 'closed', "\n\n\n===CLOSED SPECIES==============================================================\n")
	write_to_output_file_group(NUM_PER_ROW, NUM_PER_JOURNAL, group_dict, output, 'fandom', "\n\n\n===FANDOM SPECIFIC=============================================================\n")
	write_to_output_file_group(NUM_PER_ROW, NUM_PER_JOURNAL, group_dict, output, 'payment', "\n\n\n===PAYMENT SPECIFIC============================================================\n")
	write_to_output_file_group(NUM_PER_ROW, NUM_PER_JOURNAL, group_dict, output, 'quality', "\n\n\n===QUALITY SPECIFIC============================================================\n")
	write_to_output_file_group(NUM_PER_ROW, NUM_PER_JOURNAL, group_dict, output, 'agency', "\n\n\n===ADOPTABLE AGENCIES==========================================================\n")
	write_to_output_file_group(NUM_PER_ROW, NUM_PER_JOURNAL, group_dict, output, 'misc', "\n\n\n===MISCELLANEOUS===============================================================\n")
	output.close()

# ===========================================================
if __name__ == "__main__":
	print "Starting up...."
	
	group_dict = {}
	convert_cd_file_with_spreadsheet_info(group_dict)
	
	
	DELETE_FLAG = raw_input("Do you want to delete any groups? (y/n):   ",)
	while DELETE_FLAG == "y":
		group_to_remove = raw_input("Group Name:   ",)
		group_to_remove = group_to_remove.lower()
		if group_dict.has_key((group_to_remove.lower())): # entry is already included
			del group_dict[(group_to_remove.lower())]
		DELETE_FLAG = raw_input("Continue? (y/n)   ",)

	print "-------------------------------------------"
	ADD_FLAG = raw_input("Do you want to add any groups? (y/n)   ",)
	if ADD_FLAG == "y":
		p = subprocess.Popen(["notepad.exe", "category_nums.txt"])
	while ADD_FLAG == "y":
		add_group_var = raw_input("Group Name:   ",)
		add_group_var = add_group_var.lower()
		categories_for_add_group = raw_input("Categories:   ",)
		categories_for_add_group = categories_for_add_group.split(" ")
		
		if group_dict.has_key(add_group_var): # entry is already included
			new_group = GROUP(add_group_var, categories_for_add_group)
			group_dict[add_group_var].merge_groups(new_group)
		else:
			group_dict[add_group_var] = GROUP(add_group_var, categories_for_add_group)
		
		ADD_FLAG = raw_input("Continue? (y/n)   ",)
		
	
	print "Saving to cd_file.txt....\n"
	write_to_cd_file(group_dict)
	print "Writing to output.txt....\n"
	write_to_output_file(group_dict)
	
	print "Done!" # the program then opens up the output.txt file in notepad
	p = subprocess.Popen(["notepad.exe", "output.txt"])
