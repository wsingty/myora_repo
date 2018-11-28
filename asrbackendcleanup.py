from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import re
import getpass


# Getting the user to enter the SSO username and password of the account 
my_username = raw_input('Enter your sso username: ')
my_password = getpass.getpass('Enter your sso password: ')


chrome_options = Options()
#chrome_options.add_argument("--headless")
#chrome_options.add_argument("--log-level=3");
chrome_driver_path = "C:\\webdrivers\\chromedriver.exe"       
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver_path)


# Open the webpage and Login with account details
asr_portal = "https://asrportal.us.oracle.com/asr/faces/EventSearch?"
driver.get(asr_portal)
#driver.maximize_window()
#link = driver.find_element_by_id('login')
#link.click()

# clicking on the username and password field on the login page
usernameid = driver.find_element_by_id('sso_username')
passwordid = driver.find_element_by_id('ssopassword')

# Typing the values of username and password into the respective fields in login page and login
usernameid.send_keys(my_username + Keys.RETURN)
passwordid.send_keys(my_password + Keys.RETURN)

# ASR Operation console tab
driver.find_element_by_xpath('//*[@id="pt1:sdi3::head"]/table/tbody/tr/td[3]/table/tbody/tr/td[2]/span').click()
time.sleep(3)

# click Cleanup asset link
driver.find_element_by_xpath('//a[@id="pt1:cl10"]').click()
time.sleep(3)


serials = []
#for serial in open('/root/py/myserials.txt').readlines():
for serial in open('C:\\webdrivers\\myserials.txt').readlines():
   serial = serial.strip()
   if serial not in serials:
     serials.append(serial)

serials = filter(lambda item: item, serials)

def tabfun():
	try:
		time.sleep(3)
		table = table = driver.find_element_by_xpath('//*[@id="pt1:pt_region0:1:t_assetComponents::db"]/table').get_attribute('outerHTML')
		line = re.sub(".*?_rowcount", "", table)
		line = re.sub("_startrow.*$", "", line)
		line = line.replace("\"","").replace("=","").replace("\'","")
		line = line.strip()
		rows = line.encode("utf-8")
		l = int(rows)
		l = l + 1
		return l
	except:
	    pass



def delete():
	try:
		driver.find_element_by_xpath('//*[@id="pt1:pt_region0:1:cb2"]').click()
		time.sleep(3)
		#driver.find_element_by_xpath('//button[contains(text(), "Confirm Delete this AssetComponent")]').click()
		driver.find_element_by_xpath('//*[@id="pt1:pt_region0:2:cb3"]').click()
		time.sleep(3)
		button2 = driver.find_element_by_xpath('//button[contains(text(), "Done")]')
		button2.click()
		#driver.find_element_by_xpath('//a[@id="pt1:cl10"]').click()
		#driver.find_element_by_xpath('//a[@id="pt1:cl10"]').click()
		adding(d0)
		time.sleep(3)
		#driver.find_element_by_xpath('//*[@id="pt1:pt_cil1::icon"]').click()
	except:
		pass



def resetandsearch():
	try:
		driver.find_element_by_xpath('//button[@id="pt1:pt_region0:1:assetSearchQuery::reset"]').click()
		time.sleep(3)
		searchbox = '//*[@id="pt1:pt_region0:1:assetSearchQuery:val00::content"]'
		time.sleep(1)
		driver.find_element_by_xpath(searchbox).click()
		driver.find_element_by_xpath(searchbox).send_keys(serial + Keys.RETURN)
	except:
		pass



def deactivate():
    time.sleep(3)
    dec1 = '//*[@id="pt1:pt_region0:1:cb1"]'
    dec2 = '//*[@id="pt1:pt_region0:2:cb1"]'
    driver.find_element_by_xpath(dec1).click()
    time.sleep(3)
    driver.find_element_by_xpath(dec2).click()
    time.sleep(3)
    button = driver.find_element_by_xpath('//button[contains(text(), "Done")]')
    button.click()
    time.sleep(3)
    driver.find_element_by_xpath('//a[@id="pt1:cl10"]').click()
    time.sleep(3)
    resetandsearch()



header = "SERIAL-NO   ID       STATUS    REC DEACT TELEMETRY       ACTION"
dash = "="*65
record = []
record.append(dash)
record.append(header)
record.append(dash)
def adding(line):
	if line not in record:
		record.append(line)



for serial in serials:
	serial = serial.strip()
	time.sleep(3)
	resetandsearch()
	time.sleep(3)
	i = tabfun()

	while i > 0:
		try:
			i = i - 1
			time.sleep(3)
			asr_status = "/html/body/div[1]/form/div[1]/div[3]/div/div[1]/div/div[5]/div/div[1]/div[2]/div/div[6]/div/div[1]/div[3]/div/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div/div/div/table/tbody/tr/td[1]/table/tbody/tr[8]/td[2]"
			status = driver.find_element_by_xpath(asr_status)
			status = status.get_attribute("innerHTML")
			status = status.strip()
			xp = '//*[@id="pt1:pt_region0:1:t_assetComponents::db"]/table/tbody/tr[' + str(i) + ']'
			sd = '//*[@id="pt1:pt_region0:1:t_assetComponents::db"]/table/tbody/tr[' + str(i) + ']/td[9]'                 
			rt = '//*[@id="pt1:pt_region0:1:t_assetComponents::db"]/table/tbody/tr[' + str(i) + ']/td[4]/span'
			aid = '//*[@id="pt1:pt_region0:1:t_assetComponents::db"]/table/tbody/tr[' + str(i) + ']/td[1]/span'
			tele = '//*[@id="pt1:pt_region0:1:t_assetComponents::db"]/table/tbody/tr[' + str(i) + ']/td[14]/span'
			driver.find_element_by_xpath(xp).click()                                                                    
			val1 = driver.find_element_by_xpath(rt).get_attribute("innerHTML")
			val2 = driver.find_element_by_xpath(sd).get_attribute("innerHTML")
			val3  = driver.find_element_by_xpath(aid).get_attribute("innerHTML")
			val4 = driver.find_element_by_xpath(tele).get_attribute("innerHTML")
			val1 = re.sub("EM\s.*$", "EM", val1)
			val1 = re.sub("ASR-.*$", "ASR", val1)
			val1 = val1.strip()
			val2 = re.sub('<[^<]+?>', '', val2)
			val2 = val2.strip()
			val3 = re.sub('<[^<]+?>', '', val3)
			val3 = val3.strip()
			val3 = str(val3)
			val4 = re.sub('<[^<]+?>', '', val4)
			val4 = val4.strip()
			val4 = str(val4)
			serial = str(serial)
			a = val3+"  "+status+"  "+val1+"  "+val2
			b = serial+"  "+a
			c = b+"  "+val4
			d0 = c+"  deleted"
			d1 = c+"  not-deleted"
			time.sleep(3)
			if status != "Inactive" and val1 == "ASR" and val2 == "Yes":
				delete()

			if status != "Inactive" and val1 == "NA":
				deactivate()
				resetandsearch()
				delete()

			if status != "Inactive" and val1 == "ASR" and val2 == "No":
				adding(d1)

			if status != "Inactive" and val1 != "ASR":
				adding(d1)
					
			if status == "NonActiveAsset" and val1 == "ASR":
				delete()

			if status == "NonActiveAsset" and val1 != "ASR":
				adding(d1)

			#if status == "Inactive" and val1 == "ASR":
			if status == "Inactive":
				delete()

			#if status == "Inactive" and val1 != "ASR":
			#	adding(d1)	
			
			resetandsearch()
			time.sleep(3)
		except:
			pass

time.sleep(3)
record.append(dash)
for line in record:
	print(line)

driver.quit()


	
