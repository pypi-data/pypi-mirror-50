
# coding: utf-8

# In[1]:


import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like # https://stackoverflow.com/questions/50394873/import-pandas-datareader-gives-importerror-cannot-import-name-is-list-like
import pandas_datareader.data as web


# In[2]:


# http://pandas-datareader.readthedocs.io/en/latest/remote_data.html
# https://ntguardian.wordpress.com/2016/09/19/introduction-stock-market-data-python-1/
def download_tables(ticker, start=pd.Timestamp('1800-01-01'), end=pd.Timestamp.today()): # read table data from the star page to end page
    df = web.DataReader(ticker, 'fred', start, end)
    return df


# In[3]:


def update_data_in_db(filepath, ticker, COL_DATE = 'DATE'):
    try:
        df = pd.read_csv(filepath) # read the already sorted data
        df[COL_DATE] = pd.to_datetime(df[COL_DATE])
        latestDate = df.iloc[-1][COL_DATE] # temporarily save the latest date
        if latestDate < pd.Timestamp.today():
            start=latestDate + pd.Timedelta(seconds=1)
            end=pd.Timestamp.today()
            df0 = download_tables(ticker, start, end)
            df0.reset_index(inplace=True)
            df = pd.concat([df, df0])
    except:
        print("File not found in the database. Now, searching the internet to download information...")
        df = download_tables(ticker) # download the data from the website
        df.reset_index(inplace=True)
        print("Downloading completed.")
    df.sort_values(COL_DATE, inplace = True) # sort in order of date & time
    df.to_csv(filepath, index=False) # save the data to db
    return df


# In[4]:


if False:
    ticker = 'UNRATE'
    df = download_tables(ticker)

    import matplotlib.pyplot as plt
    get_ipython().run_line_magic('matplotlib', 'inline')
    df['UNRATE'].plot(grid = True)
if False:
    df = update_data_in_db('c:/Users/bomso/bomsoo1/project/python/unemply.csv', 'UNRATE')
    print(df.iloc[-35:])

