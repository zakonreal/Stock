#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import streamlit.components.v1 as components

import matplotlib as mpl
import matplotlib.pyplot as plt
import cufflinks as cf
import plotly.io as pio

import numpy as np
import pandas as pd

import requests
import urllib.request
from urllib.parse import urlencode
from urllib.request import urlopen

import webbrowser

import datetime
from datetime import datetime, date, timedelta
import time
import os

from prophet import Prophet
from prophet.plot import plot_plotly

from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.llms import OpenAI

from langchain.chat_models.gigachat import GigaChat
from langchain.chat_models import GigaChat
from langchain.schema import ChatMessage

import pandas as pd
import apimoex
# In[ ]:


stocks = ['GAZP', 'ROSN', 'SBERP', 'RTKMP', 'MOEX']
# stocks = ['GAZP', 'SBERP']
# os.environ['OPENAI_API_KEY'] = "OpenAI API KEY GOES HERE"

# In[ ]:


st.sidebar.title('⚙️Options')


# In[ ]:


selected_stock = st.sidebar.selectbox("Select stock", stocks)


# In[ ]:


ch = st.sidebar.radio("Select chart", ['Candlestick', 'Line'])


# In[ ]:


pr = st.sidebar.radio("Select period", ['1m', '1Y', '3Y'])


# In[ ]:

n_years = st.sidebar.slider("Stock Prediction", 1, 3)
period = n_years * 365   

# In[ ]:
button_c = st.sidebar.button("Predict 🔮")
button_clicked = st.sidebar.button("Report 📊")


# In[ ]:


# @st.cache
# def get_data1(i):
#     path = f'data/{i}_day.csv'
#     return pd.read_csv(path, index_col=0, low_memory=False)


# In[ ]:

def get_data1(i):
    with requests.Session() as session:
            yesterday = date.today() - timedelta(days=1)
            data_end = str(yesterday)
            data = apimoex.get_board_candles(session, i, start = '2020-01-01', end = data_end)
            dfh = pd.DataFrame(data)
            dfh.columns = ['DATE', 'OPEN', 'CLOSE', 'HIGH', 'LOW',  'VOL']
            dfh['DATE'] =  dfh['DATE'].apply(lambda x: x[:10]) 
            # dfh['DATE'] = pd.to_datetime(dfh['DATE'], format='%Y%m%d %H:%M:%S')
            dfh.set_index('DATE', inplace=True)

    return dfh


# In[ ]:

# @st.cache
# def get_data1(cod, data_start = '2022-01-01'):
    
#     data_start = data_start
#     yesterday = date.today() - timedelta(days=1)
#     data_end = str(yesterday)
    
#     # Начальная дата
#     t0 = '.'.join(reversed(data_start.split('-')))
#     t01 = t0.split('.')[2]
#     t02 = str(int(t0.split('.')[1])-1)
#     t03 = t0.split('.')[0]
    
#     # Конечная дата
#     t1 = '.'.join(reversed(data_end.split('-')))
#     t11 = t1.split('.')[2]
#     t12 = str(int(t1.split('.')[1])-1)
#     t13 = t1.split('.')[0]
    
#     p = 8 # период день
#     cod5 = cod # Биржевой курс акций Сбербанк-П  (moex)
#     token='03ADUVZwA9gRNHBgCOuXyphBx7YgdmsSQYVO4KJYqu1HIwjMsNG1XJO5gdMZWjZ5XRq_FY8Ev2QEnQUHnBWFl91ZlAExJav4c39F82glIPI2xIsRHl1lgKedIbUiZBWe5TRZcWTClPBvALDMV8aZMcw64wRAeSgVrg5_p3r3zoVvHnJ5D8PDKNxrMgAhdBcBjeTu8lLA5LLPcpXpb3ZSUFfPZc54ehulaZ4zCngw_ZjB5uz82i_3EMb8zOb49woCsrQmqzj40Qe-o37KklI-VEdVOHp9gZ2jTSwcm_a4veyfj91O4xJmiPg6XeSQdmn8ESulDijDy9BHEhPMUt18dM_4TYztqgGwg-EEsv9h6O_jdAQsPe1mEZ-7CnkRG45ExoszJDe2XnYM9xHMqUwkrEBTZ--IuYNw680_zpp7poUk86I-am6PxhNaRa1NRCcUZM2Gcgr6AvshhOB73R68aFjswX29Kg28sLS8X0uAUJVLPNE2uDyc2Ni64HiDlOnp3CBJNfa1Y8aCfpd9KuNvuz8zBqBalYCf5f_w'
#     maket = {'USDCB': 41,'GAZP': 1, 'ROSN': 1, 'SBERP': 1, 'RTKMP': 1, 'MOEX': 1}
#     em = {'USDCB': 82485,'GAZP': 16842, 'ROSN': 17273, 'SBERP': 23, 'RTKMP': 15, 'MOEX': 152798}
    
#     url =f'https://export.finam.ru/export9.out?market={maket[cod5]}&em={em[cod5]}&token={token}&code={cod5}&apply=0&df={t03}&mf={t02}&yf={t01}&from={t0}&dt={t13}&mt={t12}&yt={t11}&to={t1}&p={p}&f={cod5}_200101_230820&e=.csv&cn={cod5}&dtf=1&tmf=1&MSOR=1&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1'
#     req = urllib.request.Request(
#     url,
#     data=None,
#     headers={
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
#     }
#     )
#     s = urllib.request.urlopen(req)
#     dfd = pd.read_csv(s)
#     dfd.columns = ['TICKER','PER', 'DATE', 'TIME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOL']
#     dfd['DATE'] = pd.to_datetime(dfd['DATE'], format='%Y%m%d')
#     dfd['DATE'] = dfd['DATE'].dt.strftime("%Y-%m-%d")
#     dfd.set_index('DATE', inplace=True)
    
#     return dfd

# In[ ]:

data = get_data1(selected_stock)
data = data[['OPEN', 'HIGH', 'LOW', 'CLOSE']]
data1 = data.copy()
data1['Delta'] = data1['CLOSE'].diff()
data1['%'] = (data1['CLOSE'].pct_change()*100).round(2)

# In[ ]:


st.header(f'📈Stock Analysis {selected_stock}')

# In[ ]:

# @st.cache
def stock_min_now(cod):
    
    data_start = str(date.today())
    yesterday = date.today()
    data_end = str(yesterday)
    
    # Начальная дата
    t0 = '.'.join(reversed(data_start.split('-')))
    t01 = t0.split('.')[2]
    t02 = str(int(t0.split('.')[1])-1)
    t03 = t0.split('.')[0]
    
    # Конечная дата
    t1 = '.'.join(reversed(data_end.split('-')))
    t11 = t1.split('.')[2]
    t12 = str(int(t1.split('.')[1])-1)
    t13 = t1.split('.')[0]
    
    p1 = 2 # период min
    cod5 = cod # Биржевой курс акций Сбербанк-П  (moex)
    token='03ADUVZwA9gRNHBgCOuXyphBx7YgdmsSQYVO4KJYqu1HIwjMsNG1XJO5gdMZWjZ5XRq_FY8Ev2QEnQUHnBWFl91ZlAExJav4c39F82glIPI2xIsRHl1lgKedIbUiZBWe5TRZcWTClPBvALDMV8aZMcw64wRAeSgVrg5_p3r3zoVvHnJ5D8PDKNxrMgAhdBcBjeTu8lLA5LLPcpXpb3ZSUFfPZc54ehulaZ4zCngw_ZjB5uz82i_3EMb8zOb49woCsrQmqzj40Qe-o37KklI-VEdVOHp9gZ2jTSwcm_a4veyfj91O4xJmiPg6XeSQdmn8ESulDijDy9BHEhPMUt18dM_4TYztqgGwg-EEsv9h6O_jdAQsPe1mEZ-7CnkRG45ExoszJDe2XnYM9xHMqUwkrEBTZ--IuYNw680_zpp7poUk86I-am6PxhNaRa1NRCcUZM2Gcgr6AvshhOB73R68aFjswX29Kg28sLS8X0uAUJVLPNE2uDyc2Ni64HiDlOnp3CBJNfa1Y8aCfpd9KuNvuz8zBqBalYCf5f_w'
    maket = {'USDCB': 41,'GAZP': 1, 'ROSN': 1, 'SBERP': 1, 'RTKMP': 1, 'MOEX': 1}
    em = {'USDCB': 82485,'GAZP': 16842, 'ROSN': 17273, 'SBERP': 23, 'RTKMP': 15, 'MOEX': 152798}
    
    # загружаем on-line датасет - Биржевой курс акций Сбербанк-П  (moex)
    url =f'https://export.finam.ru/export9.out?market={maket[cod5]}&em={em[cod5]}&token={token}&code={cod5}&apply=0&df={t03}&mf={t02}&yf={t01}&from={t0}&dt={t13}&mt={t12}&yt={t11}&to={t1}&p={p1}&f={cod5}_200101_230820&e=.csv&cn={cod5}&dtf=1&tmf=1&MSOR=1&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1'
    req = urllib.request.Request(
    url,
    data=None,
    headers={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }
    )
    s = urllib.request.urlopen(req)
    dfh = pd.read_csv(s,  encoding='cp1251')
    dfh.columns = ['TICKER','PER', 'DATE', 'TIME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOL']
    
    dfh['TIME'] = dfh['TIME'].map(lambda x: '00:00:00' if x == 0 else (datetime.strptime(str(x),"%H%M%S")).strftime("%H:%M:%S"))
    dfh['DATE'] = pd.to_datetime(dfh['DATE'], format='%Y%m%d')
    dfh['DATE'] = dfh['DATE'].dt.strftime("%Y-%m-%d")
    dfh['DATE'] = dfh['DATE'] + ' ' + dfh['TIME']
#     dfh['DATE'] = pd.to_datetime(dfh['DATE'], format='%Y%m%d %H:%M:%S')
    dfh.set_index('DATE', inplace=True)

    return dfh[['CLOSE']]

# In[ ]:

st.write("✔️ Now Stock")
b_clicked = st.button("↻")
try:
    if b_clicked == False:
            sto = stock_min_now(selected_stock) 
            if sto.empty:
                sto = data[['CLOSE']].tail(1)
            else:
                sto1 = data[['CLOSE']].tail(1)
                sto2 = sto[['CLOSE']].tail(1)
                s = pd.concat([sto1, sto2], ignore_index=False)
                s['Delta'] = s['CLOSE'].diff()
                s['%'] = (s['CLOSE'].pct_change() *100).round(2)
            st.write(s.tail(1))
    else:
            sto = stock_min_now(selected_stock)
            if sto.empty:
                sto = dat1[['CLOSE']].tail(1)
            else:
                sto1 = data[['CLOSE']].tail(1)
                sto2 = sto[['CLOSE']].tail(1)
                s = pd.concat([sto1, sto2], ignore_index=False)
                s['Delta'] = s['CLOSE'].diff()
                s['%'] = (s['CLOSE'].pct_change()*100).round(2)
            st.write(s.tail(1))
except:
            st.write(data[['CLOSE']].tail(1))
     #       sto = data1[['CLOSE']].tail(1)
# In[ ]:

st.write("Financial Data")
st.write(data1.tail())


# In[ ]:

if pr == '1m':
    quotes = data.iloc[-30:]
if pr == '1Y':
    quotes = data.iloc[-365:]
if pr == '3Y':
    quotes = data.iloc[-1095:]


# In[ ]:


def plot_raw_data(quotes, selected_stock):
        qf = cf.QuantFig(quotes, title=f'{selected_stock} Exchange Rate', legend='top', name = selected_stock)
        qf.add_bollinger_bands(periods=15, boll_std=2)
        qf.add_rsi(periods=14,showbands=False)
        fig = qf.iplot(asFigure=True)
        # pio.write_image(fig, f'{selected_stock} Rate.png')
        st.plotly_chart(fig)
        
        


# In[ ]:


st.write("Chart")
if ch == 'Candlestick': 
    plot_raw_data(quotes, selected_stock)
if ch == 'Line':
    quotes[f'{selected_stock} Rate'] = quotes['CLOSE']
    quotes[f'{selected_stock} Rate'].plot();  
    plt.savefig(f'{selected_stock} Rate.png');
    st.line_chart(quotes[f'{selected_stock} Rate'])

# In[ ]:


# @st.cache
def get_mfso(i):
    if i == 'SBERP': i = 'SBER'
    if i == 'RTKMP': i = 'RTKM'
    path = f'data/MSFO_{i}.csv'
    return pd.read_csv(path, index_col=0, low_memory=False)


# In[ ]:


mfso = get_mfso(selected_stock)


# In[ ]:


st.write("Fundamental Analysis")
st.write(mfso.fillna('-').tail(4))


# In[ ]:


# @st.cache
def get_news(i):
    if i == 'SBERP': i = 'SBER'
    if i == 'RTKMP': i = 'RTKM'
    path = f'data/{i}_news.csv'
    return pd.read_csv(path, index_col=0, low_memory=False)[['title', 'site', 'url']].tail()


# In[ ]:

st.write("News Stock")
news = get_news(selected_stock)
news.columns = ['Тема', 'Источник', 'Адрес']
st.write(news.to_html(render_links=True, escape=False), unsafe_allow_html=True)

# In[ ]:

# query = st.sidebar.text_input("Enter a query:") 

#  # Execute pandas response logic
# if st.sidebar.button("Execute ❓") and query:
#         with st.sidebar.spinner('Generating response...'):
#             try:

#                  # Define pandas df agent - 0 ~ no creativity vs 1 ~ very creative
#                 agent = create_pandas_dataframe_agent(OpenAI(temperature=0.0),data1,verbose=True) 

#                 # Run agent and retrieve answer
#                 answer = agent.run(query)

#                 # Display user query and agents answer
#                 st.write(user_template.replace("{{MSG}}",query ), unsafe_allow_html=True)
#                 st.write(bot_template.replace("{{MSG}}", answer ), unsafe_allow_html=True)
#                 st.write("")

#             except Exception as e:
#                 st.error(f"An error occurred: {str(e)}")


# In[ ]:


# 1. Set up multiple variables to store the titles, text within the report
# Настройте несколько переменных для хранения заголовков и текста в отчете.
# @st.cache
def rep(selected_stock):
        page_title_text=f'{selected_stock} report'
        title_text = f'📈Stock Analysis {selected_stock}'
        t1  = "✔️ Now Stock"
        t2  = "Forecast"
        text = 'Financial Data'
        chart_text = 'Chart'
        f_text = 'Fundamental Analysis'
        n_text = 'News Stock'


        # 2. Combine them together using a long f-string
        # Соедините их вместе, используя длинную f-строку.
        html = f'''
            <html>
                <head>
                    <title>{page_title_text}</title>
                </head>
                <body>
                    <h1>{title_text}</h1>
                    <p>{t1}</p>
                    {sto.tail(1).to_html()}
                    <p>{text}</p>
                    {data1.tail().to_html()}
                    <h2>{chart_text}</h2>
                    f'<img src = '{selected_stock} Rate.png' width="700">'
                    <h2>{f_text}</h2>
                    {mfso.fillna('-').tail(4).to_html()}
                    <h2>{n_text}</h2>
                    {news.to_html(render_links=True, escape=False)}
                </body>
            </html>
            '''
        # 3. Write the html string as an HTML file
        # Запишите строку html как файл HTML.
        with open(f'{selected_stock}_report.html', 'w', encoding="utf-8") as f:
            f.write(html)


# In[ ]:

if button_clicked:
            rep(selected_stock)
            webbrowser.open(f'{selected_stock}_report.html')

        
# # @st.cache            
# def get_pred_data(i):
#     path = f'{i}_day.csv'
#     return pd.read_csv(path, low_memory=False)[['DATE', 'CLOSE']]
# @st.cache  
def get_pred_data1(cod, data_start = '2013-01-01'):
    
    data_start = data_start
    yesterday = date.today() - timedelta(days=1)
    data_end = str(yesterday)
    
    # Начальная дата
    t0 = '.'.join(reversed(data_start.split('-')))
    t01 = t0.split('.')[2]
    t02 = str(int(t0.split('.')[1])-1)
    t03 = t0.split('.')[0]
    
    # Конечная дата
    t1 = '.'.join(reversed(data_end.split('-')))
    t11 = t1.split('.')[2]
    t12 = str(int(t1.split('.')[1])-1)
    t13 = t1.split('.')[0]
    
    p = 8 # период день
    cod5 = cod # Биржевой курс акций Сбербанк-П  (moex)
    token='03ADUVZwA9gRNHBgCOuXyphBx7YgdmsSQYVO4KJYqu1HIwjMsNG1XJO5gdMZWjZ5XRq_FY8Ev2QEnQUHnBWFl91ZlAExJav4c39F82glIPI2xIsRHl1lgKedIbUiZBWe5TRZcWTClPBvALDMV8aZMcw64wRAeSgVrg5_p3r3zoVvHnJ5D8PDKNxrMgAhdBcBjeTu8lLA5LLPcpXpb3ZSUFfPZc54ehulaZ4zCngw_ZjB5uz82i_3EMb8zOb49woCsrQmqzj40Qe-o37KklI-VEdVOHp9gZ2jTSwcm_a4veyfj91O4xJmiPg6XeSQdmn8ESulDijDy9BHEhPMUt18dM_4TYztqgGwg-EEsv9h6O_jdAQsPe1mEZ-7CnkRG45ExoszJDe2XnYM9xHMqUwkrEBTZ--IuYNw680_zpp7poUk86I-am6PxhNaRa1NRCcUZM2Gcgr6AvshhOB73R68aFjswX29Kg28sLS8X0uAUJVLPNE2uDyc2Ni64HiDlOnp3CBJNfa1Y8aCfpd9KuNvuz8zBqBalYCf5f_w'
    maket = {'USDCB': 41,'GAZP': 1, 'ROSN': 1, 'SBERP': 1, 'RTKMP': 1, 'MOEX': 1}
    em = {'USDCB': 82485,'GAZP': 16842, 'ROSN': 17273, 'SBERP': 23, 'RTKMP': 15, 'MOEX': 152798}
    
    url =f'https://export.finam.ru/export9.out?market={maket[cod5]}&em={em[cod5]}&token={token}&code={cod5}&apply=0&df={t03}&mf={t02}&yf={t01}&from={t0}&dt={t13}&mt={t12}&yt={t11}&to={t1}&p={p}&f={cod5}_200101_230820&e=.csv&cn={cod5}&dtf=1&tmf=1&MSOR=1&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1'
    req = urllib.request.Request(
    url,
    data=None,
    headers={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }
    )
    s = urllib.request.urlopen(req)
    dfd = pd.read_csv(s)
    dfd.columns = ['TICKER','PER', 'DATE', 'TIME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOL']
    dfd['DATE'] = pd.to_datetime(dfd['DATE'], format='%Y%m%d')
    dfd['DATE'] = dfd['DATE'].dt.strftime("%Y-%m-%d")
    # dfd.set_index('DATE', inplace=True)
    
    return dfd[['DATE', 'CLOSE']]
    
if button_c:
        df_train = get_pred_data1(selected_stock)
        df_train = df_train.rename(columns={"DATE": "ds", 'CLOSE': "y"})

        m = Prophet()
        m.add_country_holidays(country_name='RU')
        m.fit(df_train)

        future = m.make_future_dataframe(periods=period)
        forecast = m.predict(future)
        d = date.today()
        if d.weekday() in [0,5,6]: future_1 = m.make_future_dataframe(periods=3)
        else: future_1 = m.make_future_dataframe(periods=1)
        forecast_1 = m.predict(future_1)

        st.write("***")
        st.write("###")

        st.write("Forecast")
        forecast1 = forecast_1[['ds', 'yhat']].copy()
        forecast1 = forecast_1.rename(columns={"ds": "DATE", "yhat": 'CLOSE'})
        st.write(forecast1[['DATE', 'CLOSE']].tail(1))

        fig1 = plot_plotly(m, forecast)
        st.plotly_chart(fig1)

        st.write("Forecast Components")
        fig2 = m.plot_components(forecast)
        st.write(fig2)
        
# In[3]:
with st.sidebar:
    st.title("GIGACHAT API")
    base_url = st.selectbox(
        "GIGACHAT_BASE_URL",
        (
            "https://gigachat.devices.sberbank.ru/api/v1",
            "https://beta.saluteai.sberdevices.ru/v1",
        ),
    )
    st.title("Авторизационные данные")
    credentials = st.text_input("GIGACHAT_CREDENTIALS", type="password")
    # st.title("OR")
    # access_token = st.text_input("GIGACHAT_ACCESS_TOKEN", type="password")
    # st.title("OR")
    # user = st.text_input("GIGACHAT_USER")
    password = st.text_input("GIGACHAT_PASSWORD", type="password")


# Initialize chat history
st.title("GigaChain Bot")
if "messages" not in st.session_state:
        st.session_state.messages = [
            ChatMessage(
                role="system",
                content="Ты - опытный торговый трейдер, который обладает необходимыми знаниями и опытом для того, чтобы помочь пользователю сделать правильный выбор и принять обоснованное решение в покупке и продаже акций российских компаний.",),
            ChatMessage(role="assistant", content="Как я могу помочь вам?"),
        ]


# Display chat messages from history on app rerun
for message in st.session_state.messages:
        with st.chat_message(message.role):
            st.markdown(message.content)

if prompt := st.chat_input():
    if not credentials:
        st.info("Заполните данные GigaChat для того, чтобы продолжить")
        st.stop()

    chat = GigaChat(
        base_url=base_url,
        credentials=credentials,
        access_token=st.session_state.get("token"),
        password=password,
        verify_ssl_certs=False,
    )

    message = ChatMessage(role="user", content=prompt)
    st.session_state.messages.append(message)

    with st.chat_message(message.role):
        st.markdown(message.content)

    message = ChatMessage(role="assistant", content="")
    st.session_state.messages.append(message)

    with st.chat_message(message.role):
        message_placeholder = st.empty()
        for chunk in chat.stream(st.session_state.messages):
            message.content += chunk.content
            message_placeholder.markdown(message.content + "▌")
        message_placeholder.markdown(message.content)

    # Каждый раз, когда пользователь нажимает что-то в интерфейсе весь скрипт выполняется заново.
    # Сохраняем токен и закрываем соединения
    st.session_state.token = chat._client.token
    chat._client.close()

# In[3]:


# from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtWebEngineWidgets import QWebEngineView

# class Ui_Form(object):
#     def setupUi(self, Form):
#         Form.setObjectName("Form")
#         Form.resize(1019, 593)

#         self.webView = QWebEngineView(parent=Form)
#         self.webView.setGeometry(QtCore.QRect(0, 30, 1021, 561))
#         self.webView.setObjectName("webView")

#         self.retranslateUi(Form)
#         QtCore.QMetaObject.connectSlotsByName(Form)

#     def retranslateUi(self, Form):
#         _translate = QtCore.QCoreApplication.translate
#         Form.setWindowTitle("Report")
#         '''
#         with open("SBERP_report.html", 'r') as f:
#             html = f.read()
#             self.webView.setHtml(html)
#         '''
        
# class Window(QtWidgets.QWidget, Ui_Form):
#     def __init__(self, parent = None):
#         super().__init__(parent)
#         self.setupUi(self)
        
#         file = "C:/Users/150ho/Desktop/DE/pro/SBERP_report.html"            # !!! +++
#         self.webView.load(QtCore.QUrl.fromLocalFile(file))  # !!! +++        


# In[8]:


# import sys
# app = QtWidgets.QApplication(sys.argv)
# w = Window()
# w.show()
# '''
#     Form = QtWidgets.QWidget()
#     ui = Ui_Form()
#     ui.setupUi(Form)
#     Form.show()
# '''
# sys.exit(app.exec())


# In[ ]:





# In[ ]:




