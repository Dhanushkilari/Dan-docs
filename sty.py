import pandas as pd
import mysql.connector
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import time

#Andhra Pradesh
lists_ap=[]
df_1=pd.read_csv("F:/New folder (2)/redbus12/df_1.csv")
for i,r in df_1.iterrows():
    lists_ap.append(r["route_name"])

# kerala 
lists_ks=[]
df_2=pd.read_csv("F:/New folder (2)/redbus12/df_2.csv")
for i,r in df_2.iterrows():
    lists_ks.append(r["route_name"])

#Telungana bus
lists_ts=[]
df_3=pd.read_csv("F:/New folder (2)/redbus12/df_3.csv")
for i,r in df_3.iterrows():
    lists_ts.append(r["route_name"])

#Goa bus
lists_kt=[]
df_4=pd.read_csv("F:/New folder (2)/redbus12/df_4.csv")
for i,r in df_4.iterrows():
    lists_kt.append(r["route_name"])

#Assam
lists_as=[]
df_5=pd.read_csv("F:/New folder (2)/redbus12/df_5.csv")
for i,r in df_5.iterrows():
    lists_as.append(r["route_name"])


# punjab
lists_ps=[]
df_6=pd.read_csv("F:/New folder (2)/redbus12/df_6.csv")
for i,r in df_6.iterrows():
    lists_ps.append(r["route_name"])

# Haryana 
lists_hr=[]
df_7=pd.read_csv("F:/New folder (2)/redbus12/df_7.csv")
for i,r in df_7.iterrows():
    lists_hr.append(r["route_name"])

#Bihar
lists_bs=[]
df_8=pd.read_csv("F:/New folder (2)/redbus12/df_8.csv")
for i,r in df_8.iterrows():
    lists_bs.append(r["route_name"])

#West Bengal
lists_wb=[]
df_9=pd.read_csv("F:/New folder (2)/redbus12/df_9.csv")
for i,r in df_9.iterrows():
    lists_wb.append(r["route_name"])

#Chandighar
lists_ct=[]
df_10=pd.read_csv("F:/New folder (2)/redbus12/df_10.csv")
for i,r in df_10.iterrows():
    lists_ct.append(r["route_name"])

#setting up streamlit page
st.set_page_config(layout="wide")

web=option_menu(menu_title="REDBUS TRANSPORTATION",
                options=["Home","States and Routes"],
                icons=["house","info-circle"],
                orientation="horizontal"
                )
# Home page setting
if web=="Home":
    st.image("F:/New folder (2)/redbus12/redbuslogo.png",width=200)
    st.title("Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit")


# States and Routes page setting
if web == "States and Routes":
    S = st.selectbox("Lists of States", ["Adhra Pradesh", "Kerala", "Telugana", "Goa", "Assam", 
                                          "Punjab", "Haryana", "Bihar", "WestBengal","Chandighar"])
    
    col1,col2=st.columns(2)
    with col1:
        select_type = st.radio("Choose bus type", ("sleeper", "semi-sleeper", "others"))
    with col2:
        select_fare = st.radio("Choose bus fare range", ("50-1000", "1000-2000", "2000 and above"))
    TIME=st.time_input("select the time")


    # Adhra Pradesh bus fare filtering
    if S=="Adhra Pradesh":
        A=st.selectbox("list of routes",lists_ap)

        def type_and_fare_A(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="Dan@123", database="red_bus")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{A}"
                AND {bus_type_condition} AND Departure_time>='{TIME}'
                ORDER BY Price and Departure_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Departure_time", "Arival_time", "Duration",
                "Price", "Seats_Available", "Rating", "route_link", "route_name"
            ])
            return df

        df_result = type_and_fare_A(select_type, select_fare)
        st.dataframe(df_result)

    # Kerala bus fare filtering
    if S == "Kerala":
        K = st.selectbox("List of routes",lists_ks)

        def type_and_fare_K(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="Dan@123", database="red_bus")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{K}"
                AND {bus_type_condition} AND Departure_time>='{TIME}'
                ORDER BY Price and Departure_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Departure_time", "Arival_time", "Duration",
                "Price", "Seats_Available", "Rating", "route_link", "route_name"
            ])
            return df

        df_result = type_and_fare_K(select_type, select_fare)
        st.dataframe(df_result)      

    # 
    if S=="Telugana":
        T=st.selectbox("list of routes",lists_ts)

        def type_and_fare_T(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="Dan@123", database="red_bus")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{T}"
                AND {bus_type_condition} AND Departure_time>='{TIME}'
                ORDER BY Price and Departure_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Departure_time", "Arival_time", "Duration",
                "Price", "Seats_Available", "Rating", "route_link", "route_name"
            ])
            return df

        df_result = type_and_fare_T(select_type, select_fare)
        st.dataframe(df_result)

    # Goa bus fare filtering
    if S=="Goa":
        G=st.selectbox("list of routes",lists_kt)

        def type_and_fare_G(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="Dan@123", database="red_bus")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{G}"
                AND {bus_type_condition} AND Departure_time>='{TIME}'
                ORDER BY Price and Departure_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Departure_time", "Arival_time", "Duration",
                "Price", "Seats_Available", "Rating", "route_link", "route_name"
            ])
            return df

        df_result = type_and_fare_G(select_type, select_fare)
        st.dataframe(df_result)

    # Assam
    if S=="Assam":
        A_1=st.selectbox("list of routes",lists_as)

        def type_and_fare_A_1(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="Dan@123", database="red_bus")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{A_1}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
                ORDER BY Price and Start_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Departure_time", "Arival_time", "Duration",
                "Price", "Seats_Available", "Rating", "route_link", "route_name"
            ])
            return df

        df_result = type_and_fare_A_1(select_type, select_fare)
        st.dataframe(df_result)
          

    # Punjab      
    if S=="Punjab":
        P=st.selectbox("list of rotes",lists_ps)

        def type_and_fare_P(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="Dan@123", database="red_bus")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{P}"
                AND {bus_type_condition} AND Departure_time>='{TIME}'
                ORDER BY Price and Departure_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Departure_time", "Arival_time", "Duration",
                "Price", "Seats_Available", "Rating", "route_link", "route_name"
            ])
            return df

        df_result = type_and_fare_P(select_type, select_fare)
        st.dataframe(df_result)
    
    # Haryana
    if S=="Haryana":
        H=st.selectbox("list of rotes",lists_hr)

        def type_and_fare_H(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="Dan@123", database="red_bus")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{H}"
                AND {bus_type_condition} AND Departure_time>='{TIME}'
                ORDER BY Price and Departure_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Departure_time", "Arival_time", "Duration",
                "Price", "Seats_Available", "Rating", "route_link", "route_name"
            ])
            return df

        df_result = type_and_fare_H(select_type, select_fare)
        st.dataframe(df_result)


    # Bihar
    if S=="Bihar":
        B=st.selectbox("list of rotes",lists_bs)

        def type_and_fare_B(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="Dan@123", database="red_bus")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{B}"
                AND {bus_type_condition} AND Departure_time>='{TIME}'
                ORDER BY Price and Departure_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Departure_time", "Arival_time", "Duration",
                "Price", "Seats_Available", "Rating", "route_link", "route_name"
            ])
            return df

        df_result = type_and_fare_B(select_type, select_fare)
        st.dataframe(df_result)

    # WestBengal
    if S=="West Bengal":
        W=st.selectbox("list of rotes",lists_wb)

        def type_and_fare_W(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="Dan@123", database="red_bus")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{W}"
                AND {bus_type_condition} AND Departure_time>='{TIME}'
                ORDER BY Price and Departure_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Departure_time", "Arival_time", "Duration",
                "Price", "Seats_Available", "Rating", "route_link", "route_name"
            ])
            return df

        df_result = type_and_fare_W(select_type, select_fare)
        st.dataframe(df_result)

    # Chandighar
    if S=="Chandighar":
        C=st.selectbox("list of rotes",lists_ct)

        def type_and_fare_C(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="Dan@123", database="red_bus")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{C}"
                AND {bus_type_condition} AND Departure_time>='{TIME}'
                ORDER BY Price and Departure_time  DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Departure_time", "Arival_time", "Duration",
                "Price", "Seats_Available", "Rating", "route_link", "route_name"
            ])
            return df

        df_result = type_and_fare_C(select_type, select_fare)
        st.dataframe(df_result)