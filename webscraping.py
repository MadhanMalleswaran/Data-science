from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Set up the webdriver
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

# Navigate to the Redbus website
driver.get("https://www.redbus.in/")

# Point to the RTC Bus Lists page
xpath = f"""//*[@id="homeV2-root"]/div[3]/div[1]/div[2]/a"""

try:
    government_bus_elements = driver.find_element(By.XPATH,xpath)

    rtc_bus_directory = government_bus_elements.get_attribute("href")

    # Open the RTC Bus List page
    driver.get(rtc_bus_directory)

    # Get the list of transport boards of all the states
    transport_boards = driver.find_elements(By.CLASS_NAME,"D113_link")

    list_of_board_urls = []
    boards = []
    # get the url and board name for an each transport boards of states
    for i in transport_boards:       
        list_of_board_urls.append(i.get_attribute("href")) 
        boards.append(i.text)
   
    # create a dataframe 
    bus_boards = pd.DataFrame({"Board_Name":boards,"Board_Url":list_of_board_urls})
    #remove the duplicates
    bus_boards.drop_duplicates()

    # print(bus_boards.count())
    
    # Save the list in local drive
    path = r"D:\Guvi\busBoards.csv"
    bus_boards.to_csv(path,index=True)
        
except Exception as e:
    print(e)

# Close the browser
driver.quit()

