# Data-science

Data Scraping:
Use Selenium to automate the extraction of Redbus data including routes, schedules, prices, and seat availability.
Data Storage:
Store the scraped data in a SQL database.
Streamlit Application:
Develop a Streamlit application to display and filter the scraped data.
Implement various filters such as bustype, route, price range, star rating, availability.
Data Analysis/Filtering using Streamlit:
Use SQL queries to retrieve and filter data based on user inputs.
Use Streamlit to allow users to interact with and filter the data through the application


Modules:
webscrapping.py - Open the redbus url and retrieve the list of government Transport boards. 
redbus_board_scrapping.py - Loop thru the list of government transport boards and obtain the list the routes availables and the respective URLs.
bus_details.py - Loop thru the list of the routes from the previous module and retrieve the bus details. 
store_busDetails.py - Store the bus details in to the SQL Server. 
app.py - Streamlit application to display the database and apply the dynamic filters.
