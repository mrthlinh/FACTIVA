# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 12:06:30 2018

@author: mrthl
"""

# Scrap web
from selenium import webdriver
import pandas as pd

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
#from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.common.keys import Keys
import os
import shutil 
from glob import glob
import json
import datetime
#import sys

#=========================== Read Parameters =================================================


#=========================== Defined Function =================================================
def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%d %B %Y')
    except ValueError:
        return False
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
            element.find_element_by_xpath("..//span[@class='mnuBtn']").click()
            navigate_click(v)
            
        else:
            if (v == 1):
                element.click()    
            else:
                element.find_element_by_xpath("..//a[@title='Click to exclude.']").click()
#                element.send_keys(Keys.ARROW_DOWN)
#                driver.implicitly_wait(10)
#                element_ = driver.find_element_by_link_text(k)
#                actionChains = ActionChains(driver)
#                actionChains.double_click(element_).perform()

def correct_name(name):
    name = name.replace('.','')
    name = name.replace('*','') 
    name = name.replace('?','') 
    return name 

def flip_page(incomplete_download):
    num_flip = int(incomplete_download / 100)
    idx = 1
    for i in range(num_flip):
        try:
            next_btn = WebDriverWait(driver, 120).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "nextItem"))
            )
        except:
            print("Failed")
            break
            
        driver.execute_script("arguments[0].click();", next_btn)
        print("Flip to the next Page: ",end="")
              
        idx = (i + 1) * 100 + 1
#        next_num = idx + 101
        
        next_num_str = str(idx)+'.  '
        try:
            WebDriverWait(driver, 120).until(
    #            EC.presence_of_element_located((By.CLASS_NAME, "previousItem"))
                EC.text_to_be_present_in_element((By.CLASS_NAME, "count"),next_num_str)
            )
        except:
            print("Failed")
            break
        print("Success")      
        

    try:
        next_btn = WebDriverWait(driver, 120).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "nextItem"))
        )
    except:
        print("Failed")
    
#    start_idx = incomplete_download -  (incomplete_download % 100 )
    start_idx = idx - 1
    return start_idx

#incomplete_download = 420
#i = flip_page(incomplete_download)
#
#try:
#    next_btn = WebDriverWait(driver, 120).until(
#        EC.element_to_be_clickable((By.CLASS_NAME, "nextItem"))
#    )
#except:
#    print("Failed")
#print("Success") 

#=========================== Login and Configuration =================================================
# Read configurations
with open("json/config.json", 'r') as f:
    config = json.load(f)
    
with open("json/error.json", 'r') as f:
    error_dict = json.load(f)

# Read actions
with open("json/actions.json", 'r') as f:
    actions = json.load(f)

download_dir = config.get("download_directory")
filename = config.get("companyFile")
print("Download Directory: ",download_dir)
print("File Name: ",filename)

#load data
data = pd.read_csv("companyList/" + filename,names  = ['CompanyName'])
company_list = data['CompanyName']
company_list = list(company_list)
    
incomplete_download = error_dict.get("incomplete_download")
incomplete_company = error_dict.get("incomplete_company")
print("Resume Download at Company: ",company_list[incomplete_company])
print("Incomplete Download at file: ",incomplete_download)
print("========================= Main Program ===================================")


url = "https://libproxy.utdallas.edu/login?url=http://global.factiva.com/en/sess/login.asp?xsid=S003Wvf3dRb4GFp5DEs5DEmODUqMTMoODFyMHmnRsIuMcNG1pRRQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQQAADay"

fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList",2)
fp.set_preference("browser.download.dir", download_dir)
fp.set_preference("browser.download.manager.showWhenStarting",False)
fp.set_preference("browser.helperApps.neverAsk.saveToDisk","application/pdf")
fp.set_preference("pdfjs.disabled", True)

driver = webdriver.Firefox(fp)
driver.get(url)

print("Login - Please enter user and password")
session_id = driver.session_id  

menu_dict = {"Source": 0, "Author":1,"Company":2,"Factiva Expert Search": 3,
            "Subject": 4, "Industry": 5, "Region": 6, "Look up": 7,
            "Language": 8, "More Options": 9, "Date": "dr", "Duplicates": "isrd"}

# Read actions
#with open("json/actions.json", 'r') as f:
#    actions = json.load(f)
    
#================================== Main Program =============================================


# Loop all companies
for company_name in company_list[incomplete_company:]:
    
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
    print("Created Folder at: ",new_directory)
    
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
    
    #==========================  Download & Get Data =====================================================  
    columns = ['id','Company Name','Date','Text']
    records = []
     
    number_download = 0
    test = 0    
    
    download_err_idx = 0    
    page_idx = flip_page(incomplete_download)
    print("page_idx after flip: ",page_idx)
    
    while(True):
        try:
            fault = 0
            # Flip to the desired page
#            idx = flip_page(incomplete_download)
                        
            count = driver.find_element_by_class_name("count")
    #        print(count.text)
            
            print("Add Data")
            result_headline = driver.find_elements_by_class_name("enHeadline")
            result_date = driver.find_elements_by_class_name("leadFields")
                        
            # Add data: i = 0 -> 99
            for i in range(incomplete_download % 100,len(result_headline)):
                st = result_date[i].text.split(', ')
                for s in st:
                    if validate(s):
                        date = s
                        break                   
                headline = result_headline[i].text                
                records.append([i + page_idx + 1 ,company_name,date,headline])
                   
            print("Download File")
            
           # Download File j = 0 -> 99
            tick = driver.find_elements_by_name("hdl")
#            print("len tick: ",len(tick))
            for j in range(incomplete_download % 100,len(tick)):
#                incomplete_download = 0
                download_err_idx = j + page_idx
                
                tick[j].click()
            
                download_select_btn = driver.find_elements_by_class_name("ppsBtn")
                download_select_btn[-2].click()
            
                headline = result_headline[j].text
                filename = str(download_err_idx + 1)
                
                
                print("Download Article "+ filename +": ",end="")
                try:
                    download_option = WebDriverWait(driver, 100).until(
                        EC.element_to_be_clickable((By.LINK_TEXT, "Article Format"))       
                    )
                except:
                    print("Failed")
                print("Success")
                
                print("Download Option Clicked")
                download_option.click()
                
                tick[j].click()
                
                print("Wait for Download Finished")
                
                while (True):
                    all_pdf = glob(download_dir+"/*.pdf")
                    if (len(all_pdf) > 0):
                        print("Wait to move File")
                        k = 1
                        for file in all_pdf:
                            
                            new_file = new_directory + '/' + filename
                            try:
                                shutil.move(file, new_file +".pdf")
                            except:
                                shutil.move(file, new_file + str(k) + ".pdf")
                            k = k + 1
                        print("Finish")
                        break
                    
            incomplete_download = 0
            
            # Next Page
            try:
                next_btn_test = driver.find_element_by_class_name("nextItem")
            except:
                print("Last Page")
                break
            
            try:
                next_btn = WebDriverWait(driver, 120).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "nextItem"))
                )
            except:
                print("Failed")
                break
            print("Success") 
            
            
            driver.execute_script("arguments[0].click();", next_btn)
            print("Heading Next Page: ",end="")
            
            page_idx = page_idx + 100
            next_num = page_idx + 1
            
             
            print("next num for next page: ",next_num)
            next_num_str = str(next_num)+'.  '
            try:
                result_bar = WebDriverWait(driver, 120).until(
        #            EC.presence_of_element_located((By.CLASS_NAME, "previousItem"))
                    EC.text_to_be_present_in_element((By.CLASS_NAME, "count"),next_num_str)
                )
            except:
                print("Failed")
                break
            print("Success") 
            
#            page_idx = page_idx + 100
        except:
            fault = 1
            break
    
    df = pd.DataFrame.from_records(records,columns=columns)
    incomplete_download = 0
#    df.to_csv(download_dir+"/"+name,index=False,encoding='utf-8')
#    print("Created a file: "+name)
    
    if (fault == 0):
        name = company_name.replace('.','') + ".csv"
        full_dir = download_dir+"/"+name

    elif (fault == 1):
        list_incomplete = glob(download_dir+"/temp/"+company_name+"*.csv")
        
        name = company_name.replace('.','') + "_incomplete"+str(len(list_incomplete))+".csv"
        full_dir = download_dir+"/temp/"+name
        
        error_dict = {"incomplete_company":company_list.index(company_name), "incomplete_download": download_err_idx}
        with open('json/error.json', 'w') as outfile:
            json.dump(error_dict, outfile)

    df.to_csv(full_dir,index=False,encoding='utf-8')
    print("Created a file: "+full_dir)
        

    searchBtn = driver.find_element_by_link_text("Search")
    searchBtn.click()
