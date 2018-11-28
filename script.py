#! /usr/bin/python
# -*- coding: utf-8 -*- 

import os
import sys
import re
import difflib
from bs4 import BeautifulSoup
import urllib



# Getting the asset serial Numbers from the list_asset output
aserials = []
lserials = []
search_list = ['SNMP', 'SNMP,HTTP', 'ILOM', 'NA']

for eachline in open('list_asset.txt').readlines():
  if re.compile('|'.join(search_list),re.IGNORECASE).search(eachline):
    eachline = eachline.split()
    eachline = eachline[2]
    eachline = eachline.strip()
    if eachline not in aserials:
      aserials.append(eachline)
      #aserials.append("\n")  
  else:
    if eachline in aserials:
      continue
    else:  
      aserials.append(eachline)

lserials = filter(lambda x: not re.match(r'^\s*$', x), aserials)

templist = []
for eachline in lserials:
  eachline = eachline.replace("\n", "")
  if eachline not in templist:
    templist.append(eachline)

lserials = templist[::]    



# InstalledBase Operation - creating iserials and ibinfo list
mylist = []
mylist1 = [] 
mylist2 = []
iserials = []
info = []
ibinfo1 = []
ibinfo2 = []

with open('ib.txt') as f:
   f = f.readlines()
   for line in sorted(f):
     mylist.append(line)

for i in mylist:
  if any(re.findall(r"SERVER|ASSY,IB|,ZS", i)):
    mylist1.append(i)

for i in mylist1:
   if "Latest" in i:
     mylist2.append(i)

for i in mylist2:
   i = i.split()
   i = i[-3]
   iserials.append(i)

for i in mylist2:
    i = i.split()
    i = i[:-4]
    info.append(i)

for i in info:
 string = "".join(i)
 ibinfo2.append(string)

for i in iserials:
 string = "".join(i)
 ibinfo1.append(string)

ibinfo0 = zip(ibinfo1, ibinfo2)

ibinfo = []
for i in ibinfo0:
   i = "  ".join(i)
   i = i.replace("\(","").replace("\)","")
   ibinfo.append(i)


# Total Serials from IB and Assetlist
sumserials = []
def findsum(list1):
   for i in list1:
     if i not in sumserials:
       sumserials.append(i)

findsum(lserials)
findsum(iserials)

 
# comparing list_asset(lserials.txt) serials and IB(iserials.txt) serials:
missing1 = []
missing2 = []

def mis(outlist, inlist):
  for i in sumserials:
    if i not in inlist:
      outlist.append(i)


mis(missing1, lserials)                       # these serials are not in the list_asset but in IB
mis(missing2, iserials)                       # these serials are not in IB but in list_asset
num1 = len(lserials)                          # count the number of serials in list_asset:
num2 = len(iserials)                          # count the number of serials in InstalledBase:
nums = str(num1)+"            "+str(num2)     # Printing out num1 and num2 values in one line


# Find and print what serial number is missing in each list
x1list = []                # x1list will hold serials from list_asset and print "-" for missing ones
x2list = []                # x2list will hold serials from list_asset and print "-" for missing ones

def xfact(inlist, outlist):
  for i in sumserials:
    if i not in inlist:
      outlist.append("----------")
    else:
      outlist.append(i)       


xfact(lserials, x1list)          # What serials are missing in list_asset 
xfact(iserials, x2list)          # What serials are missing in IB 
x3list = zip(x1list, x2list)     # Zip both lists together - for side by side viewing


# Remove the unecessary characters to clean the output
x4list = []
for i in x3list:
  i = str(i)
  i = i.replace("(","").replace(")","").replace(",","").replace("'","")
  x4list.append(i)


# Adding headers for the output of list_asset VS InstalledBase serials 
line3 = "="*25
line4 = "="*25
title1 = "Asset-List Installed-Base"+"\n"
heading0 = title1+line3



# compare is a list that will print lserials and iserials side by side with headings
compare = []
compare.append(heading0)

for i in x4list:
  compare.append(i)

compare.append(line4)
compare.append(nums)


# Downloading the fems pages 
link = "https://fems.us.oracle.com/FEMSService/resources/femsservice/femsview/"
for serial in sumserials:
  url = link+serial
  outfile = serial+".html"
  urllib.urlretrieve(url, outfile)



# Creating the assetinfo list - it holds all asset serial and product info
collist = []
for serial in sumserials:
  try:
     filename = serial+".html"
     with open(filename) as html_file:
       soup = BeautifulSoup(html_file, "lxml")
       soupdata = soup.find_all('table')
       table = soupdata[3]
       for row in table:
          cols = row.findChildren(recursive=False)
          cols = [ele.text.strip().encode('utf-8') for ele in cols]
          collist.append(cols)
  except IndexError:
      pass

newcols = []
for i in collist:
   if "Own HB" not in i:
       newcols.append(i)

length = len(newcols)
i = 0
assetinfo = []
while i < length:
  a1 = newcols[i][0]
  a1 = str(a1)
  a1 = a1.replace(",", " ")
  a1 = re.sub("\(.*?\)","", a1)
  i = i+1
  if "EM ASR" not in a1:
    b1 = a1
    if "ORACLE_DATABASE" not in b1:
      c1 = b1
      if c1 not in assetinfo:
          assetinfo.append(b1)


line1 = "="*46 
line2 = "="*46
heading1 = "Assets in InstalledBase but NOT in assetlist:"
heading2 = "Assets in assetlist but NOT in InstalledBase:"
hl2 = heading2+"\n"+line2
hl1 = heading1+"\n"+line1 

notin_assetlist = []
notin_iblist = []
notin_iblist.append(hl2)
notin_assetlist.append(hl1)


# This function will create 2 new lists to hold more detailed info about serials and product info missing in IB or list_asset 
def notin(inlist, infolist, outlist):
  for serial in inlist:
    for line in infolist:
      if serial in line:
        outlist.append(line)

notin(missing1, ibinfo, notin_assetlist)
notin(missing2, assetinfo, notin_iblist)

notin_assetlist.append(line1)
notin_iblist.append(line2)



# Extracting container information 
#heading3 = "ID\t\tStatus OwnHB Product\tHostname\tTelemetry\tReceiver\t\tASR-Siteid\t\tActivation-email\tInformation"
heading3 = "ID\t\tStatus OwnHB Product\tHostname\tTelemetry\tReceiver\t\tActivation-email\tInformation"
line5 = "="*170
conhead = heading3+"\n"+line5
conlist = []
td_list = []

for serial in sumserials:
  try:
    filename = serial+".html"
    with open(filename) as html_file:
      soup = BeautifulSoup(html_file, "lxml")
      soupdata = soup.find_all('table')
      table3 = soupdata[3]
      for tr in table3:
        td = tr.findChildren(recursive=False)
        tdlist = [ele.text.strip().encode("utf-8") for ele in td]
        td_list.append(tdlist)
  except IndexError:
      pass 

container_list = []
cxlist = []
con_list = []
con_col = []
# word_line will be removed, the line below occurs after ever serial entry and needs to be removed to creae a gap/space
word_line = "ID  Status  Own HB  Product  Hostname  Telemetry  ASR Siteid  Activation email  Information"
del td_list[0]
length = len(td_list)
i = 0
while i < length:
  d1 = (td_list[i][0])
  d1 = re.sub(",.*?\(","(", d1)
  d2 = (td_list[i][1])
  d3 = (td_list[i][5])
  d4 = (td_list[i][7])
  d4 = d4.replace("SWITCH 36", "SWITCH").replace("SUN NETWORK QDR INFINIBAND GATEWAY SWITCH", "SUN INFINIBAND SWITCH")
  d4 = d4.replace("Sun Network QDR InfiniBand Gateway Switc", "SUN INFINIBAND SWITCH")
  d4 = d4.replace("SUN DATACENTER INFINIBAND SWITCH", "SUN INFINIBAND SWITCH")
  d5 = (td_list[i][8])
  d6 = (td_list[i][9])
  d7 = (td_list[i][10])
  d8 = (td_list[i][11])
  if d8 == "":
    d8 = "None"
  d9 = (td_list[i][12])
  d9 = d9.replace("No activation received","No-activation-received")
  if d9 == "":
    d9 = "None"
  d10 = (td_list[i][13])
  d10 = d10.replace("Override activation enabled","")
  d10 = re.sub("Container.*?:", "", d10)
  d10 = re.sub("Parent.*?:", "-Parent:", d10)
  if d10 == "":
    d10 = "None"
  #d0 = d1+"  "+d2+"  "+d3+"  "+d4+"  "+d5+"  "+d6+"  "+d7+"  "+d8+"  "+d9+"  "+d10
  d0 = d1+"  "+d2+"  "+d3+"  "+d4+"  "+d5+"  "+d6+"  "+d8+"  "+d9+"  "+d10
  d0 = d0.replace(word_line, " ")
  dx = d1+"#"+d2+"#"+d3+"#"+d4+"#"+d5+"#"+d6+"#"+d7+"#"+d8+"#"+d9+"#"+d10
  dx = dx.split("#")
  d1one = re.sub("\(.*?\)", "", d1)
  dc = d1one+"  "+d8
  dc = re.sub("ID  ASR Siteid", "", dc)
  d1alt = re.sub("\(.*?\)"," ",d1)
  dalt = d1alt+"  "+d5+"  "+d6 
  if "EM ASR" not in d0:
    d0 = d0
    dx = dx
    dc = dc
    dalt = dalt
    container_list.append(d0)
    cxlist.append(dx)
    con_list.append(dc)           # list containing serial number to ASR-site ID mapping
    if dalt not in con_col:
        con_col.append(dalt)        # list contains serialNo $ hostname & telemetryType mapping
  i = i+1

containerinfo = []
containerinfo.append(conhead)

for i in container_list:
  containerinfo.append(i)

containerinfo.append(line5) 


con_list2 = []
for i in con_list:
  if i not in con_list2:
    con_list2.append(i)

con_list3 = filter(None, con_list2)        # remove unwanted blank lines from the list


siteids = []                # siteids is a list that will hold the unique value of siteIDs of assets in the operation 
for i in con_list3:
   i = i.split()
   i = i[1]
   if i not in siteids:
    siteids.append(i)



# Extracting Testevents 
il = "ILOM"
ex = "EXADATA-SW,ADR"
fm = "FMA"
sc = "SCRK"
kl = []      # This list will contain most recent testevents 1 for each telemerey source
testline = "="*160 
test_headings = "Serial\t\tProduct\t\t\tHostname\t\tSource\tType\tReceived-Time\t\tEvent-Time"


def test_recent(source):
  for serial in sumserials:
    c = []
    for line in testevent_list:
      if serial in line:
        if source in line:
          line = line.split("\n")
          c.append(line)
          length = len(c)
          i = length - 1
          while i > 0:
            del c[i]
            i = i - 1
    for item in c:
      kl.append(item)

tab = {}
link ="https://fems.us.oracle.com/FEMSService/resources/femsservice/femsview/"
for serial in sumserials:
  try:
    a = []
    filename = serial+".html"
    with open(filename) as html_file:
     soup = BeautifulSoup(html_file, "lxml")
     table = soup.find_all('table')[5]
     for tr in table.find_all('tr'):
      td = [i for i in tr]
      a.append(td)
      tab[serial] = a
  except IndexError:
    pass



testevent_list = []
for keys,values in tab.items():
  for line in values:
    line = str(line)
    line = re.sub('<[^<]+?>', ' ', line)
    if "TESTCREATE" in line:
      line = re.sub("TESTCREATE.*$", "", line)
      line = re.sub("ASR-.*?\,", "", line)
      line = re.sub("testevent_.*?\,", "testevent ", line)
      line = line.replace("[    ","   ").replace(" ,","  ").replace("         ", "   ").replace(")    ", ")   ")
      line = line.replace("    ILOM", "   ILOM").replace("    EXADATA-SW,ADR", "   EXADATA-SW,ADR").replace("    FMA", "   FMA")
      line = line.replace("       testevent", "   testevent").rstrip()
      line = line.replace("SWITCH 36", "SWITCH")
      line = line.replace("SUN NETWORK QDR INFINIBAND GATEWAY SWITCH", "SUN INFINIBAND SWITCH")
      line = line.replace("Sun Network QDR InfiniBand Gateway Switc", "SUN INFINIBAND SWITCH")
      line = line.replace("SUN DATACENTER INFINIBAND SWITCH", "SUN INFINIBAND SWITCH") 
      testevent_list.append(str(keys) + line)



for keys,values in tab.items():
  for line in values:
    line = str(line)
    line = re.sub('<[^<]+?>', ' ', line)
    if "Audit event" in line: 
      line = re.sub("Audit event.*$","", line)
      line = re.sub("\w{8}-\w{4}-\w{4}-\w{4}-\w{12}", "audit-event", line)
      line = line.rstrip(" ,").rstrip("[0-9]+").replace(" ,", "").strip().rsplit(' ', 1)[0].strip()
      testevent_list.append(str(keys) + line)


test_recent(il)
test_recent(ex)
test_recent(fm)
test_recent(sc)


wlist = []        # this list will store unique serial numbers that have generated 
for line in kl:
  line = str(line)
  line = line.split()[0].replace("[","").replace("'","").replace("]","").strip()    # get 1st column with serial numbers and remove extra wild characters. 
  if line not in wlist:                                                             # append unique serial numbers to wlist
      wlist.append(line)


test = []                        
#for serial in sumserials:
for serial in wlist:  
  ulist = []
  for line in kl:
    line =str(line)
    if serial in line:
      ulist.append(line)
  c = len(ulist)
  ulist.insert(c, "")
  for i in ulist:
    i = i.replace("[","").replace("]","").replace("'", "")
    test.append(i)


tests = []
tests.append(test_headings)
tests.append(testline)

test.pop()
for i in test:
  tests.append(i)

tests.append(testline) 





# Added 2018-10-8
# Heartbeat Information - Extracting Hb info frm FEMS
hbhead = "ASSET HEARTBEAT INFORMATION (Upto 7 entries)" 
hblines = "="*100

tableinfo = []
try:
  for serial in sumserials:
    hblink = "https://fems.us.oracle.com/PersistenceService/resources/persistenceservice/nph/heartbeatfull/"
    url = hblink+serial
    sauce = urllib.urlopen(url).read()
    soup = BeautifulSoup(sauce, 'lxml')
    table = soup.find_all('table')[1]
    table_rows = table.find_all('tr')
    for td in table_rows:
      td = td.find_all('td')
      td = str(td)
      td = re.sub('<[^<]+?>', '', td)
      td = re.sub("SUN.*$", "", td)
      td = re.sub("ORACLE.*$", "", td)
      td = re.sub("Sun.*$", "", td)
      td = re.sub("SPARC.*$", "", td)
      td = td.replace("[","").replace("]","")
      td = re.sub("\d\d:\d\d:\d\d", "", td)
      td = td.strip()
      td = td.rstrip(',')
      td = re.sub(",.*?,", "+", td)
      td = re.sub("\+.*?,", "", td)
      if td not in tableinfo:
        tableinfo.append(td)
except IndexError:
    pass      

tableinfo = filter(None, tableinfo)


heart = []
a = {}
b = []
for serial in sumserials:
  for line in tableinfo:
    if serial in line:
      line = re.sub("\s.*$"," ",line)
      line = line.strip()
      b.append(line)
      b = b[0:7]
      c = list(dict.fromkeys(b))
      final_list = [] 
      for num in c: 
        if num not in final_list: 
            final_list.append(num)
            final_list.sort()
            a[serial] = final_list

heart.append(hbhead)
heart.append(hblines)

for keys,values in a.items():
    val = "  ".join(values)
    keys = keys + ": "
    h = keys+" "+val
    heart.append(h)

heart.append(hblines)


assetInfoSerials = []
assetInfoSerials = [i.split()[0] for i in assetinfo if i not in assetInfoSerials]      # get unique serial numbers from assetinfo



newcon_col = []
for serial in sumserials:
  for line in con_col:
    if serial in line:
      if line not in newcon_col:  
        newcon_col.append(line)



# ---> pre validation report analysis
ncc1 = []
ncc2 = []
ncc3 = []
ncc4 = []
ncc5 = []
ncc6 = []
ncc7 = []
ncc8 = []
ncc9 = []
ncc10 = []

def ncc(nccx, x):
  for serial in sumserials:
    for line in newcon_col:
      if serial in line:
        if x in line:
          if line not in nccx:
            nccx.append(line)

def nccx(x,y):
  for i in y:
    i = i.split()
    i = i[0]
    if i not in x:
      x.append(i)            

def finder(listx, listy):
  for serial in ncc6:
    for line in listx:
      if serial in line:
        if line not in listy:
          listy.append(line)


ncc(ncc1, "ILOM")
ncc(ncc2, "EXADATA-SW,ADR")
ncc3 = [str(x[0]) +" "+ x[1] for x in zip(ncc1, ncc2)]            # zipping both ILOM and EXadata serials to make ONE line

nccx(ncc4, ncc3)                                                  # get serial numbers that were zipped successfully
nccx(ncc5, ncc1)                                                  # ncc5 list will contain unique serial numbers of ncc1 & ncc2 -> total serials
nccx(ncc5, ncc2)                                                  # ncc5 list will contain unique serial numbers of ncc1 & ncc2 -> total serials
ncc6 = (set(ncc5) - set(ncc4))                                    # ncc6 list will contains what serials were not zipped

finder(ncc1, ncc7)                                                # get full details for serials not zipped
finder(ncc2, ncc7)                                                # get full details for serials not zipped
ncc8 = ncc3 + ncc7                                                # map -> 




for eachline in ncc8:
  try:
    if "ILOM" and "EXADATA" in eachline:
      line = eachline.split()
      del line[2]
      del line[2]
      del line[-1]
      s1 = line[0]
      s2 = line[1]
      s3 = line[2]
      if s2 == "":
        s2 = " - "
      if s3 == "":
        s3 = " - "
      s0 = s1+"   "+s2+"   "+s3     
      if s0 not in ncc9:
          ncc9.append(s0)
  except:
    pass


for eachline in ncc8:
  try:
    s3 = ""
    if "ILOM" in eachline:        
      if "EXADATA-SW,ADR" not in eachline:
          line = eachline.split()
          del line[2]
          s1 = line[0]
          s2 = line[1]
          try:
            s3 = line[2]
          except:
            pass
          if s3 == "":
            s3 = " --- "    
          s0 = s1+"   "+s2+"   "+s3
          if s0 not in ncc9:
            ncc9.append(s0)
  except:
    pass


for i in ncc9:
  i = i.split()
  x1 = i[2]
  x2 = i[1]
  x3 = i[0]
  x0 = x3+"   "+x2+"   "+x1
  if x0 not in ncc10:
    ncc10.append(x0)


ncc11 = []
for line in assetinfo:
  l1 = line
  l1 = l1.replace("SWITCH 36", "SWITCH")
  l1 = l1.replace("SUN NETWORK QDR INFINIBAND GATEWAY SWITCH", "SUN INFINIBAND SWITCH")
  l1 = l1.replace("Sun Network QDR InfiniBand Gateway Switc", "SUN INFINIBAND SWITCH")
  l1 = l1.replace("SUN DATACENTER INFINIBAND SWITCH", "SUN INFINIBAND SWITCH")
  if l1 not in ncc11:
    ncc11.append(l1)


ncc12 = [str(x[0]) +" "+ x[1] for x in zip(ncc11, ncc10)]

ncc13 = []
for i in ncc12:
  i = i.split()
  del i[4]
  i2 = i[-2:]
  i2 = str(i2)
  i1 = i[0:4]
  i1 = str(i1)
  i = i1+"   "+i2
  i = i.replace("'","").replace("[","").replace("]","").replace(",","")
  if i not in ncc13:
    ncc13.append(i)



tcc1 = []
tcc2 = []

def tcc(tccx, x):
  for serial in sumserials:
    for line in test:
      if serial in line:
        if x in line:
          line = re.sub("testevent.*$", "", line)
          line = line.split()
          seri = line[0]                                    # get the first index
          seri = str(seri)                                  # convert to string
          val = line[-1]                                    # get the last index
          val = str(val)                                    # convert to a string variable
          line = seri+"   "+val
          if line not in tccx:
            tccx.append(line)
      if serial not in line:
        if x == "ILOM":
          val = "NOILOMTESTEVENT"
          line = serial+"   "+val
          if line not in tccx:
            tcc1.append(line)
      if serial not in line:
        if x == "EXADATA-SW,ADR":
          val = "NOEXATESTEVENT"
          line = serial+"   "+val
          if line not in tccx:
            tcc2.append(line)      


tcc(tcc1, "ILOM")
tcc(tcc2, "EXADATA-SW,ADR")

















# --> This block of code will create the ASR-manager info table
flink = "https://fems.us.oracle.com/FEMSService/resources/femsservice/femsview/asrsiteid/"
sid_info = []                                   # list to hold ASR siteID info
sid_info2 = []                                  # list to hold ASR siteID info without activation email

for siteid in siteids:
  try:    
      siteid = siteid.strip()                                         # remove leading/trailing whitespaces
      fflink = flink+siteid                                           # creating specific siteid link
      sauce = urllib.urlopen(fflink).read()                           # opening the siteID link
      soup = BeautifulSoup(sauce, 'lxml')                             # parsing the siteID link
      soupdata = soup.find_all('table')                               # finding all tables in the page
      table = soupdata[2]                                             # capturing table index 2
      for line in table:
        line = str(line)                                              # eacline is converted to a string
        if "Marked as container" in line:                             # check if eachline contains keyword "Marked"
          line = str(line)                                            # convert that to string
          line = line.split("Marked")                                 # split the string at the keyword "Marked"
          line = line[0]                                              # get the first half of the split string
          line = re.sub('<[^<]+?>', ' ', line)                        # remove all html tags
          line = line.replace(" No activation received", " No-activation-received")
          line = line.split()                                         # split line again at whitespace
          line = line[-5:]                                            # get the last 5 elements of the list
          del line[1]                                                 # delete element index1 (source type) from the list
          sline = line
          sline0 = sline[0]                                                 # ASRM-hostname
          sline1 = sline[1]                                                 # Receiver
          sline2 = sline[2]                                                 # ASRsiteID
          sline3 = sline[3]                                                 # ActivationEmail
          newsline = sline0 +"  "+ sline1 +"  "+ sline2 +"  "+ sline3       # ASRM-hostname, receiver, asrsisteID, activation-email
          aline = sline0 +"  "+ sline1 +"  "+ sline2                        # ASRM-hostname, receiver, asrsisteID
          if newsline not in sid_info:
            sid_info.append(newsline)                                       # append the line to sid_info list
          if aline not in sid_info2:  
            sid_info2.append(aline)                                         # append the line to sid_info2 list
  except:
        pass




xserials = []         # list will store infiniband serial numbers from test events (unique ones)
for i in test:
  if "INFINI" in i:
    i = i.split()
    i = i[0]            # index 0 will extract IB switch serial
    if i not in xserials:
      xserials.append(i)


# --> This block of code is for the ASR Validation report
TDlist = []
thxlist = []
tserials = []
tilomlist = []
texalist = []
tdlist1 = []
tdlist2 = []
tdlist3 = [] 

#for serial in assetInfoSerials:
for serial in sumserials:         
  file_name = serial + '.html'
  try:
      with open(file_name) as html_file:                                # open the html file from fems for parsing
          soup = BeautifulSoup(html_file, 'lxml')                       # start parsing the html file with BeautifulSoup
          soupdata = soup.find_all('table')                             # Get all tables in teh html file
          table = soupdata[1]                                           # get table index 1
          ntable = soupdata[0]                                          # get the table index 0
          for eachline in ntable:                                       # eachline that is in table[0]
            nline = str(eachline)                                       # convert eachline to a string
            nline = re.sub('<[^<]+?>', ' ', nline)                      # remove all html tags
            nline = re.sub(".*?ASR Status","ASR Status", nline)         # remove all before "ASR Status" keyword
            nline = nline.strip()                                       # remove all leading and trailing spaces
            if "ASR Status" in nline:                                   # if ASR Status is in the line
              nline = nline.split("MOS")                                # break the line where teh keyword "MOS" occurs
              l5 = nline[0].strip().replace("ASR Status:","").strip()   # strip leading/trailing spaces and remove ASR Status word
  except:
    pass               


# IMPORTANT LIST NAMES:
#===========================================================================================
# lserials    -> list with asset serials
# iserials    -> list with ib serials
# sumserials  -> total serials from ibserials and assetserials
# ibinfo      -> IB table map info {"serial":"Product Description"} 
# assetinfo   -> Asset table map info {"serial":"Product Description"}
# compare     -> Table that shows both IB serials and Asset serials side by side
# missing1    -> What is missing in Asset serials but presen in IB
# missing2    -> What is missing in IB serials but present in Asset serials
# notin_assetlist -> What serial and corresponding product is misisng from the assetlist
# notin_iblist    -> What serial and corresponding product is misisng from the IBlist
# containerinfo  -> Contains container info
# testeventlist & testinfo  -> Contains testevents list
# test   -> final testevent list
# serials_with_testevents     -> Asset serials with testevents
# serials_without_testevents  -> Asset serials with no testevents



for i in compare: 
  print(i)

print "\n"*2
if missing1:
  for i in notin_assetlist: 
    print(i)

if missing1: 
  print("\n")

if missing2:
  for i in notin_iblist: 
    print(i) 

if missing2: 
  print("\n")

print("\n")*2
for i in containerinfo: 
  print(i)

print("\n")*2
for i in tests: 
  print(i)

print("\n")*2
for i in heart: 
  print(i)

print("\n")*2
for i in TDlist: print i





#modified on 2018.11.02 
"""
              l5 = re.sub("No active contract","No-active-contract", l5)
              l5 = re.sub("Pending activation approval in My Oracle Support","Pending-MOS", l5)
              l5 = re.sub("ASR has been De-Activated","De-Activated", l5)
              l5 = re.sub("No active contract","No-active-contract", l5)
              l5 = re.sub("Deactivated","Deactivated", l5)
              l5 = re.sub("Asset serial number is not found in My Oracle Support. Please contact Oracle Support Services","Serial-Not-Found-in-MOS", l5) 
"""
              