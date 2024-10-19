import requests
import pandas as pd
import yfinance as yf
from newscatcherapi import NewsCatcherApiClient


#-------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_stocks(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)
    data.reset_index(inplace=True) 
    data['Date'] = pd.to_datetime(data['Date'])  
    return data

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_news(api_key, query, start_date, end_date):
    url = ('https://newsapi.org/v2/everything?'
           f'q={query}&from={start_date}&to={end_date}&sortBy=popularity&'
           'sources=bloomberg,cnbc,financial-times,reuters,business-insider&'
           f'apiKey={api_key}')
    
    headers = {'User-Agent': 'NewsAPI Client'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        data = response.json() 
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []
    except ValueError:
        print("Error decoding the response as JSON")
        return []
    
    articles = data.get('articles', [])
    return articles