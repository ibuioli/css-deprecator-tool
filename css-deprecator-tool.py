############################################
#CSS Deprecator Tool

#Author: Ignacio Buioli

#Simple script for detect ids and classes on
#css files not used on html files.
############################################

import codecs	#import codecs
import re	#import re for search
import os.path	#import os.path
from os import walk	#import walk from os

styles = []	#List of css files path
files = []	#List of html files path

print("- CSS Deprecator Tool -")
print("\nListing files")

for dirpath, dirnames, filenames in walk("./"):
	for i in filenames:
		filename, ext = os.path.splitext(i)
		if ext == ".html" or ext == ".xml":
			files.extend( [(dirpath+'/'+i).replace("//","/")] )
		elif ext == ".css":
			styles.extend( [(dirpath+'/'+i).replace("//","/")] )
print("\n-----------------------\n")

objs = []
css = []

def getCSSObjs(style):
	cleanCom = re.sub(r'\*[\s\S]+?\*','', style)
	cleanFile = re.sub(r'[\,\>\<\+\:]',' ', cleanCom)
	cleanNL = " ".join(cleanFile.split("\n"))
	cleanStyle = re.sub('\s+',' ', cleanNL)
	splitProp = cleanStyle.replace('}','}\n')
	deleteProp = re.sub(r'[{@*&?].*[}@*&?]', ' ', splitProp)
	finalCleanNL = " ".join(deleteProp.split("\n"))
	finalCleanStyle = re.sub('\s+',' ', finalCleanNL)
	styleParts = finalCleanStyle.split(' ')
	cssElements = []
	for i in styleParts:
		sub = re.sub(r'\{.*', ' ', i)
		subClean = re.sub(r' ', '', sub)
		if subClean != '':
			if subClean.find('.') >= 0 or subClean.find('#') >= 0:
				cssElements.append(subClean)
	return cssElements

def getHTMLObjs(file):
	ids_final = []
	classes_final = []

	ids = re.findall('id="(.*?)"', file)	#Get Ids
	if ids:
		for i in ids:
			ids_final.extend(i.split(" "))

	classes = re.findall('class="(.*?)"', file)	#Get Classes
        if classes:
		for i in classes:
			classes_final.extend(i.split(" "))

	for i, val in enumerate(ids_final):
		ids_final[i] = "#"+val
	for i, val in enumerate(classes_final):
		classes_final[i] = "."+val

	return ids_final + classes_final

############################################

for i in styles:
    f = codecs.open(i, "r", "utf-8")
    css.extend(getCSSObjs(style = f.read()))
print("CSS Elements:")
print(css)

for i in files:
    f = codecs.open(i, "r", "utf-8")
    objs.extend(getHTMLObjs(file = f.read()))
print("\nHTML Elements:")
print(objs)

not_found = []

for element in css:
	if element not in objs:
		not_found.append(element)

print("\n-----------------------\n")
print("Results:")

#Print results
if not_found:
	print("Elements not Found:\n")
	for i in not_found:
		print(i)
else:
	print("All elements matches!")
