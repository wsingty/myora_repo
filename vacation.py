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
my_username = raw_input('Enter your sso username: ')
my_password = getpass.getpass('Enter your sso password: ')


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


# This is start of the LOOP - it will open SR page in MOS and perform the required action. 
for srnumber in filtered:
	# Open the SR in MOS
	mos = 'https://mosemp.us.oracle.com/epmos/mos/sp/viewSr?srNumber='
	moslink = mos+srnumber
	#driver.set_page_load_timeout(40)
	driver.get(moslink)
	#driver.maximize_window()
	driver.implicitly_wait(300)
	driver.find_element_by_xpath('//*[@id="mouse_shortcuts"]/table/tbody/tr[2]/td[1]/a').click()
	time.sleep(3)
	tarea = driver.find_element_by_xpath('//textarea[@title="Comments"]')
	time.sleep(3)


	words = []
	for line in open('note.txt').readlines():
		line = line.split("\n")
		words.append(line)

	for word in words:
	  tarea.send_keys(word)
	  tarea.send_keys(Keys.RETURN)

	i = 0
	while i < 5:
	  driver.find_element_by_tag_name('body').send_keys(Keys.TAB)
	  i += 1

	driver.find_element_by_tag_name('body').send_keys(Keys.TAB + Keys.RETURN)
	time.sleep(10)
	

driver.quit()
