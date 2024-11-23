from redbus_board_scrapping import *            
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import pandas as pd
import time

def list_length_same(bus_infr):
    first_list_length = len(bus_info[0])
    for lst in bus_info:
        if len(lst) != first_list_length:
            return False
    return True

# Initialize the WebDriver (e.g., Chrome)
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
driver.maximize_window()

try:

    bus_name = []
    bus_type = []
    dep_time = []
    duration = []
    reach_time = []
    star = []
    price = []
    seats = []
    busRoute = []
    busRouteLink = []
    boardInfor = []

    # routes = ["Ernakulam to Kozhikode"]
    # route_link = ["https://www.redbus.in/bus-tickets/ernakulam-to-kozhikode"]
    # board_name = ["KSRTC"]
    # bus_routes = pd.DataFrame({"Bus_Routes_Name":routes,"Bus_Routes_Link":route_link, "Boards":board_name})
    
    for i,routes in bus_routes.iterrows():

        print("url couht:",i)
        bus_route = routes["Bus_Routes_Name"]
        bus_route_link = routes["Bus_Routes_Link"]
        board_name = routes["Boards"]

        # Navigate to the URL
        driver.get(bus_route_link)

        try:
            # Wait for the bus list to load 
            WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class='travels lh-24 f-bold d-color']")))

            bus_found = driver.find_element(By.XPATH,'//*[@class="f-bold busFound"]')  
            no_of_buses = bus_found.text.split()
            total_buses = int(no_of_buses[0])

            print(total_buses)
            if total_buses != 0:
                #scrolling
                bus_items = driver.find_elements(By.XPATH,"//div[@class='travels lh-24 f-bold d-color']")
                scroll = len(bus_items)
                for scroll in range(1,total_buses,1):
                    ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
                    current_bus_items = driver.find_elements(By.XPATH,"//div[@class='travels lh-24 f-bold d-color']")
                    scroll += len(current_bus_items)
                    if scroll > total_buses:
                        break

                # Find all the bus names and types
                bus_elements = driver.find_elements(By.XPATH,"//div[@class='travels lh-24 f-bold d-color']")

                busName = driver.find_elements(By.XPATH,"//div[@class='travels lh-24 f-bold d-color']")
                busType = driver.find_elements(By.XPATH,"//div[@class='bus-type f-12 m-top-16 l-color evBus']")
                depTime = driver.find_elements(By.XPATH,"//div[@class='dp-time f-19 d-color f-bold']")
                dur = driver.find_elements(By.XPATH,"//div[@class='dur l-color lh-24']")
                reachTime = driver.find_elements(By.XPATH,"//div[@class='bp-time f-19 d-color disp-Inline']")
                try:
                    rating = driver.find_elements(By.XPATH,"//div[@class='clearfix row-one']/div[@class='column-six p-right-10 w-10 fl']")
                except:
                    continue
                fare = driver.find_elements(By.XPATH,"//div[@class='fare d-block']")
                seat = driver.find_elements(By.XPATH,"//div[contains(@class,'seat-left')]")

                no_of_bus_info = len(busName)
                
                # print("len of busname:",len(busName))
                # print("len of busType:",len(busType))
                # print("len of depTime:",len(depTime))
                # print("len of dur:",len(dur))
                # print("len of reachTime:",len(reachTime))
                # print("len of rating:",len(rating))
                # print("len of fare:",len(fare))
                # print("len of seat:",len(seat))

                # data cleaning process
                for info in range(0,no_of_bus_info):
                    busRoute.append(bus_route)
                    busRouteLink.append(bus_route_link)
                    boardInfor.append(board_name)
                    if info < len(busName):
                        bus_name.append(busName[info].text)
                    else:
                        bus_name.append("N/A")

                    if info < len(busType):
                        bus_type.append(busType[info].text)
                    else:
                        bus_type.append("N/A")

                    if info < len(depTime):                        
                        dep_time.append(depTime[info].text)
                    else:
                        dep_time.append("N/A")                        
                    
                    if info < len(dur):
                        duration.append(dur[info].text)
                    else:
                        duration.append("N/A")
                    
                    if info < len(reachTime):
                        reach_time.append(reachTime[info].text)
                    else:
                        reach_time.append("N/A")

                    if info < len(rating):
                        # star.append(rating[info].text)
                        val = rating[info].text.split()
                        if len(val) > 0:
                            if val[0] == "New":
                                star.append(float(0))  
                            else:
                                star.append(float(val[0]))
                        else:   
                            star.append(float(0))
                    else:
                        star.append(float(0))

                    if info < len(fare):
                        # price.append(fare[info].text)
                        value = fare[info].text.split()
                        if value[0] == 'INR':
                            price.append(float(value[1]))    
                        else:
                            price.append(float(value[0]))
                    else:
                        price.append(float(0))

                    if info < len(seat):
                        # seats.append(seat[info].text)
                        seat_count = seat[info].text.split()
                        seats.append(int(seat_count[0])) 
                    else:
                        seats.append(0)

                bus_info = [boardInfor,busRoute,busRouteLink,bus_name,bus_type,dep_time,duration,reach_time,star,price,seats]
                
                if list_length_same(bus_info):
                    print(len(busRoute),len(busRouteLink),len(bus_name),len(bus_type),len(dep_time),len(duration),len(reach_time),len(star),len(price),len(seats))
                    bus_details = pd.DataFrame({"Boards": boardInfor, "Bus_Route": busRoute, "Bus_Route_link":busRouteLink,
                                                "Bus_name":bus_name,"Bus_type":bus_type,
                                                "Dep_time":dep_time,"Duration":duration,
                                                "Reach_time":reach_time,"Star":star,
                                                "Price":price,"Seats":seats})
            
        except Exception as e:
            print(bus_route)
            print(len(busRoute),len(busRouteLink),len(bus_name),len(bus_type),len(dep_time),len(duration),len(reach_time),len(star),len(price),len(seats))
            print(f"Error: {e}")

    path = r"D:\Guvi\busDetails.csv"
    bus_details.to_csv(path,index=False)
except Exception as e:
    print(f"Error: {e}")
# Close the browser
driver.quit()