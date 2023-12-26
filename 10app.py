#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# https://github.com/bsanket16/stock-prediction/tree/master


# In[4]:


import streamlit as st

from datetime import date

import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import cufflinks as cf

import numpy as np
import pandas as pd

from prophet import Prophet
from prophet.plot import plot_plotly


# In[23]:


stocks = ['GAZP', 'ROSN', 'SBERP', 'RTKMP', 'MOEX']


# In[24]:


st.title("Stock Prediction")
st.write("###")

selected_stock = st.selectbox("Select dataset and years for prediction", stocks)

n_years = st.slider("", 1, 5)
period = n_years * 365


# In[13]:


# @st.cache
def get_data(i):
    path = f'{i}_day.csv'
    return pd.read_csv(path, index_col=0, low_memory=False)


# In[ ]:


data_load_state = st.text("Load data ...")
data = get_data(selected_stock)
data = data[['OPEN', 'HIGH', 'LOW', 'CLOSE']]
data_load_state.text("Loading data ... Done!")


# In[ ]:


st.write("###")
st.subheader(f"Stock {selected_stock} data")
st.write(data.tail())


# In[27]:


quotes = data.iloc[-60:]
def plot_raw_data(quotes):
        qf = cf.QuantFig(quotes, title=f'{selected_stock} Exchange Rate', legend='top', name = selected_stock)
        qf.add_bollinger_bands(periods=15, boll_std=2)
        qf.add_rsi(periods=14,showbands=False)
        fig = qf.iplot(asFigure=True)
        st.plotly_chart(fig)


# In[ ]:


plot_raw_data(quotes)


# In[ ]:


# @st.cache
def get_stock_data():
    path = 'stock_day.csv'
    return pd.read_csv(path, low_memory=False)


# In[ ]:


data1 = get_stock_data()


# In[ ]:


df_train = data1[['DATE', selected_stock]]
df_train = df_train.rename(columns={"DATE": "ds", selected_stock: "y"})


# In[ ]:


m = Prophet()
m.add_country_holidays(country_name='RU')
m.fit(df_train)


# In[ ]:


future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)


# In[ ]:


st.write("***")
st.write("###")


# In[ ]:


st.subheader("Forecast data")
st.write(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())


# In[ ]:


fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)


# In[ ]:


st.subheader("Forecast Components")
fig2 = m.plot_components(forecast)
st.write(fig2)


# In[ ]:




