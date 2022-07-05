"""
# Sloka number
# //div[@id="bb181"]/h1

# check if purpote is exist
//h2[normalize-space(text()) = 'Purport']

# next btn
//ul[@class="mini-pager mt-2 pb-4"]/li[2]/a[@class="btn"]
"""

import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from automation.AutomationError import FieldIdentifierNotDefined
from automation.AutomationError import *
import time
from selenium.common.exceptions import NoSuchElementException        

options = Options()
options.headless = True
options.add_experimental_option('excludeSwitches', ['enable-logging'])
selenium_webdriver = webdriver.Chrome("C:\\chromedriver\\chromedriver.exe", options=options)
wait = WebDriverWait(selenium_webdriver, 10)


selenium_webdriver.get("https://vedabase.io/en/library/bg/1/1/")

def click(id=None, xpath=None,sleep_time=None):
    if id is None and xpath is None:
        raise FieldIdentifierNotDefined()
    elif id is not None:
        submit = wait.until(EC.visibility_of_element_located((By.ID, id)))
        submit.click()
    elif xpath is not None:
        submit = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        submit.click()


def check_exists_by_xpath(xpath):
    try:
        selenium_webdriver.find_element("xpath", xpath)
    except NoSuchElementException:
        return False
    except Exception as e:
        print(e.args[0])
    return True

db = []
chapter = 1
while True:
    try:
        data_dict = {}
        data_dict["purport_exist"] = check_exists_by_xpath("//h2[text()='Purport']")
        data_dict["sloka"] = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="r r-title r-verse"]/h1'))).get_attribute("innerHTML")
        db.append(data_dict)
        print(data_dict)
        click(id=None, xpath='//li[@class="pager-next"]/a[@class="btn"]')
    except:
        if chapter >= 18:
            break

        if check_exists_by_xpath("//dl/dt/a[contains(text(), 'TEXT')]"):
            print("next -- page -->")
            first_text = wait.until(EC.visibility_of_element_located((By.XPATH, "(//dl/dt/a[contains(text(), 'TEXT')])[1]"))).get_attribute("innerHTML")
            chapter += 1
            previous_chapter = int(float(db[-1]["sloka"].split(" ")[1]))
            selenium_webdriver.get("https://vedabase.io/en/library/bg/{0}/{1}/".format(previous_chapter + 1, first_text.split(" ")[-1].split(":")[0]))
        else:
            print("error: ", chapter)

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(db, f, ensure_ascii=False, indent=4)

selenium_webdriver.close()

