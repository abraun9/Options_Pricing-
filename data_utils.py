import numpy as np
import yfinance as yf
from datetime import datetime

def get_stock_price(ticker):
    """
    Fetch the latest stock price from Yahoo Finance.
    
    Parameters:
    - ticker: Stock ticker symbol (e.g., 'AAPL')
    
    Returns:
    - Latest stock price or None if the ticker is invalid
    """
    try:
        stock_data = yf.Ticker(ticker)
        history = stock_data.history(period="1d")
        if history.empty:
            return None
        return history['Close'].iloc[-1]
    except Exception:
        return None

def get_time_to_maturity(expiration_date):
    """
    Calculate the time to maturity in years from the current date.
    
    Parameters:
    - expiration_date: The expiration date of the option
    
    Returns:
    - Time to maturity in years
    """
    try:
        current_date = datetime.now()
        T = (expiration_date - current_date).days / 365
        return T
    except Exception as e:
        print(f"Error calculating time to maturity: {e}")
        return None

def get_risk_free_rate():
    """
    Fetch the current risk-free rate from Yahoo Finance (1-year Treasury yield).
    
    Returns:
    - Risk-free interest rate (annualized)
    """
    try:
        treasury_data = yf.Ticker("^IRX")
        r = treasury_data.history(period="1d")['Close'].iloc[-1] / 100
        return r
    except Exception as e:
        print(f"Error fetching risk-free rate: {e}")
        return None

def get_volatility(ticker, start_date, end_date):
    """
    Calculate historical volatility based on stock price data.
    
    Parameters:
    - ticker: Stock ticker symbol (e.g., 'AAPL')
    - start_date: Start date for the historical data
    - end_date: End date for the historical data
    
    Returns:
    - Volatility of the stock (annualized)
    """
    try:
        data = yf.download(ticker, start=start_date, end=end_date)['Close']
        returns = data.pct_change().dropna()
        sigma = np.std(returns) * np.sqrt(252)
        return sigma
    except Exception as e:
        print(f"Error calculating volatility for {ticker}: {e}")
        return None