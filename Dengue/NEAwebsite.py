# from selenium.common.exceptions import NoSuchElementException
# from selenium.common.exceptions import StaleElementReferenceException
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
cases2weeks = []
for num in casesSince2weeks:
    cases2weeks.append(num.text) 
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
data["date of extraction"] = dateExtractedCol
file = open("NeaData", "a")
csv = data.to_csv(index=False)
file.writelines(csv)
file.close()