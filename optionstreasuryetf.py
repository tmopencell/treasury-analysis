import pandas_datareader.data as web
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import requests

def get_historical_volatility(prices, window=30):
    """Calculate historical volatility from daily returns"""
    returns = np.log(prices / prices.shift(1))
    return returns.rolling(window=window).std() * np.sqrt(252)  # Annualized

def get_tlt_data():
    """Get TLT price data from Jan 2024 to Jan 2025"""
    start_date = pd.Timestamp('2024-01-01')
    end_date = pd.Timestamp('2025-01-31')
    
    try:
        hist = web.DataReader('TLT', 'av-daily',
                            start_date, end_date,
                            api_key='CFFZLL3MH1R3VKB7')
        print("Successfully retrieved TLT data")
        # Ensure index is datetime
        hist.index = pd.to_datetime(hist.index)
        print("Date range:", hist.index[0], "to", hist.index[-1])
        return hist
    except Exception as e:
        print(f"Error getting TLT data: {e}")
        return None

def price_bond(fv, T, ytm, coup, freq=2):
    """Calculate bond price"""
    freq = float(freq)
    periods = T*freq
    coupon = coup/100*fv/freq
    
    dt = [(i+1)/freq for i in range(int(periods))]
    price = sum([coupon/(1+ytm/freq)**(freq*t) for t in dt]) + \
            fv/(1+ytm/freq)**(freq*T)
    return price

def get_treasury_yields():
    """Get historical 30Y Treasury yields"""
    try:
        url = f'https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=daily&maturity=30year&apikey=CFFZLL3MH1R3VKB7'
        r = requests.get(url)
        data = r.json()
        
        # Convert to DataFrame
        yields_df = pd.DataFrame(data['data'])
        yields_df['date'] = pd.to_datetime(yields_df['date'])
        # Clean the yield values
        yields_df['value'] = pd.to_numeric(yields_df['value'], errors='coerce') / 100
        yields_df = yields_df.dropna()  # Remove any invalid values
        yields_df.set_index('date', inplace=True)
        
        print("Treasury yields range:", yields_df.index[0], "to", yields_df.index[-1])
        print("Yield range:", yields_df['value'].min(), "to", yields_df['value'].max())
        return yields_df
        
    except Exception as e:
        print(f"Error getting Treasury yields: {e}")
        return None

def get_treasury_prices(hist_dates):
    """Calculate UST 1.25% 2050 prices using actual historical yields"""
    # Get historical yields
    yields_df = get_treasury_yields()
    if yields_df is None:
        print("Using constant yield as fallback")
        # Fallback to constant yield
        return np.full(len(hist_dates), price_bond(100, 26.5, 0.0445, 1.25))
        
    # Fixed parameters
    par = 100
    maturity = 26.5  # Years to maturity
    coupon = 1.25   # 1.25% coupon
    
    prices = []
    for date in pd.to_datetime(hist_dates):
        try:
            # Get yield for that date or nearest previous date
            daily_yield = yields_df.loc[yields_df.index <= date, 'value'].iloc[0]
            price = price_bond(par, maturity, daily_yield, coupon)
            prices.append(price)
        except (KeyError, IndexError) as e:
            print(f"Error calculating price for {date}: {e}")
            prices.append(None)
    
    return np.array(prices)

def main():
    # Get price data
    hist = get_tlt_data()
    if hist is None:
        return
        
    # Calculate metrics
    hist_vol = get_historical_volatility(hist['close'])
    ust_prices = get_treasury_prices(hist.index)
    
    # Create figure with two y-axes
    fig, ax1 = plt.subplots(figsize=(12, 8))
    ax2 = ax1.twinx()
    
    # Plot series
    ax1.plot(hist.index, hist['close'], 'b-', label='TLT Price ($)')
    ax1.plot(hist.index, hist_vol*100, 'r-', label='Volatility (%)')
    ax2.plot(hist.index, ust_prices, 'g-', label='UST 1.25% 2050 ($)')
    
    # Set labels
    ax1.set_ylabel('TLT Price ($) / Volatility (%)')
    ax2.set_ylabel('UST Price ($)')
    
    # Format x-axis dates
    plt.gcf().autofmt_xdate()
    ax1.xaxis.set_major_locator(mdates.MonthLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    
    # Combine legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    ax1.grid(True, alpha=0.2)
    plt.title('TLT, Volatility, and UST Price Comparison')
    
    plt.tight_layout()
    plt.savefig('tlt_analysis.png')
    plt.close()

if __name__ == "__main__":
    main() 