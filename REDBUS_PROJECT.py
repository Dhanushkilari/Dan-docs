from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import pandas as pd
import time


driver = webdriver.Chrome()
    
url = "https://www.redbus.in/"

op = []
for value in ["apsrtc","ksrtc-kerala","tsrtc","ktcl","rsrtc","south-bengal-state-transport-corporation-sbstc","hrtc","astc","uttar-pradesh-state-road-transport-corporation-upsrtc","wbtc-ctc","pepsu"]:
    url_placeholder= f"https://www.redbus.in/online-booking/{value}/?utm_source=rtchometile"
    driver.get(url_placeholder)
    
    routes = []
    for a in driver.find_elements(By.CLASS_NAME,'route'):
        routes.append(a.get_attribute('href'))

    for route in routes:
        driver.get(route)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        route_name = [s.text for s in soup.find_all("div",attrs={"class":"clearfix main-body border-wrap"})]
        route_link = [s.text for s in soup.find_all("div",attrs={"class":"button view-seats fr"})]
        bus_name = [s.text for s in soup.find_all("div",attrs={"class":"travels lh-24 f-bold d-color"})]
        bus_type = [s.text for s in soup.find_all("div",attrs={"class":"bus-type f-12 m-top-16 l-color evBus"})]
        departing_time = [s.text for s in soup.find_all("div",attrs={"class":"dp-time f-19 d-color f-bold"})]
        duration = [s.text for s in soup.find_all("div",attrs={"class":"dur l-color lh-24"})]
        reaching_time = [s.text for s in soup.find_all("div",attrs={"class":"bp-time f-19 d-color disp-Inline"})]
        star_rating = [s.text for s in soup.find_all("div",attrs={"class":"rating-sec 1h-24"})]
        price = [s.text for s in soup.find_all("div",attrs={"class":"seat-fare"})]
        seats_available = [s.text for s in soup.find_all("div",attrs={"class":"column-eight w-15 fl"})]
        
        test = {
            "route_name":route_name,
            "route_link":route_link,
            "bus_name":bus_name,
            "bus_type":bus_type,
            "departing_time":departing_time,
            "duration":duration,
            "reaching_time":reaching_time,
            "star_rating":star_rating,
            "price":price,
            "seats_available":seats_available
        
        }
        
        test = pd.DataFrame.from_dict(test,orient='index')
        test=test.transpose()
        test["route"] = route
        test["value"] = value
        op.append(test)
    
        time.sleep(5)
        #break
    
    #break

result  = pd.concat(op)
print(result)

#streamlit
import streamlit as st
import mysql.connector
connection=mysql.connector.connect(
    host='localhost',
    user='Revathipriya Selvamani',
    password='1216',
    database='result'
)
print('connected')

cursor =connection.cursor()
cursor.execute('select * all' from result)
print(cursor.fetchall())

st.title('Streamlit MySQL Connection')
df=pd.DataFrame(data,columns=cursor.column_names)
st.dataframe(df)