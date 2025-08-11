# Investment Portfolio Dashboard 

The project is an interactive Streamlit web app that lets you track, analyze, and visualize your investment portfolio. 
! [Portfolio Dashboard Screenshot](prfolioscrsht.png)

## Features:
1) Live Market Data : Fetches historical stock data from Yahoo Finance.
2) Portfolio Tracking : Track investments per stock and see combined portfolio value over time.
3) Interactive Charts : Zoom, filter, and explore data with Plotly line charts and sliders.
4) Key Metrics: Current prices & daily changes, Portfolio diversification (correlation heatmap), Value at Risk (VaR), Sharpe Ratio (risk-adjusted return).
5) Flexible Date Ranges.
6) User-Friendly UI : Built entirely using Streamlit, includes toggles, expanders, and responsive layouts.

## Installation:
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/portfolio-dashboard.git
   cd portfolio-dashboard
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   streamlit run findash1.py (alternatively, use python -m streamlit run findash1.py)
   ```
## How to Use:
1) Select Stocks : Choose 2–3 stocks from the dropdown.
2) Pick Date Range : Define the analysis period.
3) Enter Investments : Input how much you’ve invested in each stock.
4) Analyze : View portfolio value, diversification, VaR, Sharpe Ratio, and interactive charts.

## Metrics Explained:
1) VaR (Value at Risk) : Historical worst-case losses for different confidence levels.
2) Sharpe Ratio : Measures return per unit of risk (higher is better).
3) Diversification Score : Based on average correlation between selected assets.

## License: 
MIT License - free to use and modify.



