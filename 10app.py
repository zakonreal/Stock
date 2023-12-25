#!/usr/bin/env python
# coding: utf-8

# In[20]:


import streamlit as st

from datetime import date

import matplotlib as mpl
import seaborn as sns

import numpy as np
import pandas as pd


# In[21]:


# import matplotlib.pyplot as plt


# In[22]:


import cufflinks as cf


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
st.subheader("Raw data")
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





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




