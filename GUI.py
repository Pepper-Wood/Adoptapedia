import webbrowser
import Tkinter
from Tkinter import *
import ttk
import Tkinter,tkFileDialog
#import datetime
#from PIL import Image, ImageTk
#import os, sys
#import time, math
#import zhinst.ziPython, zhinst.utils
#import matplotlib
#import matplotlib.pyplot as plt
#from numpy import *

root = Tk()
root.title("Adoptapedia")

buttons = [ 'Add Groups',  'Delete Groups',  'Generate WC' ]

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

# -----------------------------------------------------------
def load_data():
	print "cool"
	'''
	object_array = []
	text_file = open("all_data.txt", "r")
	groupNames = text_file.readlines()
	text_file.close()
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
	'''
	
# -----------------------------------------------------------
def add_groups():
	print "adding groups....."

# -----------------------------------------------------------
def delete_groups():
	print "deleting groups..."

# -----------------------------------------------------------
def updateWC():
	print "updating WC......."

# -----------------------------------------------------------
def saveAndQuit():
	# print out the data to all_data.txt
	# destroy window
	
	# Open text files to change Adoptapedia journals
	webbrowser.open("all_data.txt")
	root.destroy()
	
# create a toplevel menu
menubar = Menu(root)
menubar.add_command(label="Save&Quit!", command=saveAndQuit)
menubar.add_command(label="Quit!", command=root.destroy)
root.config(menu=menubar)
	
# set up GUI
Button(root, text = buttons[0], command = add_groups).grid(row = 0, sticky =W+E+N+S, ipadx = 60, padx = 5, pady = 5, columnspan=3)
Button(root, text = buttons[1], command = delete_groups).grid(row = 1, sticky =W+E+N+S, ipadx = 60, padx = 5, pady = 5, columnspan=3)
Button(root, text = buttons[2], command = updateWC).grid(row = 2, sticky =W+E+N+S, ipadx = 60, padx = 5, pady = 5, columnspan=3)


# RUNTIME
load_data() #get all_data.txt into an OOD structure
root.mainloop()
