# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 07:36:32 2020

@author: yasin
"""

# import libraries
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime as dt
from datetime import date, timedelta
import pandas_datareader.data as web
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
#set working directory
os.chdir('C:/Users/yasin/Desktop/python/trading')

#The first function for extracting all constitutents of XU30 index.
def x30_tickers():    
    # specify the url
    url = "http://finans.mynet.com/borsa/endeks/xu030-bist-30/endekshisseleri/"
    # query the website and return the html to the variable ‘page’
    page = urlopen(url)
    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(page, "html.parser")
    table=soup.find_all('table')
    x30 = []
    for row in table[0].find_all('tr'):
        for stock in row.find_all('a'):
            #print(stock.text[0:5].strip())#[0:5] für first 5 elemnts of stock which is the code
            #Strip() for removing spaces of codes which are 4 letters
            x30.append(stock.text[0:5].strip())
    return x30
x30_tickers()
#The second function for extracting all data of XU30 constituents.
def get_yahoo_data():
    tickers = x30_tickers()
    os.makedirs('stock_dfs')   
    start = dt.datetime(2019, 1, 1)
    end = date.today()
    for ticker in tickers:#[:5]
        stockname = ticker + ".IS"
        df = web.DataReader(stockname, 'yahoo', start, end)
        df.to_csv('stock_dfs/{}.csv'.format(ticker))
get_yahoo_data()

#The third function is for combin all 'Adj Close' in another file.
def combine_data():
    main_df = pd.DataFrame()
    tickers=x30_tickers()
    for ticker in tickers:
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df.set_index('Date',inplace = True)
        
        df.rename(columns = {'Adj Close': ticker}, inplace = True)
        df.drop(['Open','High','Low','Close','Volume'],1, inplace= True)
        if main_df.empty:
            main_df=df
        else:
            main_df=main_df.join(df,how='outer')
    #print(main_df.head())
    main_df.to_csv('xu030_joined_closes.csv')        
    
combine_data()

def x30_corr():
    df = pd.read_csv('xu030_joined_closes.csv')
    df_corr = df.corr()
    print(df_corr.head())
    data = df_corr.values
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    
    heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)
    fig.colorbar(heatmap)
    ax.set_xticks(np.arange(data.shape[1]) + 0.5, minor = False)
    ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor = False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    
    column_labels = df_corr.columns
    row_labels = df_corr.index
    
    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)
    plt.xticks(rotation=90)
    heatmap.set_clim(-1,1)
    plt.tight_layout()
    plt.show()
x30_corr()    

