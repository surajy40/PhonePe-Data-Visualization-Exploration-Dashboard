# Importing important libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
import json
import requests
import os
import warnings
warnings.filterwarnings("ignore")
import mysql.connector

sns.set_style("whitegrid")

# My sql connection
connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root",
    database = "phonepe_data"

 )

# Function to run sql query
def run_query(query):
    return pd.read_sql(query, connection)

# Creating the side bar

st.sidebar.title("📌 Navigation")

page = st.sidebar.radio(
    "Go to",
    ["🏠 Home", "📊 Questions"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("Created by Suraj")

# Home page

if page == "🏠 Home":

    #creating logo
    col1, col2, col3 = st.columns([1,2,3])

    with col2:
        st.image("C:/Users/91886/Desktop/My Computer/Project_guvi/now/pngwing.com.png", width=500)

    st.header("👋 Welcome to PhonePe Dashboard")

    st.markdown("""
    This dashboard provides insights into:

    - 📈 Transactions across India  
    - 📱 Mobile brand usage  
    - 🛡️ Insurance adoption  
    - 👥 User engagement  

    👉 Go to **Questions** to explore analysis.
    """)

    st.info("Use the sidebar to navigate.")

# Sidebar 

elif page == "📊 Questions":
    st.header("📊 Analysis Questions")

    analysis = st.sidebar.selectbox(
        "Choose Questions",
        [
            "1. Which State have the highest number of transactions?",
            "2. How do transaction grow across quarters?",
            "3. Which transaction type dominates PhonePe?",
            "4. Which mobile brand are most used?",
            "5. Which State is the highest insurance adoption?",
            "6. Which districts have highest volume of transaction?",
            "7. Which States have highest registered users?",
            "8. Which districts show highest app engagement?",
            "9. Which state generate highest transaction value?",
            "10. Which districs show highest insurance transaction?"
        ]
    ) 

    q_id = analysis.split(".")[0]

# Question 1

    if q_id == "1":

        st.header("Which State have the highest number of transactions?")

        query = """
                SELECT States,
                SUM(Transaction_count) AS Total_transaction
                FROM aggregated_transaction
                GROUP BY States
                ORDER BY Total_transaction DESC;
                """
        
        df = run_query(query)
        st.dataframe(df)

        fig,ax = plt.subplots()
        sns.barplot(data=df.head(10), x= "Total_transaction", y="States", ax=ax)
        ax.set_title("Top States by Transactions")

        st.pyplot(fig)

        geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        geojson = requests.get(geojson_url).json()

        state_mapping = {
            "andaman & nicobar islands": "Andaman & Nicobar", "andhra pradesh": "Andhra Pradesh",
            "arunachal pradesh": "Arunachal Pradesh","assam": "Assam","bihar": "Bihar","chandigarh": "Chandigarh",
            "chhattisgarh": "Chhattisgarh","dadra & nagar haveli & daman & diu": "Dadra and Nagar Haveli and Daman and Diu",
            "delhi": "Delhi","goa": "Goa","gujarat": "Gujarat","haryana": "Haryana","himachal pradesh": "Himachal Pradesh",
            "jammu & kashmir": "Jammu & Kashmir","jharkhand": "Jharkhand","karnataka": "Karnataka","kerala": "Kerala","ladakh": "Ladakh",
            "madhya pradesh": "Madhya Pradesh","maharashtra": "Maharashtra","manipur": "Manipur","meghalaya": "Meghalaya","mizoram": "Mizoram",
            "nagaland": "Nagaland","odisha": "Odisha","puducherry": "Puducherry","punjab": "Punjab","rajasthan": "Rajasthan",
            "sikkim": "Sikkim","tamil nadu": "Tamil Nadu","telangana": "Telangana","tripura": "Tripura",
            "uttar pradesh": "Uttar Pradesh","uttarakhand": "Uttarakhand","west bengal": "West Bengal"
        }

        df["States"] = df["States"].str.lower()
        df["States"] = df["States"].map(state_mapping)

        fig_map = px.choropleth(
        df,
        geojson=geojson,
        featureidkey="properties.ST_NM",
        locations="States",
        color="Total_transaction",
        color_continuous_scale="Reds",
        title="India State-wise Transactions"
    )

        fig_map.update_geos(fitbounds="locations", visible=False)

        st.plotly_chart(fig_map)


# Question 2

    elif q_id == "2":

        st.header("How do transaction grow across quarters?")

        query = """
                SELECT Years, Quarter,
                SUM(Transaction_count) AS Total_transaction
                FROM aggregated_transaction
                GROUP BY Years, Quarter
                ORDER BY Years, Quarter;
                """
        
        df = run_query(query)
        st.dataframe(df)

        fig,ax = plt.subplots()
        sns.lineplot(data=df, x="Quarter", y="Total_transaction", hue="Years", markers="o", ax=ax)
        ax.set_title("Quarterly Transaction Growth")

        st.pyplot(fig)

        fig2, ax2 = plt.subplots()

        sns.barplot(data=df,x="Quarter",y="Total_transaction",hue="Years",ax=ax2)
        ax2.set_title("Quarter-wise Transactions Comparison")

        st.pyplot(fig2)


# Question 3

    elif q_id == "3":

        st.header("Which transaction type dominates PhonePe?")

        query = """
                SELECT Transaction_type,
                SUM(Transaction_count) AS Total_transactions
                FROM aggregated_transaction
                GROUP BY Transaction_type
                """
        
        df = run_query(query)
        st.dataframe(df)

        fig,ax = plt.subplots()
        ax.pie(df["Total_transactions"], labels=df["Transaction_type"], autopct="%1.1f%%")
        ax.set_title("Transaction Type Distribution")

        st.pyplot(fig)

# Question 4

    elif q_id == "4":

        st.header("Which mobile brand are most used?")

        query = """
                SELECT Brands,
                SUM(Transaction_count) AS Users
                FROM aggregated_user
                GROUP BY Brands
                ORDER BY Users DESc
                """
        
        df = run_query(query)
        st.dataframe(df)
        
        fig, ax = plt.subplots()
        sns.barplot(data=df.head(10), x="Users", y="Brands", ax=ax)
        ax.set_title("Top Mobile Brands")

        st.pyplot(fig)


        fig_tree = px.treemap(df.head(15),
                     path=["Brands"],
                     values="Users",
                     title="Top Mobile Brands")

        st.plotly_chart(fig_tree)


# Question 5

    elif q_id == "5":

        st.header("Which State is the highest insurance adoption?")

        query = """
                SELECT States,
                SUM(Transaction_count) AS Insurance_transactions
                FROM aggregated_insurance
                GROUP BY States
                ORDER BY Insurance_transactions DESC
                """
        
        df = run_query(query)
        st.dataframe(df)

        fig,ax = plt.subplots()
        sns.barplot(data=df.head(10), x="Insurance_transactions", y="States", ax=ax)
        ax.set_title("Insurance Adoption By States")

        st.pyplot(fig)

        fig_donut = px.pie(df.head(10),
                  names="States",
                  values="Insurance_transactions",
                  hole=0.4,
                  title="Insurance Adoption By States")

        st.plotly_chart(fig_donut)


# Question 6

    elif q_id == "6":

        st.header("Which districts have highest volume of transaction?")

        query = """
                SELECT Districts,
                SUM(Transaction_count) AS Transactions
                FROM map_transaction
                GROUP BY Districts
                ORDER BY Transactions DESC
                LIMIT 10
                """
        
        df = run_query(query)
        st.dataframe(df)

        fig,ax = plt.subplots()
        sns.barplot(data=df, x="Transactions", y="Districts", ax=ax)
        ax.set_title("Top Districts Transactions Wise")

        st.pyplot(fig)

        fig_scatter = px.scatter(df, x="Districts", y="Transactions", size="Transactions",          
        color="Transactions",hover_name="Districts",title="Top Districts Transactions Wise")

        st.plotly_chart(fig_scatter)

# Question 7

    elif q_id == "7":

        st.header("Which States have highest registered users?")

        query = """
                SELECT States,
                SUM(RegisteredUsers) AS Users
                FROM top_user
                GROUP BY States
                ORDER BY Users DESC
                """
        
        df = run_query(query)
        st.dataframe(df)

        fig,ax = plt.subplots()
        sns.barplot(data=df.head(10), x="Users", y="States", ax=ax)
        ax.set_title("Top States By RegisteredUsers")

        st.pyplot(fig)

       # india map

        geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        geojson = requests.get(geojson_url).json()

        fig_map = px.choropleth( df,geojson=geojson,featureidkey="properties.ST_NM",
            locations="States",color="Users", color_continuous_scale="Blues",
            title="India State-wise Registered Users")

        fig_map.update_geos(fitbounds="locations", visible=False)

        st.plotly_chart(fig_map)


# Question 8

    elif q_id == "8":

        st.header("Which districts show highest app engagement?")

        query = """
                SELECT Districts,
                SUM(AppOpens) AS App_opens
                FROM map_user
                GROUP BY Districts
                ORDER BY App_opens DESC
                LIMIT 10
                """
        
        df = run_query(query)
        st.dataframe(df)

        fig,ax = plt.subplots()
        sns.barplot(data=df, x="App_opens", y="Districts", ax=ax)
        ax.set_title("Top District By App Engagement")

        st.pyplot(fig)

        fig_scatter = px.scatter(df,x="App_opens",y="Districts",size="App_opens",color="App_opens", hover_name="Districts",
        color_continuous_scale="Plasma",title="District-wise App Opens (Bubble View)")

        st.plotly_chart(fig_scatter)


# Question 9

    elif q_id == "9":

        st.header("Which state generate highest transaction value?")

        query = """
                SELECT States,
                SUM(Transaction_amount) AS Total_amount
                FROM aggregated_transaction
                GROUP BY States
                ORDER BY Total_amount DESC
                """
        
        df = run_query(query)
        st.dataframe(df)

        fig,ax = plt.subplots()
        sns.barplot(df.head(10), x="Total_amount", y="States", ax=ax)
        ax.set_title("Top States By Trabsaction Amoyunt Value")

        st.pyplot(fig)

        # India map
        geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        geojson = requests.get(geojson_url).json()

        fig_map = px.choropleth(df,geojson=geojson,featureidkey="properties.ST_NM",
            locations="States",color="Total_amount",color_continuous_scale="Greens",
            title="India State-wise Transaction Amount")

        fig_map.update_geos(fitbounds="locations", visible=False)

        st.plotly_chart(fig_map)


# Question 10

    elif q_id == "10":

        st.header("Which districs show highest insurance transaction?")

        query = """
                SELECT Districts,
                SUM(Transaction_count) AS Insurance_transactions
                FROM map_insurance
                GROUP BY Districts
                ORDER BY Insurance_transactions DESC
                LIMIT 10
                """
        
        df = run_query(query)
        st.dataframe(df)

        fig,ax = plt.subplots()
        sns.barplot(data=df, x="Insurance_transactions", y="Districts", ax=ax)
        ax.set_title("Top Districts By Insurance")

        st.pyplot(fig)

        fig_tree = px.treemap(df,path=["Districts"],
                values="Insurance_transactions",title="Insurance Transaction Distribution")

        st.plotly_chart(fig_tree)


        