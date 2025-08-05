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
# storing ticker list
tickerlist = tickerframe["Yahoo Stock Tickers"].tolist()
tickers = st.multiselect("Select 2-3 stocks to view:", tickerlist, default=['AAPL','GOOGL','MSFT'])
# initial data selection
date_range = st.date_input("Select date range",[datetime.date(2015,1,1),datetime.date.today()],min_value=datetime.date(1990,1,1),max_value=datetime.date.today())
start_date,end_date = date_range
data1 = {}
investments = {}
totalinvestment = 0

# range slider plotting function 
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

# var calculation function
def var(pch):
    dictemp = {}
    xlist = [1,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,99]
    for x in xlist:
        dictemp[x] = pch['Close'].quantile(1-(x/100))
    return dictemp

# sharpe ratio calculating function
def sharpe(stodat,stda,enda,bara):
    pch = stodat.loc[stda:enda].pct_change()
    mean_returns = pch['Close'].mean()*252
    base_rate = bara/100
    std_dev = pch['Close'].std()*np.sqrt(252)
    s_r = (mean_returns-base_rate)/(std_dev)
    return s_r

# screen split control
num_stocks = len(tickers)
if num_stocks == 1:
    num_cols = 1
elif num_stocks <= 4:
    num_cols = 2
else:
    num_cols = 3
cols = st.columns(num_cols)

# downloading stock data
for i,ticker1 in enumerate(tickers):
    data1[ticker1] = (yf.download(ticker1,start=start_date,end=end_date))
    data1[ticker1] = data1[ticker1].dropna()
    data1[ticker1] = data1[ticker1][data1[ticker1]['Close']>0]
    if len(data1[ticker1].columns.levels)>1:
        data1[ticker1].columns = data1[ticker1].columns.droplevel(1)
    if data1[ticker1].empty:
        st.warning("No data available for selected timeframe")

# plotting the stock
    with cols[i%num_cols]:
            if len(data1[ticker1])>=2:
                pct_change1 = ((data1[ticker1]['Close'].iloc[-1] - data1[ticker1]['Close'].iloc[-2])*100)/(data1[ticker1]['Close'].iloc[-1])
                st.metric(
                label=f"{ticker1} current price",
                value=f"${data1[ticker1]['Close'].iloc[-1]:.2f}",
                delta=f"{pct_change1}%"
                )
            plotstock(data1[ticker1],ticker1,f'{ticker1} Closing Prices')
            investments[ticker1] = st.number_input(f"How much did u invest in {ticker1}?",value=1)
    totalinvestment+=investments[ticker1]

# initializing portfolio data
portfolio_data = None
if totalinvestment==0:
    totalinvestment=1


st.subheader(f"Total Investment:{totalinvestment}")

# constructing portfolio data
if totalinvestment!=0:
 for ticker1 in data1:
     weighted_price = (investments[ticker1]/totalinvestment) * data1[ticker1]['Close']
     if portfolio_data is None:
         portfolio_data = pd.DataFrame({'Close': weighted_price})
     else:
         portfolio_data['Close'] = portfolio_data['Close'].add(weighted_price,fill_value=0)

# Your portfolio section
with st.expander("Your Portfolio"):
    st.metric(
        label='portfolio current price',
        value=f'${portfolio_data['Close'].iloc[-1]:.2f}',
        delta=((portfolio_data['Close'].iloc[-1]-portfolio_data['Close'].iloc[-2])*100)/(portfolio_data['Close'].iloc[-1])
    )
    plotstock(portfolio_data,'portfolio', 'Portfolio Closing Prices')
    pctchang = portfolio_data.pct_change()*100
    col1,col2 = st.columns(2)
    with col1:
        for key in investments:
            st.markdown("""<p style='font-size: 20px'>Investment in {:}: {:}<p>""".format(key, investments[key]),unsafe_allow_html=True)
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
    st.write("")
    st.write("")
    st.subheader("Sharpe Ratio")
    col1, col2 = st.columns(2)
    with col1:
            date_range_sr = st.date_input("Select date range to view sharpe",[datetime.date(2015,1,1),datetime.date.today()],min_value=datetime.date(1990,1,1),max_value=datetime.date.today())
            start_date_sr,end_date_sr = date_range_sr
            filtered_data = portfolio_data.loc[start_date_sr:end_date_sr]
            base_rate = st.number_input(f"What is the Risk Free Return rate (in %)?",value=3)
            s_r_port = sharpe(portfolio_data,start_date_sr,end_date_sr,base_rate)
            for ticker in data1:
                st.write(f"{ticker} sharpe: {(sharpe(data1[ticker],start_date_sr,end_date_sr,base_rate)):.4f}")
            if s_r_port < 0.5:
                st.markdown("""
            <div style='padding: 20px; color: red; text-align: left; border-radius: 10px;'>
            <h2>Your Sharpe: {:.4f}</h2>
            <p>NEEDS IMPROVEMENT</p>
            </div>
            """.format(s_r_port), unsafe_allow_html=True)
            elif s_r_port < 1:
                st.markdown("""
            <div style='padding: 20px; color: #FAFAD2; text-align: left; border-radius: 10px;'>
            <h2>Your Sharpe: {:.4f}</h2>
            <p>NOT TOO BAD!</p>
            </div>
            """.format(s_r_port), unsafe_allow_html=True)
    
            elif s_r_port < 2:
                st.markdown("""
            <div style='padding: 20px; color: #98FB98; text-align: left; border-radius: 10px;'>
            <h2>Your Sharpe: {:.4f}</h2>
            <p>DECENT!</p>
            </div>
            """.format(s_r_port), unsafe_allow_html=True)
    
            else:
                st.markdown("""
            <div style='padding: 20px; color: #008000; text-align: left; border-radius: 10px;'>
            <p><h2>Your Sharpe: {:.4f}</h2>(EXCELLENT)</p>
            </div>
            """.format(s_r_port), unsafe_allow_html=True)
    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=portfolio_data.index,y=portfolio_data['Close'],mode='lines',name='Portfolio'))
        start_price = filtered_data['Close'].iloc[0]
        end_price = filtered_data['Close'].iloc[-1]
        fig.add_trace(go.Scatter(x=[start_date_sr,end_date_sr],y=[start_price,end_price],mode='lines', name='Linear Growth',line=dict(dash='dash', color='red')))
        fig.update_layout(
            title = 'Portfolio vs linear growth',
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
        
