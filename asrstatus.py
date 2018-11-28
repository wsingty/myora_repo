#! /usr/bin/python

import re
import requests
from bs4 import BeautifulSoup
import os
import ssl



print "Enter/Paste the Serial NUmbers. Once done press Ctrl-D to save and continue:"
contents = []
while True:
    try:
        line = raw_input("")
    except EOFError:
        break
    contents.append(line)


os.system('cls||clear')
print("Please wait while script is executing...")

sumserials = []
for serial in contents:
  if serial not in sumserials:
    sumserials.append(serial)


link = "https://fems.us.oracle.com/FEMSService/resources/femsservice/femsview/"

for serial in sumserials:
	serial = serial.replace("\n","")
	url = link+serial
	outfile = serial+".html"
	r = requests.get(url)
	open(outfile, 'w').write(r.content)


asset_stat = []

for serial in sumserials:
	serial = serial.replace("\n","")
	filename = serial+".html"
	with open(filename) as html_file:
		soup = BeautifulSoup(html_file, "lxml")
		soupdata = soup.find_all('h3')
		for eachline in soupdata:
			status = eachline.text
			status = status.replace("ASR Status:", "")
			line = serial+"  "+status
			if line not in asset_stat:
				asset_stat.append(line)


heading = "SERIAL-NUMBER  ASR-STATUS"
dash = "="*40

report = []
report.append(heading)
report.append(dash)
for i in asset_stat:
	if i not in report:
		report.append(i)

report.append(dash)

for serial in sumserials:
	serial = serial.replace("\n","")
	filename = serial+".html"
	if os.path.exists(filename):
		os.remove(filename)
	else:
		pass


os.system('cls||clear')
for i in report: print(i)















