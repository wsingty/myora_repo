#! /usr/bin/python

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
  if "EM ASR" not in d0:
    d0 = d0
    dx = dx
    dc = dc
    container_list.append(d0)
    cxlist.append(dx)
    con_list.append(dc)           # list containing serial number to ASR-site ID mapping
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



# --> This block of code will create the ASR-manager info table
flink = "https://fems.us.oracle.com/FEMSService/resources/femsservice/femsview/asrsiteid/"
sid_info = []                                   # list to hold ASR siteID info
sid_info2 = []                                  # list to hold ASR siteID info without activation email

for siteid in siteids:
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





# --> This block of code is for the ASR Validation report
TDlist = []
thxlist = []
tserials = []
tilomlist = []
texalist = []
tdlist1 = []
tdlist2 = [] 
for serial in assetInfoSerials:        
  file_name = serial + '.html'
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
      for line in table:                                            # eachline in the table is read
        line = str(line)                                            # convert eachline into string
        line = re.sub('<[^<]+?>', ' ', line)                        # remove html tags
        if "hostname" in line:                                      # check and see if "hostname" string in in the line
          l2 = line.replace("MOS hostnames","").strip()             # remove "MOS hostname" string and leave only the hostname values
          for eachline in assetinfo:                                # read eachline in the assetinfo list
            if serial in eachline:                                  # check to see if the serial in in the line
              l1 = eachline                                         # assign line to l1
              for eachline in test:                                 # get eachline in test list -> list that stores test events
                if serial in eachline:                              # check if serial is present in eachline
                  line = re.sub("testevent.*$", "", eachline)
                  #print(line)
                  line = line.split()                               # split the lines at whitespaces
                  seri = line[0]                                    # get the first index
                  seri = str(seri)                                  # convert to string
                  val = line[-1]                                    # get the last index
                  val = str(val)                                    # convert to a string variable
                  thxlist.append(seri+" "+val)                      # append serialNo+value of variable(receiverType)
              for i in thxlist:                                     # for each line in thxlist
                  i = i.split()                                     # split eachline at whitespaces
                  i = i[0]                                          # get first index
                  if i not in tserials:                             # if the serial is not in tserial list
                    tserials.append(i)                              # append to tserial - this will make sure duplicates are not included
              for eachline in thxlist:                              # for eachline in thxlist
                if "ILOM" in eachline:                              # check in ILOM keyword is in the line
                  if eachline not in tilomlist:                     # check to makre sure that line does not exist in tilom list
                    tilomlist.append(eachline)                      # this will append unique lines to the list
              for eachline in thxlist:
                if "EXADATA-SW,ADR" in eachline:                    # check if the line has EXADATA-SW,ADR keyword 
                  if eachline not in texalist:                      # check to makre sure that line does not exist in texalist
                    texalist.append(eachline)
              list3 = [str(x[0]) +" "+ x[1] for x in zip(tilomlist, texalist)]     # merge 2 lists (texalist $ tilomlist)
              list4 = []                                                           # empty list to store serial numbers from meged list3 list
              for line in list3:                                                   # for eachline in the merged list
                line = line.split()                                                # split at whitespaces
                line = line[0]                                                     # get first index - it has the serial numbers
                list4.append(line)                                                 # append them (serial numbers) to the list4
              list5 = list(set(tserials) - set(list4))                             # list5 will contain serial numbers not present in the merged list
              slist = []                                                           # blank list for getting the serialnumber and receiver type values 
              for i in list5:
                for line in test:
                  if i in line:
                    line = re.sub("testevent.*$","", line)                         # remove all lines after testevent keyword
                    line = line.strip()                                            # remove leading/trailing spaces
                    line = line.split()                                            # split lines at whitespaces
                    s1 = line[0]                                                   # get serial numbers at index0
                    s2 = line[-1]                                                  # get last index (receiver type)
                    s = s1 + " " + s2                                              # combine both to get a combo of serial number and receiver type line 
                    slist.append(s)                                                # append to slist
              list7 = list3+slist                                                  # list7 stores combined elements or list3 & slist
              for line in list7:
                if serial in line:
                    if "ILOM" in line:
                        val1 = "YES"
                    else:
                        val1 = "NO"
                    if "EXADATA-SW,ADR" in line:
                        val2 = "YES"
                    else:
                        val2 = "NO"
                    val = val1 + "  " + val2    
              #l0 = l1+"   "+l2+"   "+val+"   "+l5
              #print(l0)    
              for eachline in con_list3:
                if serial in eachline:                              # check is serial is in the lines of con_list3
                    eachline = eachline.split()                     # split those lines at whitespaces  
                    thesid = eachline[1]                            # get the siteID from the line after splitting it
                    for line in sid_info2:
                        if thesid in line:
                            line = line.split()
                            l6 = line[0]
                            l6 = l6.strip()
                            l1 = l1.replace("SWITCH 36", "SWITCH")
                            l1 = l1.replace("SUN NETWORK QDR INFINIBAND GATEWAY SWITCH", "SUN INFINIBAND SWITCH")
                            l1 = l1.replace("Sun Network QDR InfiniBand Gateway Switc", "SUN INFINIBAND SWITCH")
                            l1 = l1.replace("SUN DATACENTER INFINIBAND SWITCH", "SUN INFINIBAND SWITCH")
                            l0 = l1+"   "+l2+"   "+val+"   "+l5+"   "+l6
                            if l0 not in TDlist:
                                TDlist.append(l0)         



for i in TDlist:                    # append lines that do not have infiniband 
    if "INFINIBAND" not in i:
        tdlist1.append(i)

for i in TDlist:                    # append lines that have infiniband
    if "INFINIBAND" in i:
        i = i.replace("YES  NO","YES  NA")
        i = i.replace("NO  NO","NO  NA")
        tdlist2.append(i)       
            

TDlist = []
valhead = "ASR VALIDATION REPORT"
valvalues = "SerialNo Product-Description\tMOS-Hostnames\tILOM\tOS\tStatus\tASRM-Hostname"
TDlist.append(valhead)
TDlist.append(hblines)
TDlist.append(valvalues)
TDlist.append(hblines)
tdlist = tdlist1 + tdlist2
for i in tdlist:
    TDlist.append(i)
TDlist.append(hblines)


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






