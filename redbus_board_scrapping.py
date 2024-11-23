from webscraping import *
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import time
import pandas as pd

# Set up the webdriver
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
driver.maximize_window()

try:
 
    #board_transport = list_of_board_urls
    #board_transport = ["https://www.redbus.in/online-booking/sikkim-nationalised-transport-snt"]
    #board_transport = ["https://www.redbus.in/online-booking/ksrtc-kerala"]
    routes = []
    route_link = []
    boards = []

    # Loop thru the each url from the dataframe 
    for i, urls in bus_boards.iterrows():


        board_name = urls['Board_Name']
        url = urls['Board_Url']
        # print(board_name)
        #board_name = "KSRTC"
        driver.get(url)

        try:

            is_valid = driver.find_element(By.CLASS_NAME,"D117_main")
            
            errors = [NoSuchElementException]
            wait = WebDriverWait(driver,20,ignored_exceptions=errors)

            pages = driver.find_elements(By.CLASS_NAME,"DC_117_pageTabs")
            for page in range(1, len(pages)):
                route_dir = driver.find_elements(By.CLASS_NAME, "route")
                for info in route_dir:
                    #pick the url, routes and boards for eacl url
                    route_link.append(info.get_attribute("href"))
                    routes.append(info.get_attribute("title"))
                    boards.append(board_name)
                
                try:
                    #move to the next page to retrieve more results on the same transport board
                    nextPage = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@class="DC_117_paginationTable"]')))
                    next = nextPage.find_element(By.XPATH,f'//div[@class="DC_117_pageTabs " and text()={page+1}]')
                    driver.execute_script("arguments[0].click();",next)
                except NoSuchElementException:
                    print(f"No more pages at step {page}")
                    break
            #create a dataframe with list of Bus Route Name, Bus Routes Link and Boards
            bus_routes = pd.DataFrame({"Bus_Routes_Name":routes,"Bus_Routes_Link":route_link, "Boards":boards})

        except Exception as exc:
                print(exc)

    bus_routes.drop_duplicates()
    # print(bus_routes.count())
    # Save the list in local
    path = r"D:\Guvi\busRoutes.csv"
    bus_routes.to_csv(path,index=True)

except Exception as e:
    print(e)


driver.quit()