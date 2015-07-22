'''
simple function created to parse through the journal data without
manual manipulation. Goal is to make it function with the object-oriented 
'''
import urllib2
from HTMLParser import HTMLParser
from string import whitespace
import re

# ===========================================================
object_array = []
text_file = open("testdata2.txt", "r")
groupNames = text_file.readlines()
text_file.close()

text_file2 = open("testdata.txt", "w")

for i in range(0, len(groupNames)):
	if groupNames[i][0] == " ":
		text_file2.write(groupNames[i][1:])
	else:
		text_file2.write(groupNames[i])
	#groupNames[i] = groupNames[i].translate(None, whitespace)
text_file2.close()
'''
	start = mystring.find( ':' )
	end = mystring.find( ':' )
	if start != -1 and end != -1:
		result = mystring[start+1:end]
	
	groupNames[i].split(" ")
	print "1) " + groupNames[i]
	groupNames[i] = groupNames[i].translate(None, whitespace)
	print "2) " + groupNames[i]
	print "~~ " + groupNames[i][0] + " .:. " + groupNames[i][0]
	'''
