import streamlit as st
from PIL import Image
import pandas as pd

import yfinance as yf
import matplotlib.pyplot as plt
import os

import datetime
from pandas_datareader import data as pdr

import pymongo
from pymongo import MongoClient

#adding a title and an image
st.write("""
# Stock Market Application
Stock Price prediction....
""")

image = Image.open("C:/Users/utilisateur/Desktop/project_trading/stock.jpg")
st.image(image, use_column_width=True)

#sidebar header
st.sidebar.header('User Imput')

#funtion to get the users input
def get_input():
    start_date = st.sidebar.text_input("Start Date", "2020-08-01")
    end_date = st.sidebar.text_input("End Date", "2020-09-04")
    stock_symbol = st.sidebar.text_input("Stock Symbol", "GOOG")
    return start_date, end_date, stock_symbol

#function to get the company name
def get_comp_name(symbol):
    if symbol == "AMZN":
        return 'Amazon'
    elif symbol == "AAPL":
        return 'Appel'
    elif symbol == "GOOG":
        return 'Alphabet'
    elif symbol == "TSLA":
        return "Tesla"
    elif symbol == "MSFT":
        return "Microsoft"
    elif symbol == "FB":
        return "FaceBook"
    else: 
        "None"
#function to get the companies time frame
def get_data(symbol, start, end):
    
    #load data
    if symbol.upper() == "AMZN":
        df = pd.read_csv('C:/Users/utilisateur/Desktop/project_trading/data/AMZN.csv')
    elif symbol.upper() == "GOOG":
        df = pd.read_csv('C:/Users/utilisateur/Desktop/project_trading/data/GOOG.csv')
    elif symbol.upper() == "TSLA":
        df = pd.read_csv('C:/Users/utilisateur/Desktop/project_trading/data/TSLA.csv')
    elif symbol.upper() == "MSFT":
        df = pd.read_csv('C:/Users/utilisateur/Desktop/project_trading/data/MSFT.csv')
    elif symbol.upper() == "FB":
        df = pd.read_csv('C:/Users/utilisateur/Desktop/project_trading/data/FB.csv') 
    elif symbol.upper() == "AAPL":
        df = pd.read_csv('C:/Users/utilisateur/Desktop/project_trading/data/AAPL.csv')
        

    #get the date range
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)

    #set start and end index
    start_row = 0
    end_row = 0

    #start the date from the top of the dataset
    for i in range(0, len(df)):
        if start <= pd.to_datetime(df['Date'][i]):
            start_row = i
            break
            
    #start from the bottom of the dataset
    for j in range(0, len(df)):
        if end >= pd.to_datetime(df['Date'][len(df)-1-j]):
            end_row = len(df) - 1 - j
            break

    #set index to the date
    df = df.set_index(pd.DatetimeIndex(df['Date'].values))
    
    return df.iloc[start_row: end_row +1, :]

    
#get users input
start, end, symbol = get_input()
#get date
df = get_data(symbol, start, end)
#get the company name
company_name = get_comp_name(symbol.upper())

#dispaly the Adj Close price
st.header(company_name+" Adj Close Price\n")
st.line_chart(df['Adj Close'])

#dispaly the Volume
st.header(company_name+" Volume\n")
st.line_chart(df['Volume'])

#get statistics 
#st.header('Data Statistics')
#st.write(df.describe())

#get model
st.header('Model LSTM')
start_sp = datetime.datetime(2010, 1, 1)
end_sp = datetime.datetime(2020, 9, 24)

yf.pdr_override() # <== that's all it takes :-)
GOOD = pdr.get_data_yahoo('GOOG', start_sp, end_sp)
    
GOOD.head()

#using mongodb
myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient["Stocks"]
mycol = mydb["Tickers"]

myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient["Stocks"]
mycol = mydb["Tickers"]

# Step 2: Insert Data into DB
#GOOG.reset_index(inplace=True) # Reset Index
#data_dict = GOOG.to_dict("records") # Convert to dictionary
#mycol.insert_one({"Index":"GOOG","data":data_dict}) # inesrt into DB

# Step 3: Get data from DB
#st.sidebar.header('User Imput')

#funtion to get the users input
#def get_input():
    #data_from_db = mycol.find_one({"symbol":"GOOG"})
    #GOOG = pd.DataFrame(data_from_db["data"])
    #GOOG.set_index("Date",inplace=True)


