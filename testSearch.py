# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 12:06:30 2018

@author: mrthl
"""

# Scrap web
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import os
import shutil 
from glob import glob
import json
import datetime
#=========================== Defined Function =================================================
def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%d %B %Y')
    except ValueError:
        return False
#        raise ValueError("Incorrect data format, should be YYYY-MM-DD")
    return True

def navigate_click(my_dict):
    
    for (k,v) in my_dict.items():
#        print(k)
        try:
            element = WebDriverWait(driver, 120).until(      
#                EC.element_to_be_clickable((By.LINK_TEXT, k))
                EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, k))
#                EC.visibility_of_element_located((By.LINK_TEXT, k))        
            )           
        except:
            print("Failed")
        print("Success") 
               
        print("Clicking "+k+": ",end="")
        
        if (type(v) == dict):
#            print("I'm here")
#            driver.find_elements_by_class_name("mnuBtn")[-1].click()
            # Find the sibling with class mnuBtn
            element.find_element_by_xpath("..//span[@class='mnuBtn']").click()
            navigate_click(v)
        else:
            if (v == 1):
                element.click()    
            else:              
                element.send_keys(Keys.ARROW_DOWN)
                driver.implicitly_wait(10)
                element_ = driver.find_element_by_link_text(k)
#                driver.find_element_by_link_text("Newswires")
                actionChains = ActionChains(driver)
                actionChains.double_click(element_).perform()

#navigate_click(actions.get("Source"))

def correct_name(name):
    name = name.replace('.','')
    name = name.replace('*','') 
    name = name.replace('?','') 
    return name        
#=========================== Login and Configuration =================================================
# Read configurations
with open("json/config.json", 'r') as f:
    config = json.load(f)
    
url = "https://libproxy.utdallas.edu/login?url=http://global.factiva.com/en/sess/login.asp?xsid=S003Wvf3dRb4GFp5DEs5DEmODUqMTMoODFyMHmnRsIuMcNG1pRRQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQQAADay"

download_dir = config.get("download_directory")
#download_dir = "E:\FACTIVA"

fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList",2)
fp.set_preference("browser.download.dir", download_dir)
fp.set_preference("browser.download.manager.showWhenStarting",False)
fp.set_preference("browser.helperApps.neverAsk.saveToDisk","application/pdf")
fp.set_preference("pdfjs.disabled", True)

driver = webdriver.Firefox(fp)
driver.get(url)

print("Logining")
session_id = driver.session_id  

menu_dict = {"Source": 0, "Author":1,"Company":2,"Factiva Expert Search": 3,
            "Subject": 4, "Industry": 5, "Region": 6, "Look up": 7,
            "Language": 8, "More Options": 9, "Date": "dr", "Duplicates": "isrd"}

# Read actions
with open("json/actions.json", 'r') as f:
    actions = json.load(f)
    
#================================== Main Program =============================================

#load data
filename = config.get("companyFile")
data = pd.read_csv("/companyList/" +filename,names  = ['CompanyName'])
company_list = data['CompanyName']
company_list = list(company_list)


# Loop all companies
for company_name in company_list:   
    print (company_name)
    company_name = correct_name(company_name)
    
    print("Page Loading", end="")
    id_name = "scLst"
    try:
        element = WebDriverWait(driver, 120).until(
            EC.text_to_be_present_in_element((By.ID, id_name),"All Sources")
        )
    except:
        print("Failed")
    print("Success")
    
#    print("Page loaded")

    #========================== Make new Directory =====================================================    
    new_directory = download_dir + "\\download\\" +company_name.replace('.','')
    if not os.path.exists(new_directory):
        os.makedirs(new_directory)
    
    #==========================  Select Options =====================================================  
    main_menu = driver.find_elements_by_class_name("pnlTabArrow")
    
    for (key, value) in actions.items():
        
        main_menu_index = menu_dict.get(key)
        
        if (type(main_menu_index) == int):
            main_menu_arrow = main_menu[main_menu_index]
            main_menu_arrow.click()      
                
            print("Clicking "+key+": ",end="")  
            try:
                element = WebDriverWait(driver, 120).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "mnuBtn"))  
                )
            except:
                print("Failed")
            print("Success")
            
            navigate_click(value)
            
            main_menu_arrow.click()
            
        else:           
            select = Select(driver.find_element_by_id(main_menu_index))
            
            # select by visible text
            select.select_by_visible_text(value)
            
            print("Select " + key + " with choice " + value)
        
    #==========================  Other Options =====================================================    
    print("Input Company Name")
    company = driver.find_element_by_id("coTab")
    company.click()
    
    company_input = driver.find_element_by_id("coTxt")
    company_input.send_keys(company_name)
    
    enter_search = driver.find_element_by_id("coLkp")
    enter_search.click()
    
    print("Selecting Company Name: ",end="")
    try:
        select_company = WebDriverWait(driver, 120).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "mnuItm"))
        )
    except:
        print("Failed")
    
    select_company1 = driver.find_element_by_class_name("mnuItm")
    select_company1.click()
    print("Success")
    company.click()
    
    print("Clicking Search Button: ",end="")
    btn_search = driver.find_element_by_id("btnSearchBottom")
    btn_search.click()
    
    try:
        result_bar = WebDriverWait(driver, 120).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "enHeadline"))
        )
    except:
        print("Failed")
    print("Success")
    
    searchBtn = driver.find_element_by_link_text("Search")
    searchBtn.click()

    #==========================  Download & Get Data =====================================================  
    
      