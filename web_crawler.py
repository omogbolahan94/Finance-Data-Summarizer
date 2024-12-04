
import aiohttp
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_financial_data(company_name=None):
    """
    Searches the web for financial data of the given company name.
    Returns stock price, market cap, and P/E ratio (if available).
    """
    driver = webdriver.Chrome()

    finance_data = {'Previous close': '', 'Day range': '', 'Year range': '',
                'Market cap': '', 'Avg Volume': '', 'P/E ratio': '',
                'Dividend yield': '', 'Primary exchange': ''}

    suffix = {'NASDAQ':['GOOGL', 'AAPL', 'MFST', 'AMZN', 'TSLA', 'META', 'NVDA', 'DUOL'],
              'NYSE':['JPM', 'V', 'KO']}

    query = ''
    if company_name is None:
        return None
        
    for k, v in suffix.items():
      if company_name in v:
        query = f"{company_name.upper()}:{k}"
        print(query, 'stock price financial data exists')
        break
      else: return f"Data for the company '{company_name}' could not the found."

    search_url = f"https://www.google.com/finance/quote/{query}"

    try:
        driver.get(search_url)
        driver.implicitly_wait(10)
        elements = driver.find_elements(By.CLASS_NAME, 'P6K39c')
        for i, item in enumerate(elements[:8]):
            k = list(finance_data.keys())[i]
            finance_data[k] = item.text
        return finance_data
    except Exception as e:
        return e
    else:
        return {"error": "Web search failed"}

# print(get_financial_data('DUOL'))