from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re



srnumber = raw_input('Enter the SR Number: ')

# Username and password of the account
my_username = "david.ingty@oracle.com"
my_password = "Solaris10"

# crome driver paths
#chrome_driver_path = r"C:\webdrivers\chromedriver.exe"
chrome_driver_path = "C:\\webdrivers\\chromedriver"
driver = webdriver.Chrome(chrome_driver_path)

# Open the webpage and Login with account details
driver.get('https://support.us.oracle.com/oip/faces/index.jspx')
link = driver.find_element_by_id('login')
link.click()

usernameid = driver.find_element_by_id('sso_username')
passwordid = driver.find_element_by_id('ssopassword')

usernameid.send_keys(my_username + Keys.RETURN)
passwordid.send_keys(my_password + Keys.RETURN)

xpath0 = '//*[@id="_id2"]/div[1]/table[2]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td[1]/button'
btn = driver.find_element_by_xpath(xpath0)
btn.click()


# Open the SR in MOS
mos = 'https://mosemp.us.oracle.com/epmos/mos/sp/viewSr?srNumber='
moslink = mos+srnumber
#driver.set_page_load_timeout(40)
driver.get(moslink)
#driver.maximize_window()
driver.implicitly_wait(15)
serialno = driver.find_element_by_xpath('//input[@name="serialNum"]').get_attribute('value')
tt = driver.find_element_by_xpath('//textarea[@name="description"]').get_attribute('value')


# InstalledBase page should have been loaded in the browser by now!!
driver.get('https://global-ebusiness.oraclecorp.com/OA_HTML/RF.jsp?function_id=1301858&resp_id=1181216&resp_appl_id=542&security_group_id=0&lang_code=US&oas=qpF8epQr9Bh8ILREo8SQHQ..&params=4dXsJAkcvJ0MjWaqrSrjpgiFtD53JFEW3b.3.ywdlQw')
driver.find_element_by_xpath('//*[@id="SerialNumberSch"]').send_keys(serialno)
driver.find_element_by_xpath('//*[@id="SimpleSearchRN"]/tbody/tr[4]/td/table/tbody/tr/td/div/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td[2]/button[1]').click()
driver.find_element_by_id('SystemNameSch').click()


# After pasting the serial in the serial search box the curson needs to go to the product link and return key must be pressed
i = 0
while i < 21:
  driver.find_element_by_tag_name('body').send_keys(Keys.TAB)
  i += 1

driver.find_element_by_tag_name('body').send_keys(Keys.TAB + Keys.RETURN)
driver.find_element_by_xpath('//*[@id="N530"]/tbody/tr/td[8]/a').click()
driver.find_element_by_xpath('//*[@id="N388"]/table[1]/tbody/tr[2]/td/table/tbody/tr/td/a[1]').click()


# finding the installedbase table after clicking on expand link and storing in a variable
ibtable = driver.find_element_by_xpath('//*[@id="N388"]/table[2]/tbody')

# Save the table info to the outlist list
outlist = []
for i in ibtable.find_elements_by_xpath('.//tr'):
    pr = i.get_attribute('innerHTML')
    outlist.append(pr)

# Data cleaning of ib information
outlist2 = []
for eachrow in outlist:
  eachrow = eachrow.replace("Item Description","").replace("Item","").replace("Serial Number","").replace("Quantity","").replace("Status","")
  eachrow = eachrow.replace("Focus", "").replace("Instance", "")
  eachrow = re.sub('<[^<]+?>', ' ', eachrow)
  eachrow = eachrow.strip()
  if eachrow not in outlist2:
    outlist2.append(eachrow)

# removing blank lines from the list
filtered = filter(lambda x: not re.match(r'^\s*$', x), outlist2)

# This list will hold the list_asset extracted from the SR page
list_asset = []
tt = tt.split("\n")
for i in tt:
  i = i.encode('utf-8')
  if "SNMP" in i:
    list_asset.append(i)



# writing the contents of filtered list to ib.txt file
with open('ib.txt', 'w') as r:
  for line in filtered:
    r.write(line)
    r.write("\n")

# writing the list_asset lines to list_asset.txt file
with open('list_asset.txt', 'w') as r:
  for line in list_asset:
    r.write(line)
    r.write("\n")


time.sleep(5)
driver.quit()






