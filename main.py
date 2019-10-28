#
#
# #
# I do not condone using this program nefariously.
# I am in no ways managing, nor taking responsibility for the extended usage of this project.
# It was used as an educational aiding project, and as a result, I believe that educationally
# I believe similar functionality should be natively implemented into this software.
# PLEASE DO NOT ABUSE THIS
# #
#
#
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from seleniumwire import webdriver

from bs4 import BeautifulSoup #scraping
import re
import pandas as pd #generate table view
from tabulate import tabulate #show table
import os
import time
import logging
import json

def sortAndAppend(ClassScores):
    assignments = json.loads(ClassScores)
    print("assignments" + str(type(assignments)))
    print("assignments[0]" + str(type(assignments[0])))
    null = ""
    remove = []
    #For all assignments remove everything except for what's needed. (Also move things around a little bit)
    for d in range(len(assignments)):
        x = assignments[d]["Assignment"]
        assignments[d]["Assignment"] = re.sub("[ ](?=[ ])|[^-_,A-Za-z0-9 ]+", "", str(x))
        assignments[d].pop('Flags')
        assignments[d].pop('Score')
        assignments[d].pop('%')
        assignments[d].pop('Grade')
        assignments[d].pop('View comments and descriptions')
        assignments[d].pop('Unnamed: 8')
        assignments[d].pop('Unnamed: 9')
        assignments[d]["Score"] = assignments[d].pop('Unnamed: 10')
        assignments[d]["%"] = assignments[d].pop('Unnamed: 11')
        assignments[d].pop('Unnamed: 12')
        assignments[d].pop('Unnamed: 13')
        if(assignments[d]["%"] == None): #Remove assigned assignments that have no grade, as it'll show up a null row in Node.js
            remove.append(d) #<--probably couldv'e used [del] here, but it seemed to mess up the current index of array., see below.
    for d in range(len(remove)):
        del assignments[remove[d] - d]
    return assignments

def main():
    url = "https://powerschool.{changeme}/public/"
    username = "user"
    password = "pass"

    #ChromeOptions //
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--no-proxy-server')
    #chrome_options.add_argument("--headless") //Disables or Enables viewing the Actual Application Window
    #chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(chrome_options=chrome_options)

    driver._client.set_header_overrides(
        headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language":"en-US,en;q=0.9",
            "Connection":"keep-alive",
            "User-Agent": "	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        })

    driver.get(url)
    time.sleep(2)
    inputElement = driver.find_element_by_id("fieldAccount")
    inputElement.send_keys(username)
    inputElement = driver.find_element_by_id("fieldPassword")
    inputElement.send_keys(password)
    inputElement.submit()
    datalist = [] #empty list
    filterBy = "S1" #//S1 == Semester1, S2 == Semester2, Q1 ==... ect.
    weburl = "https://powerschool.{changeme}/guardian/"
    index=BeautifulSoup(driver.page_source, 'lxml')
    for link in index.find_all("a",{"class":"bold"}):
        if(link["href"].startswith("scores.html") and link["href"].endswith("fg=" + filterBy)):
            time.sleep(2)
            driver.get(str(weburl) + str(link['href']))
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "zebra")))
            grades=BeautifulSoup(driver.page_source, 'lxml')
            gradesTable = grades.find("table", {"class":"zebra grid table ng-scope"})
            df = pd.read_html(str(gradesTable),skiprows=0,header=0)
            datalist.append(df[0])
            print("**Success: Appending Datalist.")
        print("**Info: Not the link we are looking for.")
    driver.quit()


    for i in range(len(datalist)):
        result = pd.concat([pd.DataFrame(datalist[i])],ignore_index=True)
        json_Sanitized = sortAndAppend(result.to_json(orient='records'))
        #get current working directory
        path = os.getcwd()
        #open, write, and close the file
        with open(path + "\\graphs\classdata" + str(i) + ".json", 'w') as outfile:
            json.dump(json_Sanitized, outfile)
main()
