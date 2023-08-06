#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


#ref) https://medium.com/@ageitgey/quick-tip-the-easiest-way-to-grab-data-out-of-a-web-page-in-python-7153cecfca58
def download_table(url): 
    dfs = pd.read_html(url, header=0) # read tables and save them into a list of dataframes
    df = dfs[0]  # select the first element of the list
    df.dropna(axis=0, inplace=True) # axis=0: remove rows that contain NaN
    ii = df.iloc[:,0].str.contains('\d').values # excluding non-digit rows by checking the first column
    return df.loc[ii,]
def download_tables(url_, start=1, end=5, print_url = False): # read table data from the start page to end page
    dfs = list()
    for i in range(start, end+1):
        url = url_ + str(i) # create a complete url for naver web page
        if (print_url == True):
            print(url)
        df0 = download_table(url) # download a table from a naver web page
        if (i != start) and (pd.DataFrame.equals(dfs[-1], df0) or len(df0.index)==0): # stop conditions
            break
        else:
            dfs.append(df0)
    df = pd.concat(dfs)
    return df


# In[3]:


def update_data_in_db(filepath, url_, COL_DATE = '날짜', MAX_PAGE = 99999, print_url = False):
    try:
        df = pd.read_csv(filepath) # read the already sorted data
        latestDate = df.iloc[-1][COL_DATE] # temporarily save the latest date
        for i in range(1, MAX_PAGE):
            url = url_ + str(i) # create a complete url for naver web page
            df0 = download_table(url)
            if any(df0[COL_DATE] == latestDate):
                df.drop(df.index[df[COL_DATE] == latestDate], inplace=True) # drop the last row 
                df = pd.concat([df, df0[df0[COL_DATE] >= latestDate]])
                break
            else:
                df = pd.concat([df, df0])
    except:
        print("File not found in the database. Now, searching the internet to download information...")
        df = download_tables(url_, start = 1, end = MAX_PAGE, print_url = print_url) # download the data from the website
        print("Downloading completed.")
    df.sort_values(COL_DATE, inplace = True) # sort in order of date & time
    df.to_csv(filepath, index=False) # save the data to db
    return df


# In[6]:


if False:
#     df = download_table('http://finance.naver.com/item/sise_day.nhn?code=035420&page=1')
#     df = download_table('http://info.finance.naver.com/marketindex/exchangeDailyQuote.nhn?marketindexCd=FX_USDKRW&page=1')
    df = download_table('https://finance.naver.com/marketindex/exchangeDailyQuote.nhn?marketindexCd=FX_CADKRW&page=403')
    print(df)
if False:
#     df = download_tables('http://finance.naver.com/item/sise_day.nhn?code=035420&page=', 1, 15)
#     df = download_tables('https://finance.naver.com/item/sise_day.nhn?code=000660&page=', 542, 547, print_url = True)
    df = download_tables('https://finance.naver.com/marketindex/exchangeDailyQuote.nhn?marketindexCd=FX_CADKRW&page=', 376, 380, print_url = True)
    print(df)
if False:
#    df = update_data_in_db('c:/Users/bomso/bomsoo1/project/python/naver.csv', 'http://finance.naver.com/item/sise_day.nhn?code=035420&page=')
#    df = update_data_in_db('c:/Users/bomso/bomsoo1/project/python/samsung.csv', 'http://info.finance.naver.com/marketindex/exchangeDailyQuote.nhn?marketindexCd=FX_USDKRW&page=')
#    df = update_data_in_db('c:/Users/bomso/bomsoo1/project/python/kospi.csv', 'http://finance.naver.com/sise/sise_index_day.nhn?code=KOSPI&page=')
#     df = update_data_in_db('c:/Users/bomso/bomsoo1/project/python/gold.csv', 'http://info.finance.naver.com/marketindex/goldDailyQuote.nhn?&page=')
    df = update_data_in_db('C:/Users/bomsoo/bomsoo1/project/python/project_stock_db_csv/CADKRW.csv', 'https://finance.naver.com/marketindex/exchangeDailyQuote.nhn?marketindexCd=FX_CADKRW&page=')
    
    #df['종가'].plot(xlim=(pd.Timestamp('2016-01-01'), pd.Timestamp.today()), ylim=(400000,1000000))

    print(df.iloc[-35:])


# In[ ]:





# In[ ]:




