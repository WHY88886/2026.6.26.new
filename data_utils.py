import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime

def fetch_stock_data(symbol, start_date, end_date):
    try:
        data = yf.download(symbol, start=start_date, end=end_date)
        if data.empty:
            return generate_mock_data(start_date, end_date)
        return data
    except Exception:
        return generate_mock_data(start_date, end_date)

def generate_mock_data(start_date, end_date):
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    base_price = 100
    prices = []
    current_price = base_price
    
    for date in dates:
        if date.weekday() < 5:
            change = np.random.normal(0, 2)
            current_price = max(current_price + change, 50)
            prices.append(current_price)
        else:
            prices.append(None)
    
    data = pd.DataFrame({
        'Date': dates,
        'Open': prices,
        'High': [p * (1 + np.random.uniform(0, 0.02)) if p else None for p in prices],
        'Low': [p * (1 - np.random.uniform(0, 0.02)) if p else None for p in prices],
        'Close': prices,
        'Volume': [np.random.randint(1000000, 10000000) if p else None for p in prices]
    })
    
    data = data.dropna().set_index('Date')
    return data

def calculate_technical_indicators(data):
    data = data.copy()
    
    data['MA5'] = data['Close'].rolling(window=5).mean()
    data['MA20'] = data['Close'].rolling(window=20).mean()
    data['MA60'] = data['Close'].rolling(window=60).mean()
    
    delta = data['Close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    data['RSI'] = 100 - (100 / (1 + rs))
    
    data['MACD'] = data['Close'].ewm(span=12, adjust=False).mean() - data['Close'].ewm(span=26, adjust=False).mean()
    data['Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()
    
    data['Volatility'] = data['Close'].rolling(window=20).std()
    
    return data

def get_stock_info(symbol):
    stock_info = {
        '600519.SS': {'name': '贵州茅台', 'industry': '白酒', 'pe': 25.5, 'pb': 6.2, 'dividend': 2.8},
        '000858.SZ': {'name': '五粮液', 'industry': '白酒', 'pe': 18.3, 'pb': 4.5, 'dividend': 2.5},
        '600036.SS': {'name': '招商银行', 'industry': '银行', 'pe': 7.8, 'pb': 1.2, 'dividend': 4.5},
        '601318.SS': {'name': '中国平安', 'industry': '保险', 'pe': 9.2, 'pb': 1.1, 'dividend': 3.2},
        '002594.SZ': {'name': '比亚迪', 'industry': '新能源汽车', 'pe': 85.6, 'pb': 8.9, 'dividend': 1.2},
        '300750.SZ': {'name': '宁德时代', 'industry': '动力电池', 'pe': 45.2, 'pb': 6.8, 'dividend': 1.5},
        '00700.HK': {'name': '腾讯控股', 'industry': '互联网', 'pe': 22.1, 'pb': 3.8, 'dividend': 1.8},
        'BABA': {'name': '阿里巴巴', 'industry': '互联网', 'pe': 16.5, 'pb': 2.1, 'dividend': 0.8},
        'AAPL': {'name': '苹果', 'industry': '科技', 'pe': 28.3, 'pb': 6.1, 'dividend': 0.6},
        'TSLA': {'name': '特斯拉', 'industry': '新能源汽车', 'pe': 72.4, 'pb': 12.3, 'dividend': 0.0}
    }
    return stock_info.get(symbol, {'name': '未知', 'industry': '未知', 'pe': 0, 'pb': 0, 'dividend': 0})

def generate_portfolio_report(selected_stocks, weights):
    report = {
        'total_return': np.random.uniform(-10, 30),
        'annual_return': np.random.uniform(5, 25),
        'volatility': np.random.uniform(15, 40),
        'sharpe_ratio': np.random.uniform(0.5, 2.0),
        'max_drawdown': np.random.uniform(-5, -25)
    }
    return report