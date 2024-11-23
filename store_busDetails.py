from bus_details import *
import pymysql

# Function Definition
def creation_of_table(cursor, table_name, table_create_declaration):
    create_table_query = f"""create table {table_name}({table_create_declaration});"""
    print("create_table_query = ", create_table_query)
    cursor.execute(create_table_query)
    print("Table Created Successfully")

def insertion_into_table(cursor, connection, table_name, table_insert_declaration, values_to_be_inserted):
    insert_table_query = f"""insert into {table_name} {table_insert_declaration};"""
    cursor.executemany(insert_table_query, values_to_be_inserted) # To insert Multiple record      
    connection.commit()
    return "Success"

def fetching_from_table(cursor, table_name, column_selector, flag, condition):
    if flag == 'all':
        fetching_from_table_query = f"""select {column_selector} from {table_name};"""
    else:
        fetching_from_table_query = f"""select {column_selector} from {table_name} where {condition};"""
    cursor.execute(fetching_from_table_query)
    fetch_all_result = cursor.fetchall()
    return len(fetch_all_result)

def drop_table(cursor, connection, table_name):
    delete_from_table_query = f"drop table {table_name}"
    cursor.execute(delete_from_table_query)
    print("Successfully dropped")
    connection.commit()    

def check_table_exists(table_name):
    inquire = f"select count(*) from information_schema.tables where table_name = '{table_name}'"
    cursor.execute(inquire)
    if cursor.fetchone()[0] == 1:
        return True
    else:
        return False

try:
    # Connection Parameters
    connection = pymysql.connect(
         host = 'localhost', user = 'root', 
         password = 'Maddy@1208')
    cursor = connection.cursor()
    create_database = "create database if not exists RedBus_Data"
    cursor.execute(create_database)
    use_database = "use RedBus_Data"
    cursor.execute(use_database)
        
    # Create the Table bus_routes
    redbus_table = 'bus_routes'

    table_exists = check_table_exists(redbus_table)

    if table_exists == True:
        #Fetching of results
        column_selector, flag, condition = '*', 'all', ''   
        number_of_records = fetching_from_table(cursor, redbus_table, column_selector, flag, condition)
        print(number_of_records)
        if number_of_records > 0:
            drop_table(cursor, connection, redbus_table)

    table_exists = check_table_exists(redbus_table)
    if table_exists == False:
        table_create_declaration = "id INT auto_increment primary key, boards VARCHAR(50), route_name VARCHAR(100), route_link VARCHAR(255), busname VARCHAR(255), bustype VARCHAR(255), departing_time TIME, duration VARCHAR(20), reaching_time TIME, star_rating FLOAT, price DECIMAL(10,2), seats_available INT" 
        creation_of_table(cursor, redbus_table, table_create_declaration) # Function Calling   
    
    # Values Inserting in Table
    data = bus_details.values.tolist()

    table_insert_declaration = "(boards, route_name, route_link, busname, bustype, departing_time, duration, reaching_time, star_rating, price, seats_available) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    insertion_into_table(cursor, connection, redbus_table, table_insert_declaration, data)
    
except Exception as e:
    print(str(e))

