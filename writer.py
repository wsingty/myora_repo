# This script is written in python 2.7.15

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time
import re
import getpass



print("Please ensure that mysrs.txt file has been updated with the SRNumbers \nand note.txt file with the message to be displayed on the SR\n")
print("NOTE: mysrs.txt and note.txt must be in the same directory/folder where this script resides")


# Getting the user to enter the SSO username and password of the account 
#my_username = raw_input('Enter your sso username: ')
#my_password = getpass.getpass('Enter your sso password: ')

my_username = "david.ingty@oracle.com"
my_password = "Solaris10"

# ChromeDriver is a separate executable that WebDriver uses to control Chrome. Please see: https://www.seleniumhq.org/download/
#Crome driver paths.
#chrome_driver_path = r"C:\webdrivers\chromedriver.exe"
chrome_driver_path = "C:\\webdrivers\\chromedriver"
#chrome_driver_path = "/Users/davidingty/Downloads/tree/chromedriver"
driver = webdriver.Chrome(chrome_driver_path)


# Open the webpage and Login with account details
driver.get('https://support.us.oracle.com/oip/faces/index.jspx')
link = driver.find_element_by_id('login')
link.click()

# clicking on the username and password field on the login page
usernameid = driver.find_element_by_id('sso_username')
passwordid = driver.find_element_by_id('ssopassword')

# Typing the values of username and password into the respective fields in login page and login
usernameid.send_keys(my_username + Keys.RETURN)
passwordid.send_keys(my_password + Keys.RETURN)

# click "I Agree" button
xpath0 = '//*[@id="_id2"]/div[1]/table[2]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td[1]/button'
btn = driver.find_element_by_xpath(xpath0)
btn.click()

# reading the list of SRs saved under mysrs.txt file
srlist = []
for srn in open('mysrs.txt').readlines():
	srn = srn.strip()
	if srn not in srlist:
		srlist.append(srn)


# removing all blank lines
filtered = filter(lambda x: not re.match(r'^\s*$', x), srlist)


summarydesc = "SR for potential ASR Misconfiguration effort (ASR Enabled)"
catagorydesc = "HW x86 ASR Proactive Issue"
componentdesc = "Auto Service Request (ASR) Issues"
subcomponentdesc = "Configuration"
line1 = "Automation has identified that WebSR# "
line2 = " was logged on an ASR Enabled System.\nThe ASR software should have recognized this disk fault and created an SR automatically.\nThis SR has been created proactively to investigate the issue."

# This is start of the LOOP - it will open SR page in MOS and perform the required action. 
def copytext(var1, field1):
  	words = []
	for line in var1:
		line = line.split("\n")
		words.append(line)

	for word in words:
	  field1.send_keys(word)
	  field1.send_keys(Keys.RETURN)


for srnumber in filtered:
	# Open the SR in MOS
	mos = 'https://mosemp.us.oracle.com/epmos/mos/sp/viewSr?srNumber='
	moslink = mos+srnumber
	#driver.set_page_load_timeout(40)
	driver.get(moslink)
	driver.implicitly_wait(300)
	# Opening the copy link:
	copylink1 = "https://support.us.oracle.com/oip/faces/secure/srm/sr/SRCreate.jspx?srNumber="
	copylink2 = "&queryTabName=Dynamic%20Query&srcreateOp=SRCopy"
	copylink = copylink1+srnumber+copylink2
	driver.get(copylink)

	summaryfield = driver.find_element_by_xpath('//input[@id="summary"]')
	descfield = driver.find_element_by_xpath('//textarea[@id="description"]')
	catagoryfield = driver.find_element_by_xpath('//input[@id="categoryDescription"]')
	componentfield = driver.find_element_by_xpath('//input[@id="componentDescription"]')
	subcomponentfield = driver.find_element_by_xpath('//input[@id="subcomponentDescription"]')
	severitydesc = driver.find_element_by_xpath('//input[@id="severity"]')
	line0 = line1+srnumber+line2

	time.sleep(7)
	copytext(summarydesc, summaryfield)

	catagoryfield.clear()
	time.sleep(3)
	componentfield.clear()
	time.sleep(3)
	subcomponentfield.clear()
	time.sleep(3)
 
	catagoryfield.send_keys(catagorydesc + Keys.TAB)
	time.sleep(3)

	componentfield.send_keys('Auto'+ Keys.TAB)
	time.sleep(3)
	
	subcomponentfield.send_keys('Con'+ Keys.TAB)
	time.sleep(3)

	severitydesc.clear()
	severitydesc.send_keys('3-Standard' + Keys.TAB)
	time.sleep(3)

	for line in line0:
		line = line.split("\n")
		descfield.send_keys(line)







	










'''


	

'''
