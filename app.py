import streamlit as st
import pandas as pd
import pymysql
import math as m

@st.cache_data(ttl=3600)
def get_boards():
    connection = pymysql.connect(
            host = 'localhost', user = 'root', 
            password = 'Maddy@1208', database='RedBus_Data')
    sql = """ 
        SELECT boards as Boards FROM bus_routes  
    """
    return pd.read_sql(sql,connection)

def get_routes():
    connection = pymysql.connect(
            host = 'localhost', user = 'root', 
            password = 'Maddy@1208', database='RedBus_Data')
    sql = """ 
        SELECT route_name as Routes FROM bus_routes  
    """
    return pd.read_sql(sql,connection)

def get_busname():
    connection = pymysql.connect(
            host = 'localhost', user = 'root', 
            password = 'Maddy@1208', database='RedBus_Data')
    sql = """ 
        SELECT busname as Bus_Name FROM bus_routes  
    """
    return pd.read_sql(sql,connection)

def get_bustype():
    connection = pymysql.connect(
            host = 'localhost', user = 'root', 
            password = 'Maddy@1208', database='RedBus_Data')
    sql = """ 
        SELECT bustype as Bus_Type FROM bus_routes  
    """
    return pd.read_sql(sql,connection)

def get_departureTime():
    connection = pymysql.connect(
            host = 'localhost', user = 'root', 
            password = 'Maddy@1208', database='RedBus_Data')
    sql = """ 
        SELECT departing_time as Departing_Time FROM bus_routes  
    """
    return pd.read_sql(sql,connection)

def get_duration():
    connection = pymysql.connect(
            host = 'localhost', user = 'root', 
            password = 'Maddy@1208', database='RedBus_Data')
    sql = """ 
        SELECT duration as Duration FROM bus_routes  
    """
    return pd.read_sql(sql,connection)

def get_reachingTime():
    connection = pymysql.connect(
            host = 'localhost', user = 'root', 
            password = 'Maddy@1208', database='RedBus_Data')
    sql = """ 
        SELECT reaching_time as Reaching_Time FROM bus_routes  
    """
    return pd.read_sql(sql,connection)

def get_rating():
    connection = pymysql.connect(
            host = 'localhost', user = 'root', 
            password = 'Maddy@1208', database='RedBus_Data')
    sql = """ 
        SELECT star_rating as Rating FROM bus_routes  
    """
    return pd.read_sql(sql,connection)

def get_price():
    connection = pymysql.connect(
            host = 'localhost', user = 'root', 
            password = 'Maddy@1208', database='RedBus_Data')
    sql = """ 
        SELECT MIN(price) as Min_Price, MAX(price) as Max_Price FROM bus_routes  
    """
    return pd.read_sql(sql,connection)   
                 
def get_availableSeats():
    connection = pymysql.connect(
            host = 'localhost', user = 'root', 
            password = 'Maddy@1208', database='RedBus_Data')
    sql = """ 
        SELECT seats_available as Available FROM bus_routes  
    """
    return pd.read_sql(sql,connection)   

def get_info(col_name):
    connection = pymysql.connect(
            host = 'localhost', user = 'root', 
            password = 'Maddy@1208', database='RedBus_Data')
    sql = f""" 
        SELECT {col_name} FROM bus_routes  
    """
    return pd.read_sql(sql,connection)  

def get_bus_details():
    connection = pymysql.connect(
            host = 'localhost', user = 'root', 
            password = 'Maddy@1208', database='RedBus_Data')
    sql = """ 
        SELECT boards as Boards,
                route_name as Routes,
                busname as Bus_Name, 
                bustype as Bus_Type, 
                departing_time as Departing_Time, 
                duration as Duration, 
                reaching_time as Reaching_Time, 
                star_rating as Star_Rating, 
                price as Price, 
                seats_available as Seats_Available 
                FROM bus_routes  
    """
    return pd.read_sql(sql,connection)   

def time64_toNormalTime(parm):
    time64_value = pd.Timedelta(parm)
    hours = time64_value.components.hours
    mins = time64_value.components.minutes
    return f'{hours}:{mins}'

st.set_page_config(layout='wide')
#sidebar widgets
st.sidebar.header('Filters')

bus_details = get_bus_details()

for i in range(0,len(bus_details)):    
    bus_details['Departing_Time'][i] = time64_toNormalTime(bus_details['Departing_Time'][i])
    bus_details['Reaching_Time'][i] = time64_toNormalTime(bus_details['Reaching_Time'][i])

with st.sidebar.form("filter_form"):
    # board = get_info("boards")
    board = get_boards()
    boards = st.selectbox(label="Boards", index=None, options=board['Boards'].unique())

    route = get_routes()
    routes = st.selectbox(label="Routes", index=None, options=route['Routes'].unique())

    busname = get_busname()
    busn = st.selectbox(label="Bus Name", index=None, options=busname['Bus_Name'].unique())

    bustype = get_bustype()
    bust = st.selectbox(label="Bus Type", index=None, options=bustype['Bus_Type'].unique())

    deptime = get_departureTime()
    dept = st.selectbox(label="Departing Time", index=None, options=deptime['Departing_Time'].unique())

    reachtime = get_reachingTime()
    reach = st.selectbox(label="Reaching Time", index=None, options=reachtime['Reaching_Time'].unique())

    fare = get_price()
    min = int(round(fare['Min_Price'].values[0]))
    max = int(m.ceil(fare['Max_Price'].values[0]))
    price = st.slider(label="Price", min_value=0, max_value=max, value=min)

    submit = st.form_submit_button("Apply")

    if submit:
        if boards:
            bus_details = bus_details[bus_details['Boards'] == boards]
        if routes:
            bus_details = bus_details[bus_details['Routes'] == routes]
        if busn:
            bus_details = bus_details[bus_details['Bus_Name'] == busn]
        if bust:
            bus_details = bus_details[bus_details['Bus_Type'] == bust]
        if dept:
            bus_details = bus_details[bus_details['Departing_Time'] == dept]
        if reach:
            bus_details = bus_details[bus_details['Reaching_Time'] == reach] 
        if price:
            bus_details = bus_details[bus_details['Price'] <= price]            
    
st.subheader('RedBus - Bus Details')

st.dataframe(bus_details,hide_index=True)