# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 15:50:42 2018

@author: mrthl
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 00:17:00 2018

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
import datetime

def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%d %B %Y')
    except ValueError:
        return False
#        raise ValueError("Incorrect data format, should be YYYY-MM-DD")
    return True

#=========================== Login and Configuration =================================================
user = "lht160030"
password = "Workintheus1992"
url = "https://libproxy.utdallas.edu/login?url=http://global.factiva.com/en/sess/login.asp?xsid=S003Wvf3dRb4GFp5DEs5DEmODUqMTMoODFyMHmnRsIuMcNG1pRRQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQQAADay"

download_dir = "E:\FACTIVA"

fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList",2)
fp.set_preference("browser.download.dir", download_dir)
fp.set_preference("browser.download.manager.showWhenStarting",False)
fp.set_preference("browser.helperApps.neverAsk.saveToDisk","application/pdf")
fp.set_preference("pdfjs.disabled", True)

driver = webdriver.Firefox(fp)
driver.get(url)

print("Logining: ",end="")

user_input = driver.find_element_by_name("user")
user_input.send_keys(user)

pass_input = driver.find_element_by_name("pass")
pass_input.send_keys(password)

button = driver.find_element_by_name("SUBMIT")
button.click()

session_id = driver.session_id  
#id_name = "scTab"

#id_name = "scLst"
#try:
#    element = WebDriverWait(driver, 120).until(
#        EC.text_to_be_present_in_element((By.ID, id_name),"All Sources")
#    )
#except:
#    print("Failed")
#print("Success")
#
#print("Page loaded")
#===============================================================================
#company_list = ['XYLEM INC.','3-D SYSTEMS CORP','3M Company']
#company_name = company_list[0]

#load data
#data = pd.read_csv("CompanyNames.csv",names  = ['CompanyName'])
data = pd.read_csv("Companies.csv",names  = ['CompanyName'])
company_list = data['CompanyName']
company_list = list(company_list)

# Loop all companies
for company_name in company_list[:3]:   
    print (company_name)
    
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
    new_directory = download_dir + "\\" +company_name.replace('.','')
    if not os.path.exists(new_directory):
        os.makedirs(new_directory)

#==========================  Select Options =====================================================  
    all_source = driver.find_element_by_id("scTab")
    all_source.click()
    
    print("Clicking Source: ",end="")
    
    
    try:
        element = WebDriverWait(driver, 120).until(
    #        EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".mnuItm:last-child"),"Wires")
    #        EC.element_to_be_clickable((By.CLASS_NAME, "mnuItm"))
            EC.element_to_be_clickable((By.CLASS_NAME, "mnuBtn"))
            
        )
    except:
        print("Failed")
    print("Success")
    
    print("Clicked Wires")
    wire = driver.find_elements_by_class_name("mnuBtn")[-1]
    wire.click()
    
    print("Deselect Newswires: ",end="")
    try:
        Not_Newswire = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Newswires"))      
        )
    except:
        print("Failed")
    actionChains = ActionChains(driver)
    actionChains.move_to_element(Not_Newswire)
    actionChains.double_click(Not_Newswire)
    actionChains.perform()
    print("Success")
    
    print("Select Press Release Wires: ",end="")
    try:
        element = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Press"))       
        )
    except:
        print("Failed")
    press_wire = driver.find_elements_by_class_name("mnuBtn")[-1]
    press_wire.click()
    print("Success")
    
    print("Select Business and GlobeNews Wires: ",end="")
    try:
        Business_Wire = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Business Wire (U.S.)"))       
        )
    except:
        print("Failed")
    
    Business_Wire.click()
    GlobeNewswire = driver.find_element_by_partial_link_text('GlobeNewswire (U.S.)')
    PR_Newswire = driver.find_element_by_partial_link_text('PR Newswire (U.S.)')
    GlobeNewswire.click()
    PR_Newswire.click()
    print("Success")
    
    wire.click()
    all_source.click()
    
    
    region = driver.find_element_by_id("reTab")
    region.click()
    print("Clicked Region")
    
    print("Clicking North America: ",end="")
    try:
        element = WebDriverWait(driver, 60).until(
    #        EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".mnuItm:last-child"),"Wires")
            EC.element_to_be_clickable((By.CLASS_NAME, "mnuBtn"))
        )
    except:
        print("Failed")
    NA = driver.find_elements_by_class_name("mnuBtn")[-2]
    NA.click()
    print("Success")
    
    print("Clicking US: ",end="")
    try:
        element = WebDriverWait(driver, 60).until(
    #        EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".mnuItm:last-child"),"Wires")
    #        EC.element_to_be_clickable((By.CLASS_NAME, "mnuBtn"))
            EC.element_to_be_clickable((By.LINK_TEXT, "United States"))
        )
    except:
        print("Failed")
    element.click()
    print("Success")
    region.click()
    
    select = Select(driver.find_element_by_id('dr'))
    # select by visible text
    select.select_by_visible_text('All Dates')
    print("Select All Dates")
    
    
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
    #        EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".mnuItm:last-child"),"Wires")
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


columns = ['id','Company Name','Date','Text']
records = []
idx = 1

number_download = 0
test = 0


while(True):
    count = driver.find_element_by_class_name("count")
    print(count.text)
    
    result_headline = driver.find_elements_by_class_name("enHeadline")
    result_date = driver.find_elements_by_class_name("leadFields")
    
    print("Validate date")
    # Validate date
    for i in range(len(result_headline)):
        st = result_date[i].text.split(', ')
        for s in st:
            if validate(s):
                date = s
                break
            
        headline = result_headline[i].text
        records.append([i + idx ,company_name,date,headline])

    
    print("Download File")
   # Download File
    tick = driver.find_elements_by_name("hdl")

    for j in range(len(tick)-90):
        tick[j].click()
    
        download_select_btn = driver.find_elements_by_class_name("ppsBtn")
        download_select_btn[-2].click()
    
        headline = result_headline[j].text
        filename = str(j + idx)
        
        
        print("Download Article: ",end="")
        try:
            download_option = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Article Format"))       
            )
        except:
            print("Failed")
        print("Success")
        download_option.click()
        
        tick[j].click()
        
        print("Wait for Download Finished")
        
        while (True):
            all_pdf = glob(download_dir+"/*.pdf")
            if (len(all_pdf) == 1):
                file = all_pdf[0]
#                print(file)
#                print(filename)
                print("Wait to move File")
                #all_pdf = glob(download_dir+"/*.pdf")
                new_file = new_directory + '/' + filename +".pdf"
                shutil.move(file, new_file)
                
                while (True):
                    all_pdf = glob(download_dir+"/*.pdf")
                    if (len(all_pdf) == 0):
                        break;
                
                print("Finish")
                break
    

    # Next Page
    try:
        next_btn_test = driver.find_element_by_class_name("nextItem")
    except:
        print("Last Page")
        break
    
    try:
        next_btn = WebDriverWait(driver, 120).until(
#            EC.presence_of_element_located((By.CLASS_NAME, "previousItem"))
            EC.element_to_be_clickable((By.CLASS_NAME, "nextItem"))
        )
    except:
        print("Failed")
        break
    print("Success") 
    
#    next_btn = driver.find_element_by_class_name("nextItem")
#    next_btn.click()
    
    driver.execute_script("arguments[0].click();", next_btn)
#    next_btn.send_keys("\n")
    print("Heading Next Page: ",end="")
    
    next_num = idx + 100
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
    
    idx = idx + 100
    



modifyBtn = driver.find_element_by_id("btnModifySearch")
modifyBtn.click()




#
#session_id = driver.session_id  
#
#tick = driver.find_elements_by_name("hdl")
#result_headline = driver.find_elements_by_class_name("enHeadline")
#
## Download File
#for j in range(len(tick)-90):
#    tick[j].click()
#
#    download_select_btn = driver.find_elements_by_class_name("ppsBtn")
#    download_select_btn[-2].click()
#
#    headline = result_headline[j].text
#    filename = str(j+1)
#    
#    
#    print("Download Article: ",end="")
#    try:
#        download_option = WebDriverWait(driver, 100).until(
#            EC.element_to_be_clickable((By.LINK_TEXT, "Article Format"))       
#        )
#    except:
#        print("Failed")
#    print("Success")
#    download_option.click()
#    
#    tick[j].click()
#    
#    print("Wait All Download Finished")
#    while (True):
#        all_pdf = glob(download_dir+"/*.pdf")
#        if (len(all_pdf) == 1):
#            file = all_pdf[0]
#            print(file)
#            print(filename)
#            print("Move File")
#            #all_pdf = glob(download_dir+"/*.pdf")
#            new_file = new_directory + '/' + filename +".pdf"
#            shutil.move(file, new_file)
#            print("Finish")
#            break
    




