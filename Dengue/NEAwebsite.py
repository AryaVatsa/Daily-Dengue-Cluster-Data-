from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import datetime
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions


options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=options)

driver.get("https://www.nea.gov.sg/dengue-zika/dengue/dengue-clusters")
driver.maximize_window()
driver.implicitly_wait(2)
placesRAW = driver.find_elements(By.XPATH, '//tr[@data-row]')
casesSince2weeks = driver.find_elements(By.XPATH, '//td[4]')
casesSinceStart = driver.find_elements(By.XPATH, '//td[5]')

places = []
for place in placesRAW:
    places.append(place.get_attribute("id"))

showButtons = []
for place in places:
    showButtons.append(driver.find_element(By.XPATH, f'//*[@id="{place}"]/td[3]/p[1]'))
def closePopUp():
    driver.find_element(By.XPATH, '//*[@id="ClusterModal"]/div/div[1]/h2/span').click()
localities = []
# for button in showButtons:
#     button.click()
#     driver.implicitly_wait(2)
#     for n in range(2, 30):
#         try:
#             localities.append(driver.find_element(By.XPATH, f'//*[@id="modalBody"]/table/tbody/tr[{n}]/td[1]').text)
#         except NoSuchElementException:
#             break
#     driver.implicitly_wait(2)
#     closePopUp()

for button in showButtons:
    button.click()
    driver.implicitly_wait(2)
    elements = driver.find_elements(By.XPATH, '//*[@id="modalBody"]/table/tbody')
    for element in elements:
        localities.append(element.text)
    driver.implicitly_wait(2)
    closePopUp()
localityFile = open("NeaLocalityData", "a")
localityFile.writelines(localities)
localityFile.close()

def fileFindnReplace(FileName, Find, Replace):
    file = open(FileName, "r")
    newContent = (file.read()).replace(Find, Replace)
    file.close()
    Data = open(FileName, "w")
    Data.write(newContent)
    Data.close()



fileFindnReplace("NeaLocalityData", "Location No. of Cases", "")
fileFindnReplace("NeaLocalityData", "\n(", " (")

file = open("NeaLocalityData", "r")
lines = file.readlines()
newLines = []
for line in lines:
    try:
        if line[-4].isdigit() and line[-3].isdigit() and line[-2].isdigit():
            newLine = line[:-5] + "," + line[-4:]
        
        elif line[-3].isdigit() and line[-2].isdigit():
            newLine = line[:-4] + "," +  line[-3:]

        elif line[-2].isdigit():
            newLine = line[:-3] + "," +  line[-2:]
        newLines.append(newLine)
    except IndexError:
        print(line)
file = open("NeaLocalityData", "w")
file.writelines(newLines)
file.close()


cases2weeks = []
for num in casesSince2weeks:
    cases2weeks.append(num.text) 
print(cases2weeks) 
CasesStart = []

for num in casesSinceStart:
    CasesStart.append(num.text)

driver.close()

newPlaces = []
for place in places:
    newplace = ""
    for i, char in enumerate(place):
        if char.isupper():
            newplace += " " + char
        else:
            newplace += char
    newPlaces.append(newplace)

data = pd.DataFrame(list(zip(newPlaces, cases2weeks, CasesStart)), columns=["cluster address", "cases in last 2 weeks", "cases since beginning of cluster"])
count = data.count()
numOfRows = count.iloc[0]
dateExtractedCol = []
extractionDate = datetime.date.today()
for _ in range(numOfRows):
    dateExtractedCol.append(extractionDate)


file = open("NeaDataOverview", "a")
csv = data.to_csv(index=False)
file.writelines(csv)
file.close()

localData = pd.read_csv("NeaLocalityData")
count = localData.count()
numOfRows = count.iloc[0]
extractionDate = datetime.date.today()
for _ in range(numOfRows):
    dateExtractedCol.append(extractionDate)
localData["date of extraction"] =  dateExtractedCol
file = open("NeaLocalityData", "w")
csv = localData.to_csv()
file.writelines(csv)
file.close()