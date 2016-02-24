# STEP 1) Create a parsing function for the "groups to add" google form
# STEP 2) Create a parsing function for pre-existing groups
# STEP 3) Merge the two
#		-- duplicate entries have their categories merged
#		  -- i.e. "GroupA" is in the "Species specific" category
#		  -- "GroupA" already exists in "Payment specific" category
#		  -- "GroupA" now exists in "Species Specific" and "Payment specific" categories

# STEP 4) Parse a given webpage and update watcher count for directory
# STEP 5) Parsing a Google Doc of groups to delete
#		-- removes entries from the over-arching data structure
#      -- clear the document when finished

# STEP 6) Formatting outputs to pre-existing spreadsheet and the journal-formatted outputs
# STEP 7) Script to automatically update deviantArt pages????

# It'd be awesome to hook this up to a raspberry pi and have the code automatically run at
#  the end of every day or so.

import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
import operator
import subprocess

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
# param: form_responses0 = a list of lists for all the cells in one of the spreadsheets
#        dict = a dictionary that will be populated
#        form_flag = True if form responses, False if current dictionary
# modifies: dict = a dictionary of GROUP objects
def convert_spreadsheet_info(form_responses0, dict, form_flag):
	q = 0
	if form_flag: q = 1
	for i in range(1, len(form_responses0)): #starts at 1 to avoid the first line
		# iterate over each row
		# form_responses0[i][q] :: name of group
		# form_responses0[i][q+1] :: string of categories (separated by commas)
		if dict.has_key(form_responses0[i][q].lower()): # entry is already included
			new_group = GROUP(form_responses0[i][q],form_responses0[i][q+1].split(','))
			dict[form_responses0[i][q].lower()].merge_groups(new_group)
		else: # create a new entry
			dict[form_responses0[i][q].lower()] = GROUP(form_responses0[i][q],form_responses0[i][q+1].split(','))

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

# -----------------------------------------------------------	
def erase_spreadsheet(spreadsheet):
	done_flag = False # flips once an empty cell is reached
	counter = 0
	while not done_flag:
		counter += 1
		if counter == spreadsheet.row_count:
			done_flag = True
		elif spreadsheet.cell(counter,1).value == None or spreadsheet.cell(counter,1).value == "":
			done_flag = True
		else:
			spreadsheet.update_cell(counter,1,"")
			spreadsheet.update_cell(counter,2,"")
			spreadsheet.update_cell(counter,3,"")

# -----------------------------------------------------------
def remove_groups(group_dict):
	delete_file = open("delete.txt", 'r')
	for line in delete_file:
		if group_dict.has_key((line.lower())): # entry is already included
			del group_dict[(line.lower())]
	delete_file.close()
	open("delete.txt", 'w').close() # erases the text file

# -----------------------------------------------------------
def write_to_spreadsheet(group_dict):
	count = 1
	for group in (sorted(group_dict.values(), key=operator.attrgetter('name'))):
		print count,
		cd.update_cell(count,1,group.name)
		cd.update_cell(count,2,(', '.join(group.categories)))
		count += 1

# -----------------------------------------------------------
def write_to_cd_file(group_dict):
	cd_file = open("cd_file.txt", 'w')
	for group in (sorted(group_dict.values(), key=operator.attrgetter('name'))):
		cd_file.write(str(group.name) + " " + str((' '.join(group.categories))) + "\n")
	cd_file.close()

# -----------------------------------------------------------
def write_to_output_file(group_dict):
	output = open("output.txt", 'w')
	output.write(str(len(group_dict)) + "\n\n")
	output.write("\n\n\nhttp://adoptapedia.deviantart.com/journal/Directory-List-of-All-Registered-Groups-357048592\n")
	NUM_PER_ROW = 5
	NUM_PER_JOURNAL = 200
	counting = 0
	for group in (sorted(group_dict.values(), key=operator.attrgetter('name'))):
		counting += 1
		output.write(group.print4journals().rstrip('\n'))
		output.write("    ".rstrip("\n"))
		if counting % NUM_PER_ROW == 0:
			output.write("\n")
		if counting % NUM_PER_JOURNAL == 0:
			output.write("\n\n")
		
	counting = 0
	output.write("\n\n\nhttp://adoptapedia.deviantart.com/journal/Directory-All-Adopts-Accepted-Groups-356536839\n")
	for group in (sorted(group_dict.values(), key=operator.attrgetter('name'))):
		if 'all' in group.categories:
			counting += 1
			output.write(group.print4journals().rstrip('\n'))
			output.write("    ".rstrip("\n"))
			if counting % NUM_PER_ROW == 0:
				output.write("\n")
	counting = 0
	output.write("\n\n\n===SPECIES SPECIFIC============================================================\n")
	for group in (sorted(group_dict.values(), key=operator.attrgetter('name'))):
		if 'species' in group.categories:
			counting += 1
			output.write(group.print4journals().rstrip('\n'))
			output.write("    ".rstrip("\n"))
			if counting % NUM_PER_ROW == 0:
				output.write("\n")
	counting = 0
	output.write("\n\n\n===CLOSED SPECIES==============================================================\n")
	for group in (sorted(group_dict.values(), key=operator.attrgetter('name'))):
		if 'closed' in group.categories:
			counting += 1
			output.write(group.print4journals().rstrip('\n'))
			output.write("    ".rstrip("\n"))
			if counting % NUM_PER_ROW == 0:
				output.write("\n")
	counting = 0
	output.write("\n\n\n===FANDOM SPECIFIC=============================================================\n")
	for group in (sorted(group_dict.values(), key=operator.attrgetter('name'))):
		if 'fandom' in group.categories:
			counting += 1
			output.write(group.print4journals().rstrip('\n'))
			output.write("    ".rstrip("\n"))
			if counting % NUM_PER_ROW == 0:
				output.write("\n")
	counting = 0
	output.write("\n\n\n===PAYMENT SPECIFIC============================================================\n")
	for group in (sorted(group_dict.values(), key=operator.attrgetter('name'))):
		if 'payment' in group.categories:
			counting += 1
			output.write(group.print4journals().rstrip('\n'))
			output.write("    ".rstrip("\n"))
			if counting % NUM_PER_ROW == 0:
				output.write("\n")
	counting = 0
	output.write("\n\n\n===QUALITY SPECIFIC============================================================\n")
	for group in (sorted(group_dict.values(), key=operator.attrgetter('name'))):
		if 'quality' in group.categories:
			counting += 1
			output.write(group.print4journals().rstrip('\n'))
			output.write("    ".rstrip("\n"))
			if counting % NUM_PER_ROW == 0:
				output.write("\n")
	counting = 0
	output.write("\n\n\n===ADOPTABLE AGENCIES==========================================================\n")
	for group in (sorted(group_dict.values(), key=operator.attrgetter('name'))):
		if 'agency' in group.categories:
			counting += 1
			output.write(group.print4journals().rstrip('\n'))
			output.write("    ".rstrip("\n"))
			if counting % NUM_PER_ROW == 0:
				output.write("\n")
	counting = 0
	output.write("\n\n\n===MISCELLANEOUS SPECIFIC======================================================\n")
	for group in (sorted(group_dict.values(), key=operator.attrgetter('name'))):
		if 'misc' in group.categories:
			counting += 1
			output.write(group.print4journals().rstrip('\n'))
			output.write("    ".rstrip("\n"))
			if counting % NUM_PER_ROW == 0:
				output.write("\n")
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
	p = subprocess.Popen(["notepad.exe", "delete.txt"])
	p = subprocess.Popen(["notepad.exe", "cd_file.txt"])
	
	
	'''
	# print tests=================================
	for i in range(0, len(form_responses)):
		for j in range(0, len(form_responses[i])):
			print form_responses[i][j] + "  |  ",
		print ""

	# write to second worksheet
	cell_list = cd.range('A1:C7')
	for cell in cell_list:
		cell.value = '0_o'
	cd.update_cells(cell_list)
	'''
