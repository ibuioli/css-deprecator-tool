############################################
#CSS Deprecator Tool

#Author: Ignacio Buioli

#Simple script for detect ids and classes on
#css files not used on html files.

############################################

import codecs	#import codecs
import re	#import re for search

styles = ["styles.css"]	#Load css files path
files = [""]	#Load html files path

objs = []
css = []

def getCSSObjs(style):
	cleanNL = " ".join(style.split("\n"))
	cleanStyle = re.sub('\s+',' ', cleanNL)
	styleParts = cleanStyle.split("}")
	cssElements = []
	for i in styleParts:
		sub = re.sub(r'\{.*', ' ', i)
		subClean = re.sub(r' ', '', sub)
		if subClean != '':
			cssElements.append(subClean)
	return cssElements;

def getHTMLObjs(file):
	ids_final = []
	classes_final = []

	ids = re.findall('id="(.*?)"', file)	#Get Ids
	if ids:
                for i in ids:
                        ids_final = ids_final + i.split(" ")

	classes = re.findall('class="(.*?)"', file)    #Get Classes
        if classes:
		for i in classes:
			classes_final = classes_final + i.split(" ")

	for i, val in enumerate(ids_final):
		ids_final[i] = "#"+val
	for i, val in enumerate(classes_final):
                classes_final[i] = "."+val

	return ids_final + classes_final;

for i in styles:
        f = codecs.open(i, "r", "utf-8")
        css = css + getCSSObjs(style = f.read())
print("CSS Elements:")
print(css)

for i in files:
        f = codecs.open(i, "r", "utf-8")
        objs = objs + getHTMLObjs(file = f.read())
print("HTML Elements:")
print(objs)
print("-----------------------")

not_found = []

for element in css:
	print(element)
	if element not in objs:
		not_found.append(element)

print("-----------------------")
print("Results:")
#Print results
if not_found:
	print("Elements not Found:")
	print(not_found)
else:
	print("All elements matches!")
