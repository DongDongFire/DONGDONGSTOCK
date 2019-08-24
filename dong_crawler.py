#!/usr/bin/env python
# coding: utf-8

# In[27]:


import pandas as pd
from bs4 import BeautifulSoup
import requests
import os

__all__ = ['stock_pirce_history']


class stock_price_history:
    
    code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]  
    code_df.종목코드=code_df.종목코드.map('{:06d}'.format)
    code_df=code_df[['회사명','종목코드']]
    code_df=code_df.rename(columns={'회사명':'name','종목코드':'code'})
    def __init__(self, corp_name):
        self.corp_name=corp_name
    
    def get_price(self):

        code=self.code_df.query("name=='{}'".format(self.corp_name))['code'].to_string(index=False)
        code=code.strip()
        url='https://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)

        df=pd.DataFrame()
        for page in range(1,100):
            pg_url='{url}&page={page}'.format(url=url,page=page)
            df=df.append(pd.read_html(pg_url,header=0)[0],ignore_index=True)

        df=df.dropna()

        df=df.rename(columns={'날짜':'Date','종가':'Close','거래량':'Volume','전일비':'Diff'})
        df2=df.drop(['시가','고가','저가'],axis=1)
        df2['Diff']=list(df2.set_index('Date').diff()['Close'])
        return code, df2

