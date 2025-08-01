import yfinance as yf
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import datetime
import plotly.express as px
from storbrr import tickerframe
st.set_page_config(layout="wide", page_title="Portfolio Dashboard")
st.title("Investment Portfolio Display")

tickerlist = tickerframe["Yahoo Stock Tickers"].tolist()
tickers = st.multiselect("Select 2-3 stocks to view:", tickerlist, default=['AAPL','GOOGL','MSFT'])
date_range = st.date_input("Select date range",[datetime.date(2015,1,1),datetime.date.today()],min_value=datetime.date(1990,1,1),max_value=datetime.date.today())
start_date,end_date = date_range
data1 = {}
investments = {}
totalinvestment = 0
def plotstock(plotthis,nam,tit):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=plotthis.index,y=plotthis['Close'],mode='lines',name=nam))
    fig.update_layout(
        title = tit,
        xaxis = dict(rangeslider = dict(visible=True),
                 rangeselector = dict(
                    buttons = list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
                 ),
                 type = 'date')
    )
    st.plotly_chart(fig,use_container_width=True)

def var(pch):
    dictemp = {}
    xlist = [1,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,99]
    for x in xlist:
        dictemp[x] = pch['Close'].quantile(1-(x/100))
    return dictemp

num_stocks = len(tickers)
if num_stocks == 1:
    num_cols = 1
elif num_stocks <= 4:
    num_cols = 2
else:
    num_cols = 3
cols = st.columns(num_cols)

for i,ticker1 in enumerate(tickers):
    data1[ticker1] = (yf.download(ticker1,start=start_date,end=end_date))
    data1[ticker1] = data1[ticker1].dropna()
    data1[ticker1] = data1[ticker1][data1[ticker1]['Close']>0]
    if len(data1[ticker1].columns.levels)>1:
        data1[ticker1].columns = data1[ticker1].columns.droplevel(1)
    if data1[ticker1].empty:
        st.warning("No data available for selected timeframe")
# st.dataframe(data1)
#Plotly with range slider:
    with cols[i%num_cols]:
            if len(data1[ticker1])>=2:
                pct_change = ((data1[ticker1]['Close'].iloc[-1] - data1[ticker1]['Close'].iloc[-2])*100)/(data1[ticker1]['Close'].iloc[-1])
                st.metric(
                label=f"{ticker1} current price",
                value=f"${data1[ticker1]['Close'].iloc[-1]}",
                delta=f"{pct_change}%"
                )
            plotstock(data1[ticker1],ticker1,f'{ticker1} Closing Prices')
            investments[ticker1] = st.number_input(f"How much did u invest in {ticker1}?",value=1)
#   investments[ticker1] = st.number_input(f"How much did u invest in {ticker1}?")
    totalinvestment+=investments[ticker1]
# More robust - collect all weighted prices first
# Initialize portfolio_data properly
portfolio_data = None
if totalinvestment==0:
    totalinvestment=1
#sk

st.write(f"Total Investment:{totalinvestment}")
if totalinvestment!=0:
 for ticker1 in data1:
     weighted_price = (investments[ticker1]/totalinvestment) * data1[ticker1]['Close']
     if portfolio_data is None:
         # First stock - create the DataFrame
         portfolio_data = pd.DataFrame({'Close': weighted_price})
     else:
         # Subsequent stocks - add to existing
         portfolio_data['Close'] = portfolio_data['Close'].add(weighted_price,fill_value=0)


with st.expander("Your Portfolio"):
    st.metric(
        label='portfolio current price',
        value=f'${portfolio_data['Close'].iloc[-1]}',
        delta=((portfolio_data['Close'].iloc[-1]-portfolio_data['Close'].iloc[-2])*100)/(portfolio_data['Close'].iloc[-1])
    )
    plotstock(portfolio_data,'portfolio', 'Portfolio Closing Prices')
    pctchang = portfolio_data.pct_change()*100
    col1,col2 = st.columns(2)
    with col1:
        for key in investments:
            st.write(f"Investment in {key}: {investments[key]}")
    with col2:
        if st.toggle("View Percentage Change"):
            plotstock(pctchang,'Percentage Change', 'Portfolio: Daily Returns')
            st.metric("Your returns per dollar from starting date to end date:",f'${(portfolio_data['Close'][-1]/portfolio_data['Close'][0])}')
    st.subheader("Portfolio Diversification Analysis")
    returns = pd.DataFrame()
    for ticker in data1:
        returns[ticker] = data1[ticker]['Close'].pct_change()
    corr_mat = returns.corr()
    col1, col2 = st.columns(2)  # Give col1 less space
    with col2:
        mask = np.triu(np.ones_like(corr_mat, dtype=bool), k=1)
        avg_correlation = corr_mat.where(mask).stack().mean()
        fig = px.imshow(
        corr_mat,
        text_auto=True,
        aspect="equal",
        color_continuous_scale='RdYlGn_r',
        color_continuous_midpoint=0,
        title="Stock Correlation Heatmap"
        )
        fig.update_layout(
            title_x=0.22
        )
        st.plotly_chart(fig, use_container_width=True)
    with col1:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        if avg_correlation < 0.2:
            st.markdown("""
            <div style='padding: 20px; background-color: #d4f6d4; color: #2d5016; text-align: center; border-radius: 10px;'>
            <h2>WELL DIVERSIFIED</h2>
            <p>Avg correlation: {:.2f}</p>
            </div>
            """.format(avg_correlation), unsafe_allow_html=True)
    
        elif avg_correlation < 0.5:
            st.markdown("""
            <div style='padding: 20px; background-color: #fff3cd; color: #856404; text-align: center; border-radius: 10px;'>
            <h2>MODERATELY DIVERSIFIED</h2>
            <p>Avg correlation: {:.2f}</p>
            </div>
            """.format(avg_correlation), unsafe_allow_html=True)
    
        else:
            st.markdown("""
            <div style='padding: 20px; background-color: #f8d7da; color: #721c24; text-align: center; border-radius: 10px;'>
            <h2>POORLY DIVERSIFIED</h2>
            <p>Avg correlation: {:.2f}</p>
            </div>
            """.format(avg_correlation), unsafe_allow_html=True)
    for x in range(3):
        st.write('')
    st.subheader("**VaR:**")
    dic2 = var(pctchang) 
    xlist, ylist = [],[]
    for key in dic2:
        xlist.append(key)
        ylist.append(dic2[key])
    fig = px.bar(x=xlist,y=ylist,labels={'x': 'Percentile', 'y': 'Return %'})
    st.plotly_chart(fig,use_container_width=True)
    st.write("")
    st.write("")
    st.write(f"**Interpretation:** You will lose less than {dic2[95]}% of your investment tomorrow, 95% of the time, and gain more than {dic2[50]}% of your investment tomrrow, 50% of the time")

