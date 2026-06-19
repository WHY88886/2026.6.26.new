import streamlit as st
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

st.set_page_config(
    page_title="普惠 AI 股息估值系统",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

STOCK_DB = {
    '600519': {'name': '贵州茅台', 'market': 'A股', 'industry': '白酒', 'base_price': 1650, 'dividend_yield': 0.025, 'beta': 0.85, 'pe': 25.5, 'pb': 6.2, 'roe': 32.5, 'roa': 25.8, 'debt_ratio': 0.18, 'revenue_growth': 18.2, 'net_profit_growth': 20.5, 'eps': 48.5},
    '000858': {'name': '五粮液', 'market': 'A股', 'industry': '白酒', 'base_price': 145, 'dividend_yield': 0.022, 'beta': 0.9, 'pe': 18.3, 'pb': 4.5, 'roe': 25.2, 'roa': 18.5, 'debt_ratio': 0.22, 'revenue_growth': 15.3, 'net_profit_growth': 16.8, 'eps': 6.8},
    '600809': {'name': '山西汾酒', 'market': 'A股', 'industry': '白酒', 'base_price': 280, 'dividend_yield': 0.018, 'beta': 0.88, 'pe': 28.5, 'pb': 8.2, 'roe': 35.2, 'roa': 22.5, 'debt_ratio': 0.28, 'revenue_growth': 28.5, 'net_profit_growth': 35.2, 'eps': 8.5},
    '600036': {'name': '招商银行', 'market': 'A股', 'industry': '银行', 'base_price': 36, 'dividend_yield': 0.045, 'beta': 1.1, 'pe': 7.8, 'pb': 1.2, 'roe': 16.5, 'roa': 1.2, 'debt_ratio': 0.92, 'revenue_growth': 8.5, 'net_profit_growth': 12.3, 'eps': 5.2},
    '601398': {'name': '工商银行', 'market': 'A股', 'industry': '银行', 'base_price': 5.8, 'dividend_yield': 0.052, 'beta': 0.95, 'pe': 5.8, 'pb': 0.7, 'roe': 12.5, 'roa': 1.1, 'debt_ratio': 0.91, 'revenue_growth': 3.2, 'net_profit_growth': 5.8, 'eps': 3.6},
    '002594': {'name': '比亚迪', 'market': 'A股', 'industry': '新能源', 'base_price': 265, 'dividend_yield': 0.005, 'beta': 1.5, 'pe': 85.6, 'pb': 8.9, 'roe': 28.5, 'roa': 8.2, 'debt_ratio': 0.72, 'revenue_growth': 72.3, 'net_profit_growth': 128.5, 'eps': 5.2},
    '300750': {'name': '宁德时代', 'market': 'A股', 'industry': '新能源', 'base_price': 195, 'dividend_yield': 0.012, 'beta': 1.6, 'pe': 45.2, 'pb': 6.8, 'roe': 22.5, 'roa': 10.5, 'debt_ratio': 0.65, 'revenue_growth': 48.5, 'net_profit_growth': 82.1, 'eps': 8.5},
    '601318': {'name': '中国平安', 'market': 'A股', 'industry': '保险', 'base_price': 48, 'dividend_yield': 0.035, 'beta': 1.2, 'pe': 9.2, 'pb': 1.1, 'roe': 15.8, 'roa': 2.1, 'debt_ratio': 0.89, 'revenue_growth': 6.2, 'net_profit_growth': 15.8, 'eps': 4.8},
    '600900': {'name': '长江电力', 'market': 'A股', 'industry': '电力', 'base_price': 28, 'dividend_yield': 0.048, 'beta': 0.5, 'pe': 12.5, 'pb': 2.1, 'roe': 16.8, 'roa': 8.5, 'debt_ratio': 0.58, 'revenue_growth': 12.5, 'net_profit_growth': 8.2, 'eps': 1.2},
    '600585': {'name': '海螺水泥', 'market': 'A股', 'industry': '建材', 'base_price': 28, 'dividend_yield': 0.038, 'beta': 1.1, 'pe': 8.5, 'pb': 1.0, 'roe': 12.8, 'roa': 8.5, 'debt_ratio': 0.18, 'revenue_growth': -15.2, 'net_profit_growth': -25.5, 'eps': 2.8},
    '601888': {'name': '中国中免', 'market': 'A股', 'industry': '零售', 'base_price': 72, 'dividend_yield': 0.025, 'beta': 1.3, 'pe': 32.5, 'pb': 5.2, 'roe': 25.8, 'roa': 15.2, 'debt_ratio': 0.45, 'revenue_growth': 25.8, 'net_profit_growth': 35.5, 'eps': 3.5},
    'AAPL': {'name': '苹果', 'market': '美股', 'industry': '科技', 'base_price': 185, 'dividend_yield': 0.006, 'beta': 1.2, 'pe': 28.3, 'pb': 6.1, 'roe': 185, 'roa': 28.5, 'debt_ratio': 0.52, 'revenue_growth': 2.5, 'net_profit_growth': 5.8, 'eps': 6.1},
    'MSFT': {'name': '微软', 'market': '美股', 'industry': '科技', 'base_price': 375, 'dividend_yield': 0.008, 'beta': 0.95, 'pe': 32.5, 'pb': 12.5, 'roe': 38.5, 'roa': 22.5, 'debt_ratio': 0.42, 'revenue_growth': 12.5, 'net_profit_growth': 18.5, 'eps': 11.5},
    'GOOGL': {'name': '谷歌', 'market': '美股', 'industry': '科技', 'base_price': 140, 'dividend_yield': 0.0, 'beta': 1.05, 'pe': 25.2, 'pb': 5.8, 'roe': 28.5, 'roa': 18.2, 'debt_ratio': 0.28, 'revenue_growth': 15.5, 'net_profit_growth': 22.5, 'eps': 5.5},
    'AMZN': {'name': '亚马逊', 'market': '美股', 'industry': '科技', 'base_price': 178, 'dividend_yield': 0.0, 'beta': 1.15, 'pe': 62.5, 'pb': 8.5, 'roe': 32.5, 'roa': 12.5, 'debt_ratio': 0.45, 'revenue_growth': 12.8, 'net_profit_growth': 85.5, 'eps': 2.8},
    'NVDA': {'name': '英伟达', 'market': '美股', 'industry': '科技', 'base_price': 480, 'dividend_yield': 0.0004, 'beta': 1.75, 'pe': 65.2, 'pb': 35.5, 'roe': 58.5, 'roa': 32.5, 'debt_ratio': 0.35, 'revenue_growth': 125.5, 'net_profit_growth': 185.5, 'eps': 7.5},
    'META': {'name': 'Meta', 'market': '美股', 'industry': '科技', 'base_price': 505, 'dividend_yield': 0.005, 'beta': 1.25, 'pe': 28.5, 'pb': 8.2, 'roe': 28.5, 'roa': 18.5, 'debt_ratio': 0.18, 'revenue_growth': 25.5, 'net_profit_growth': 75.5, 'eps': 17.5},
    'BABA': {'name': '阿里巴巴', 'market': '美股', 'industry': '互联网', 'base_price': 88, 'dividend_yield': 0.015, 'beta': 1.4, 'pe': 16.5, 'pb': 2.1, 'roe': 12.5, 'roa': 8.5, 'debt_ratio': 0.32, 'revenue_growth': 8.3, 'net_profit_growth': 25.6, 'eps': 5.8},
    'JD': {'name': '京东', 'market': '美股', 'industry': '互联网', 'base_price': 28, 'dividend_yield': 0.025, 'beta': 1.35, 'pe': 12.5, 'pb': 2.5, 'roe': 18.5, 'roa': 5.5, 'debt_ratio': 0.52, 'revenue_growth': 5.5, 'net_profit_growth': 125.5, 'eps': 2.2},
    'PDD': {'name': '拼多多', 'market': '美股', 'industry': '互联网', 'base_price': 105, 'dividend_yield': 0.0, 'beta': 1.45, 'pe': 22.5, 'pb': 6.5, 'roe': 35.5, 'roa': 22.5, 'debt_ratio': 0.25, 'revenue_growth': 85.5, 'net_profit_growth': 125.5, 'eps': 4.5},
    'TSLA': {'name': '特斯拉', 'market': '美股', 'industry': '新能源', 'base_price': 175, 'dividend_yield': 0.0, 'beta': 2.0, 'pe': 72.4, 'pb': 12.3, 'roe': 25.5, 'roa': 12.5, 'debt_ratio': 0.35, 'revenue_growth': 37.6, 'net_profit_growth': 105.3, 'eps': 3.8},
    'JNJ': {'name': '强生', 'market': '美股', 'industry': '医药', 'base_price': 155, 'dividend_yield': 0.032, 'beta': 0.65, 'pe': 15.2, 'pb': 5.5, 'roe': 52.5, 'roa': 15.5, 'debt_ratio': 0.45, 'revenue_growth': 5.8, 'net_profit_growth': 8.5, 'eps': 10.2},
    'PFE': {'name': '辉瑞', 'market': '美股', 'industry': '医药', 'base_price': 28, 'dividend_yield': 0.045, 'beta': 0.75, 'pe': 12.5, 'pb': 2.5, 'roe': 28.5, 'roa': 12.5, 'debt_ratio': 0.38, 'revenue_growth': -25.5, 'net_profit_growth': -85.5, 'eps': 2.2},
    'UNH': {'name': '联合健康', 'market': '美股', 'industry': '医药', 'base_price': 525, 'dividend_yield': 0.015, 'beta': 0.85, 'pe': 22.5, 'pb': 6.5, 'roe': 28.5, 'roa': 8.5, 'debt_ratio': 0.62, 'revenue_growth': 12.5, 'net_profit_growth': 15.5, 'eps': 23.5},
    'JPM': {'name': '摩根大通', 'market': '美股', 'industry': '银行', 'base_price': 195, 'dividend_yield': 0.025, 'beta': 1.2, 'pe': 11.5, 'pb': 1.6, 'roe': 18.5, 'roa': 1.5, 'debt_ratio': 0.88, 'revenue_growth': 12.5, 'net_profit_growth': 18.5, 'eps': 16.5},
    'KO': {'name': '可口可乐', 'market': '美股', 'industry': '消费', 'base_price': 62, 'dividend_yield': 0.030, 'beta': 0.6, 'pe': 22.5, 'pb': 8.2, 'roe': 42.5, 'roa': 12.5, 'debt_ratio': 0.72, 'revenue_growth': 3.2, 'net_profit_growth': 5.5, 'eps': 2.6},
    'PG': {'name': '宝洁', 'market': '美股', 'industry': '消费', 'base_price': 162, 'dividend_yield': 0.025, 'beta': 0.55, 'pe': 25.5, 'pb': 7.5, 'roe': 32.5, 'roa': 15.5, 'debt_ratio': 0.65, 'revenue_growth': 4.2, 'net_profit_growth': 5.8, 'eps': 6.2},
    'PEP': {'name': '百事可乐', 'market': '美股', 'industry': '消费', 'base_price': 175, 'dividend_yield': 0.028, 'beta': 0.58, 'pe': 26.5, 'pb': 9.2, 'roe': 45.5, 'roa': 12.5, 'debt_ratio': 0.68, 'revenue_growth': 5.2, 'net_profit_growth': 8.5, 'eps': 6.5},
    'NKE': {'name': '耐克', 'market': '美股', 'industry': '消费', 'base_price': 92, 'dividend_yield': 0.018, 'beta': 0.85, 'pe': 28.5, 'pb': 10.5, 'roe': 38.5, 'roa': 15.5, 'debt_ratio': 0.42, 'revenue_growth': 8.5, 'net_profit_growth': 2.5, 'eps': 3.2},
    '00700': {'name': '腾讯控股', 'market': '港股', 'industry': '互联网', 'base_price': 355, 'dividend_yield': 0.02, 'beta': 1.3, 'pe': 22.1, 'pb': 3.8, 'roe': 28.5, 'roa': 18.5, 'debt_ratio': 0.35, 'revenue_growth': 10.5, 'net_profit_growth': 18.2, 'eps': 12.5},
}

def get_stock_info(symbol):
    symbol = symbol.strip().upper()
    
    for code, info in STOCK_DB.items():
        if symbol == code.upper():
            return {**info, 'symbol': code}
    
    for code, info in STOCK_DB.items():
        if code.upper() in symbol or symbol in code.upper():
            return {**info, 'symbol': code}
    
    for code, info in STOCK_DB.items():
        if info['name'] in symbol or symbol in info['name']:
            return {**info, 'symbol': code}
    
    if symbol.isdigit():
        normalized = symbol.zfill(6)
        for code, info in STOCK_DB.items():
            if code == normalized:
                return {**info, 'symbol': code}
    
    return {'name': '未知股票', 'market': 'A股', 'industry': '综合', 'base_price': 100, 'dividend_yield': 0.02, 'beta': 1.0, 'pe': 15.0, 'pb': 2.0, 'roe': 15.0, 'roa': 8.0, 'debt_ratio': 0.5, 'revenue_growth': 10.0, 'net_profit_growth': 12.0, 'eps': 5.0, 'symbol': symbol}

def generate_simulation_data(symbol):
    stock_info = get_stock_info(symbol)
    base_price = stock_info.get('base_price', 100)
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365*3)
    
    dates, closes, highs, lows, opens, volumes = [], [], [], [], [], []
    
    current_price = base_price
    volatility = stock_info.get('beta', 1.0) * 0.015
    
    while start_date <= end_date:
        if start_date.weekday() < 5:
            dates.append(start_date)
            
            shock = random.gauss(0, volatility)
            current_price = max(current_price * (1 + shock), base_price * 0.3)
            high = current_price * (1 + abs(random.gauss(0, 0.008)))
            low = current_price * (1 - abs(random.gauss(0, 0.008)))
            open_price = closes[-1] * (1 + random.uniform(-0.005, 0.005)) if closes else current_price
            
            closes.append(current_price)
            
            highs.append(high)
            lows.append(low)
            opens.append(open_price)
            volumes.append(int(random.uniform(5000000, 50000000)))
        
        start_date += timedelta(days=1)
    
    return {'dates': dates, 'closes': closes, 'highs': highs, 'lows': lows, 'opens': opens, 'volumes': volumes, 'stock_info': stock_info}

def calculate_technical_indicators(data):
    closes = np.array(data['closes'])
    highs = np.array(data['highs'])
    lows = np.array(data['lows'])
    
    n = len(closes)
    ma5 = np.zeros(n)
    ma10 = np.zeros(n)
    ma20 = np.zeros(n)
    ma60 = np.zeros(n)
    
    for i in range(n):
        ma5[i] = np.mean(closes[max(0, i-4):i+1])
        ma10[i] = np.mean(closes[max(0, i-9):i+1])
        ma20[i] = np.mean(closes[max(0, i-19):i+1])
        ma60[i] = np.mean(closes[max(0, i-59):i+1])
    
    delta = np.diff(closes, prepend=closes[0])
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    
    avg_gain = np.zeros(n)
    avg_loss = np.zeros(n)
    for i in range(n):
        avg_gain[i] = np.mean(gain[max(0, i-13):i+1])
        avg_loss[i] = np.mean(loss[max(0, i-13):i+1])
    rs = avg_gain / (avg_loss + 1e-10)
    rsi = 100 - (100 / (1 + rs))
    
    ema12 = np.zeros(n)
    ema26 = np.zeros(n)
    alpha12 = 2 / 13
    alpha26 = 2 / 27
    ema12[0] = closes[0]
    ema26[0] = closes[0]
    for i in range(1, n):
        ema12[i] = alpha12 * closes[i] + (1 - alpha12) * ema12[i-1]
        ema26[i] = alpha26 * closes[i] + (1 - alpha26) * ema26[i-1]
    
    macd = ema12 - ema26
    signal = np.zeros(n)
    alpha9 = 2 / 10
    signal[0] = macd[0]
    for i in range(1, n):
        signal[i] = alpha9 * macd[i] + (1 - alpha9) * signal[i-1]
    macd_hist = macd - signal
    
    high14 = np.array([max(highs[max(0,i-13):i+1]) for i in range(n)])
    low14 = np.array([min(lows[max(0,i-13):i+1]) for i in range(n)])
    k = 100 * (closes - low14) / (high14 - low14 + 1e-10)
    d = np.zeros(n)
    for i in range(n):
        d[i] = np.mean(k[max(0, i-2):i+1])
    
    sma20 = ma20
    std20 = np.zeros(n)
    for i in range(n):
        std20[i] = np.std(closes[max(0, i-19):i+1])
    upper_band = sma20 + 2 * std20
    lower_band = sma20 - 2 * std20
    
    returns = np.diff(closes) / closes[:-1] if len(closes) > 1 else np.array([0])
    volatility = np.std(returns) * np.sqrt(252) if len(returns) > 0 else 0
    cumulative_return = np.cumprod(1 + returns) - 1 if len(returns) > 0 else np.array([0])
    max_drawdown = np.min(cumulative_return - np.maximum.accumulate(cumulative_return)) if len(cumulative_return) > 0 else 0
    sharpe_ratio = np.mean(returns) / (np.std(returns) + 1e-10) * np.sqrt(252) if np.std(returns) > 0 else 0
    
    return {
        'ma5': ma5.tolist(), 'ma10': ma10.tolist(), 'ma20': ma20.tolist(), 'ma60': ma60.tolist(),
        'rsi': rsi.tolist(), 'macd': macd.tolist(), 'macd_signal': signal.tolist(), 'macd_hist': macd_hist.tolist(),
        'k': k.tolist(), 'd': d.tolist(),
        'bollinger_upper': upper_band.tolist(), 'bollinger_lower': lower_band.tolist(), 'bollinger_mid': sma20.tolist(),
        'volatility': float(volatility), 'max_drawdown': float(max_drawdown) * 100, 'sharpe_ratio': float(sharpe_ratio),
        'prices': closes.tolist(), 'dates': data['dates'],
        'current_price': float(closes[-1]) if len(closes) > 0 else 0
    }

def calculate_valuation(data):
    stock_info = data['stock_info']
    closes = data['closes']
    current_price = closes[-1] if closes else stock_info.get('base_price', 100)
    
    rf = 0.025
    beta = stock_info.get('beta', 1.0)
    discount_rate = rf + beta * 0.08 + 0.01
    
    avg_growth = stock_info.get('net_profit_growth', 10) / 100
    
    last_dividend = current_price * stock_info.get('dividend_yield', 0.02)
    
    model_results = {}
    model_results['零增长DDM'] = last_dividend / discount_rate if discount_rate > 0 else current_price
    model_results['戈登增长模型'] = last_dividend * (1 + avg_growth) / (discount_rate - avg_growth) if discount_rate > avg_growth else current_price
    
    two_stage_val = 0
    for t in range(1, 6):
        two_stage_val += last_dividend * (1 + min(avg_growth, 0.15)) ** t / (1 + discount_rate) ** t
    if discount_rate > min(avg_growth, 0.15):
        two_stage_val += last_dividend * (1 + min(avg_growth, 0.15)) ** 5 / ((discount_rate - min(avg_growth, 0.15)) * (1 + discount_rate) ** 5)
    model_results['两阶段DDM'] = two_stage_val
    
    pe_value = stock_info.get('eps', 5) * stock_info.get('pe', 15)
    model_results['PE估值法'] = pe_value
    
    book_value = current_price / stock_info.get('pb', 2.0) if stock_info.get('pb', 2.0) > 0 else current_price
    model_results['PB估值法'] = book_value
    
    eps = stock_info.get('eps', current_price * 0.06)
    bvps = current_price / stock_info.get('pb', 2.0) if stock_info.get('pb', 2.0) > 0 else current_price * 0.5
    model_results['Graham公式'] = np.sqrt(22.5 * eps * bvps) if eps > 0 and bvps > 0 else current_price
    
    growth = stock_info.get('net_profit_growth', 10)
    model_results['PEG估值'] = pe_value / growth if growth > 0 else pe_value
    
    valid_models = [v for v in model_results.values() if 0 < v < current_price * 10]
    fair_value = np.median(valid_models) if valid_models else current_price
    
    diff = (fair_value - current_price) / current_price
    
    if diff < -0.15:
        conclusion, color = '高估', '#ef4444'
    elif diff > 0.15:
        conclusion, color = '低估', '#22c55e'
    else:
        conclusion, color = '合理', '#f59e0b'
    
    return {
        'current_price': round(current_price, 2),
        'fair_value': round(fair_value, 2),
        'discount_rate': round(discount_rate, 4),
        'model_results': model_results,
        'conclusion': conclusion,
        'conclusion_color': color,
        'valuation_diff': round(diff * 100, 1),
        'dividend_growth': round(avg_growth * 100, 1),
        'stock_info': stock_info,
        'price_history': closes,
        'dates': data['dates']
    }

def render_header():
    st.markdown("""
    <style>
        .header-container { background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%); padding: 25px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .main-title { color: white; font-size: 28px; font-weight: bold; margin: 0; text-align: center; }
        .sub-title { color: rgba(255,255,255,0.85); font-size: 14px; text-align: center; margin-top: 8px; }
        .card { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 20px; }
        .metric-card { background: #f8fafc; border-radius: 10px; padding: 15px; margin: 8px 0; border-left: 3px solid #3b82f6; }
        .info-box { background: #f1f5f9; border-radius: 8px; padding: 15px; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

def generate_trend_analysis(period, change_pct):
    trend = '上涨' if change_pct > 5 else ('下跌' if change_pct < -5 else '震荡')
    
    if period == '近7日':
        if change_pct > 10:
            return f'近7日股票{trend}明显，涨幅达{change_pct:.1f}%，短期涨幅较大，注意回调风险。'
        elif change_pct < -10:
            return f'近7日股票{trend}明显，跌幅达{abs(change_pct):.1f}%，短期超跌，关注反弹机会。'
        else:
            return f'近7日股票{trend}整理，波动幅度{abs(change_pct):.1f}%，处于区间震荡状态。'
    
    elif period == '近1个月':
        if change_pct > 15:
            return f'近1个月股票强势{trend}，累计涨幅{change_pct:.1f}%，多头趋势明显。'
        elif change_pct < -15:
            return f'近1个月股票持续{trend}，累计跌幅{abs(change_pct):.1f}%，空头压力较大。'
        else:
            return f'近1个月股票{trend}整理，整体波动{abs(change_pct):.1f}%，方向不明。'
    
    elif period == '近6个月':
        if change_pct > 30:
            return f'近6个月股票趋势性{trend}，涨幅{change_pct:.1f}%，中长期看好。'
        elif change_pct < -30:
            return f'近6个月股票深度{trend}，跌幅{abs(change_pct):.1f}%，需关注基本面变化。'
        else:
            return f'近6个月股票{trend}盘整，波动{abs(change_pct):.1f}%，等待方向选择。'
    
    else:
        if change_pct > 50:
            return f'近1年股票大幅{trend}，累计涨幅{change_pct:.1f}%，表现优异。'
        elif change_pct < -50:
            return f'近1年股票大幅{trend}，累计跌幅{abs(change_pct):.1f}%，需谨慎评估。'
        else:
            return f'近1年股票{trend}运行，整体涨跌幅{abs(change_pct):.1f}%，表现平稳。'

def render_tab1():
    render_header()
    
    if 'search_symbol' not in st.session_state:
        st.session_state.search_symbol = '600519'
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("""<div class="card"><h3 style="color: #1e3a5f; margin-bottom: 15px;">股票查询</h3></div>""", unsafe_allow_html=True)
        
        user_input = st.text_input(
            "",
            value=st.session_state.search_symbol,
            placeholder="输入代码或名称（如 600519、茅台、AAPL）",
            key="symbol_input",
            label_visibility="collapsed"
        )
        
        if user_input.strip():
            st.session_state.search_symbol = user_input.strip()
    
    symbol = st.session_state.search_symbol
    if not symbol:
        symbol = '600519'
    
    try:
        stock_info = get_stock_info(symbol)
        data = generate_simulation_data(stock_info['symbol'])
        tech = calculate_technical_indicators(data)
        val_result = calculate_valuation(data)
        
        with col2:
            st.markdown(f"""
            <div style="background: #f8fafc; border-radius: 12px; padding: 15px;">
                <p style="color: #64748b; font-size: 12px; margin: 0;">当前查询</p>
                <p style="color: #1e3a5f; font-size: 16px; font-weight: bold; margin: 5px 0;">{stock_info['name']}</p>
                <p style="color: #94a3b8; font-size: 12px; margin: 0;">{stock_info['market']} · {stock_info['industry']}</p>
                <p style="color: #3b82f6; font-size: 20px; font-weight: bold; margin: 10px 0;">{tech['current_price']:.2f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""<div class="card"><h3 style="color: #1e3a5f; margin-bottom: 0;">股票基本信息</h3></div>""", unsafe_allow_html=True)
        
        col_info1, col_info2, col_info3, col_info4, col_info5, col_info6 = st.columns(6)
        info_items = [
            ('市盈率 PE', f"{stock_info.get('pe', 0):.1f}", '#3b82f6'),
            ('市净率 PB', f"{stock_info.get('pb', 0):.1f}", '#8b5cf6'),
            ('ROE', f"{stock_info.get('roe', 0):.1f}%", '#22c55e'),
            ('ROA', f"{stock_info.get('roa', 0):.1f}%", '#f59e0b'),
            ('股息率', f"{stock_info.get('dividend_yield', 0)*100:.2f}%", '#10b981'),
            ('Beta', f"{stock_info.get('beta', 0):.2f}", '#6366f1')
        ]
        
        for i, (label, value, color) in enumerate(info_items):
            with [col_info1, col_info2, col_info3, col_info4, col_info5, col_info6][i]:
                st.markdown(f"""
                <div style="background: #f8fafc; border-radius: 10px; padding: 15px; border-left: 4px solid {color};">
                    <p style="color: #64748b; font-size: 12px; margin: 0;">{label}</p>
                    <p style="color: {color}; font-size: 24px; font-weight: bold; margin: 5px 0;">{value}</p>
                </div>
                """, unsafe_allow_html=True)
        
        col_info7, col_info8 = st.columns(2)
        with col_info7:
            growth_color = '#22c55e' if stock_info.get('revenue_growth', 0) > 0 else '#ef4444'
            st.markdown(f"""
            <div style="background: #f8fafc; border-radius: 10px; padding: 15px; border-left: 4px solid {growth_color};">
                <p style="color: #64748b; font-size: 12px; margin: 0;">营收增长率</p>
                <p style="color: {growth_color}; font-size: 24px; font-weight: bold; margin: 5px 0;">{stock_info.get('revenue_growth', 0):.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
        with col_info8:
            profit_color = '#22c55e' if stock_info.get('net_profit_growth', 0) > 0 else '#ef4444'
            st.markdown(f"""
            <div style="background: #f8fafc; border-radius: 10px; padding: 15px; border-left: 4px solid {profit_color};">
                <p style="color: #64748b; font-size: 12px; margin: 0;">净利润增长率</p>
                <p style="color: {profit_color}; font-size: 24px; font-weight: bold; margin: 5px 0;">{stock_info.get('net_profit_growth', 0):.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""<div class="card"><h3 style="color: #1e3a5f; margin-bottom: 15px;">基本面综合分析</h3></div>""", unsafe_allow_html=True)
        
        pe = stock_info.get('pe', 0)
        pb = stock_info.get('pb', 0)
        roe = stock_info.get('roe', 0)
        debt = stock_info.get('debt_ratio', 0.5)
        profit_growth = stock_info.get('net_profit_growth', 0)
        revenue_growth = stock_info.get('revenue_growth', 0)
        dividend = stock_info.get('dividend_yield', 0) * 100
        
        if pe < 15:
            pe_comment = '估值偏低，具备安全边际'
        elif pe < 30:
            pe_comment = '估值处于合理区间'
        else:
            pe_comment = '估值偏高，需关注成长性支撑'
        
        if pb < 2:
            pb_comment = '市净率较低，资产价值被低估的可能性较大'
        elif pb < 5:
            pb_comment = '市净率处于合理水平'
        else:
            pb_comment = '市净率偏高，市场给予较高溢价'
        
        if roe > 20:
            roe_comment = 'ROE优秀，资本回报能力强劲'
        elif roe > 10:
            roe_comment = 'ROE良好，具备稳定的盈利能力'
        else:
            roe_comment = 'ROE偏低，资本使用效率有待提升'
        
        if debt > 0.7:
            debt_comment = '负债率偏高，需关注财务风险'
        elif debt > 0.4:
            debt_comment = '负债率适中，财务结构相对稳健'
        else:
            debt_comment = '负债率较低，财务风险可控'
        
        if profit_growth > 20 and revenue_growth > 15:
            growth_comment = '营收和利润双增长，成长性优异'
        elif profit_growth > 0 and revenue_growth > 0:
            growth_comment = '营收利润正向增长，经营态势良好'
        elif profit_growth < 0 and revenue_growth < 0:
            growth_comment = '营收利润双降，经营面临较大压力'
        else:
            growth_comment = '业绩增长出现分化，需关注具体业务变化'
        
        if dividend > 3:
            dividend_comment = '股息率较高，适合价值投资者获取稳定现金流'
        elif dividend > 1:
            dividend_comment = '股息率适中，兼顾成长与分红'
        else:
            dividend_comment = '股息率偏低，公司更倾向将利润用于再投资'
        
        st.markdown(f"""
        <div style="background: #f8fafc; border-radius: 12px; padding: 20px;">
            <p style="color: #1e3a5f; font-size: 14px; line-height: 1.8; margin: 0;">
                <strong>1. 估值水平：</strong>{stock_info['name']}当前市盈率(PE)为{pe:.1f}倍，{pe_comment}；
                市净率(PB)为{pb:.1f}倍，{pb_comment}。<br><br>
                <strong>2. 盈利能力：</strong>净资产收益率(ROE)为{roe:.1f}%，{roe_comment}。
                公司整体盈利能力{"较强" if roe > 15 else "一般" if roe > 8 else "偏弱"}，
                能够为股东创造{"可观" if roe > 15 else "一定" if roe > 8 else "有限"}的价值回报。<br><br>
                <strong>3. 成长性：</strong>{growth_comment}。
                营收增长率为{revenue_growth:.1f}%，净利润增长率为{profit_growth:.1f}%，
                {"显示出强劲的增长动力" if profit_growth > 20 else "保持稳健增长" if profit_growth > 0 else "增长面临挑战"}。<br><br>
                <strong>4. 财务安全：</strong>资产负债率约为{debt*100:.0f}%，{debt_comment}。
                公司整体财务{"较为健康" if debt < 0.6 else "需要关注"}，偿债压力{"较小" if debt < 0.5 else "适中" if debt < 0.7 else "较大"}。<br><br>
                <strong>5. 分红能力：</strong>股息率约为{dividend:.2f}%，{dividend_comment}。
                {"适合长期持有获取分红收益" if dividend > 3 else "可作为辅助收益来源" if dividend > 1 else "更依赖股价上涨获取收益"}。
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""<div class="card"><h3 style="color: #1e3a5f; margin-bottom: 15px;">价格走势分析</h3></div>""", unsafe_allow_html=True)
        
        periods = {'近7日': 7, '近1个月': 30, '近6个月': 180, '近1年': 365}
        tabs = st.tabs(list(periods.keys()))
        
        for tab, (period_name, days) in zip(tabs, periods.items()):
            with tab:
                start_idx = max(0, len(tech['dates']) - days)
                plot_dates = tech['dates'][start_idx:]
                plot_prices = tech['prices'][start_idx:]
                
                if len(plot_prices) >= 2:
                    change_pct = (plot_prices[-1] - plot_prices[0]) / plot_prices[0] * 100
                    change_color = '#22c55e' if change_pct >= 0 else '#ef4444'
                    
                    col_stat1, col_stat2, col_stat3 = st.columns(3)
                    with col_stat1:
                        st.markdown(f"""
                        <div style="background: #f8fafc; border-radius: 10px; padding: 15px; text-align: center;">
                            <p style="color: #64748b; font-size: 12px; margin: 0;">期初价格</p>
                            <p style="color: #1e3a5f; font-size: 20px; font-weight: bold; margin: 5px 0;">{plot_prices[0]:.2f}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    with col_stat2:
                        st.markdown(f"""
                        <div style="background: #f8fafc; border-radius: 10px; padding: 15px; text-align: center;">
                            <p style="color: #64748b; font-size: 12px; margin: 0;">期末价格</p>
                            <p style="color: #1e3a5f; font-size: 20px; font-weight: bold; margin: 5px 0;">{plot_prices[-1]:.2f}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    with col_stat3:
                        st.markdown(f"""
                        <div style="background: #f8fafc; border-radius: 10px; padding: 15px; text-align: center;">
                            <p style="color: #64748b; font-size: 12px; margin: 0;">涨跌幅</p>
                            <p style="color: {change_color}; font-size: 20px; font-weight: bold; margin: 5px 0;">{change_pct:+.2f}%</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=plot_dates, y=plot_prices,
                        name='收盘价',
                        line=dict(color='#3b82f6', width=2),
                        fill='tozeroy', fillcolor='rgba(59,130,246,0.1)',
                        hovertemplate='日期: %{x}<br>价格: %{y:.2f}<extra></extra>'
                    ))
                    
                    ma20_idx = max(0, len(tech['ma20']) - days)
                    if len(tech['ma20'][ma20_idx:]) > 0:
                        fig.add_trace(go.Scatter(
                            x=plot_dates, y=tech['ma20'][ma20_idx:],
                            name='MA20',
                            line=dict(color='#f59e0b', width=1.5, dash='dash'),
                            hovertemplate='MA20: %{y:.2f}<extra></extra>'
                        ))
                    
                    fig.update_layout(height=350, template='plotly_white', xaxis_rangeslider_visible=True, hovermode='x unified', title=f'{period_name}价格走势图')
                    st.plotly_chart(fig, use_container_width=True)
                    
                    analysis_text = generate_trend_analysis(period_name, change_pct)
                    st.markdown(f"""<div style="background: #f1f5f9; border-radius: 8px; padding: 15px;"><p style="color: #1e3a5f; font-size: 14px; margin: 0;">{analysis_text}</p></div>""", unsafe_allow_html=True)
                    
                    ma20_period = tech['ma20'][start_idx:]
                    ma60_period = tech['ma60'][start_idx:] if len(tech['ma60']) >= start_idx else []
                    
                    ma_analysis = ''
                    if len(ma20_period) >= 2:
                        price_vs_ma20 = (plot_prices[-1] - ma20_period[-1]) / ma20_period[-1] * 100 if ma20_period[-1] != 0 else 0
                        if price_vs_ma20 > 3:
                            ma_trend = '股价站上20日均线且偏离度较大，短期强势特征明显'
                        elif price_vs_ma20 > 0:
                            ma_trend = '股价在20日均线上方运行，短期趋势偏多'
                        elif price_vs_ma20 > -3:
                            ma_trend = '股价在20日均线下方运行，短期趋势偏弱'
                        else:
                            ma_trend = '股价大幅偏离20日均线，短期超卖特征明显'
                        
                        if len(ma60_period) >= 2 and ma60_period[-1] != 0:
                            price_vs_ma60 = (plot_prices[-1] - ma60_period[-1]) / ma60_period[-1] * 100
                            if price_vs_ma60 > 5:
                                long_trend = '中长期趋势向好，60日均线提供较强支撑'
                            elif price_vs_ma60 > -5:
                                long_trend = '中长期趋势中性，股价在60日均线附近震荡'
                            else:
                                long_trend = '中长期趋势偏弱，60日均线构成压力'
                        else:
                            long_trend = '数据不足，无法判断中长期趋势'
                        
                        ma_analysis = f"""
                        <strong>均线系统分析：</strong>{ma_trend}。{long_trend}。
                        当前价格与20日均线偏离度为{price_vs_ma20:+.2f}%，
                        {"短期可能面临回调压力" if price_vs_ma20 > 5 else "短期有反弹空间" if price_vs_ma20 < -5 else "短期走势相对均衡"}。
                        """
                    
                    max_price = max(plot_prices) if plot_prices else 0
                    min_price = min(plot_prices) if plot_prices else 0
                    amplitude = ((max_price - min_price) / min_price * 100) if min_price > 0 else 0
                    
                    st.markdown(f"""
                    <div style="background: #e0f2fe; border-radius: 8px; padding: 15px; margin-top: 10px;">
                        <p style="color: #1e3a5f; font-size: 13px; line-height: 1.8; margin: 0;">
                            <strong>走势详细解读：</strong>该周期内股价最高达到{max_price:.2f}，最低下探至{min_price:.2f}，
                            振幅为{amplitude:.2f}%。{"波动较为剧烈，适合短线操作" if amplitude > 15 else "波动相对温和，趋势较为平稳"}。
                            {"股价整体呈现上升趋势，高点和低点不断抬升" if change_pct > 5 else "股价整体呈现下跌趋势，高点和低点逐步下移" if change_pct < -5 else "股价在区间内震荡整理，尚未形成明确方向"}。
                            {ma_analysis}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"分析出错: {str(e)}")

def render_tab2():
    st.markdown("""<div class="card"><h3 style="color: #1e3a5f; margin-bottom: 15px;">技术指标分析</h3></div>""", unsafe_allow_html=True)
    
    symbol = st.session_state.get('search_symbol', '600519')
    stock_info = get_stock_info(symbol)
    data = generate_simulation_data(stock_info['symbol'])
    tech = calculate_technical_indicators(data)
    
    col_overview1, col_overview2, col_overview3 = st.columns(3)
    
    vol_color = '#ef4444' if tech['volatility'] > 0.4 else ('#f59e0b' if tech['volatility'] > 0.25 else '#22c55e')
    with col_overview1:
        st.markdown(f"""
        <div style="background: #f8fafc; border-radius: 12px; padding: 20px; text-align: center;">
            <p style="color: #64748b; font-size: 13px; margin: 0;">年化波动率</p>
            <p style="color: {vol_color}; font-size: 32px; font-weight: bold; margin: 10px 0;">{tech['volatility']*100:.1f}%</p>
            <p style="color: #94a3b8; font-size: 11px; margin: 0;">风险水平指标</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_overview2:
        st.markdown(f"""
        <div style="background: #f8fafc; border-radius: 12px; padding: 20px; text-align: center;">
            <p style="color: #64748b; font-size: 13px; margin: 0;">最大回撤</p>
            <p style="color: #ef4444; font-size: 32px; font-weight: bold; margin: 10px 0;">{tech['max_drawdown']:.1f}%</p>
            <p style="color: #94a3b8; font-size: 11px; margin: 0;">历史最大亏损</p>
        </div>
        """, unsafe_allow_html=True)
    
    sharpe_color = '#22c55e' if tech['sharpe_ratio'] > 1 else ('#f59e0b' if tech['sharpe_ratio'] > 0 else '#ef4444')
    with col_overview3:
        st.markdown(f"""
        <div style="background: #f8fafc; border-radius: 12px; padding: 20px; text-align: center;">
            <p style="color: #64748b; font-size: 13px; margin: 0;">夏普比率</p>
            <p style="color: {sharpe_color}; font-size: 32px; font-weight: bold; margin: 10px 0;">{tech['sharpe_ratio']:.2f}</p>
            <p style="color: #94a3b8; font-size: 11px; margin: 0;">风险调整收益</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""<div class="card"><h4 style="color: #1e3a5f; margin-bottom: 15px;">K线图与均线</h4></div>""", unsafe_allow_html=True)
    
    recent_dates = tech['dates'][-120:]
    recent_closes = tech['prices'][-120:]
    recent_highs = np.array(data['highs'])[-120:].tolist()
    recent_lows = np.array(data['lows'])[-120:].tolist()
    recent_opens = np.array(data['opens'])[-120:].tolist()
    
    fig_candlestick = go.Figure(data=[go.Candlestick(
        x=recent_dates,
        open=recent_opens,
        high=recent_highs,
        low=recent_lows,
        close=recent_closes
    )])
    
    fig_candlestick.add_trace(go.Scatter(x=recent_dates, y=tech['ma5'][-120:], name='MA5', line=dict(color='#ef4444', width=1.5)))
    fig_candlestick.add_trace(go.Scatter(x=recent_dates, y=tech['ma20'][-120:], name='MA20', line=dict(color='#f59e0b', width=1.5)))
    fig_candlestick.add_trace(go.Scatter(x=recent_dates, y=tech['ma60'][-120:], name='MA60', line=dict(color='#3b82f6', width=1.5)))
    
    fig_candlestick.update_layout(height=400, template='plotly_white', xaxis_rangeslider_visible=True, hovermode='x unified')
    st.plotly_chart(fig_candlestick, use_container_width=True)
    
    col_indicators1, col_indicators2 = st.columns(2)
    
    with col_indicators1:
        st.markdown("""<div class="card"><h4 style="color: #1e3a5f; margin-bottom: 15px;">RSI 相对强弱指标</h4></div>""", unsafe_allow_html=True)
        
        rsi_values = tech['rsi'][-60:]
        rsi_dates = tech['dates'][-60:]
        
        fig_rsi = go.Figure()
        fig_rsi.add_trace(
            go.Scatter(
                x=rsi_dates, 
                y=rsi_values, 
                name='RSI', 
                line=dict(color='#8b5cf6', width=2), 
                fill='tozeroy', 
                fillcolor='rgba(139,92,246,0.1)'
            )
        )
        fig_rsi.add_hline(y=70, line_dash='dash', line_color='#ef4444', annotation_text='超买')
        fig_rsi.add_hline(y=30, line_dash='dash', line_color='#22c55e', annotation_text='超卖')
        fig_rsi.update_layout(height=200, template='plotly_white', hovermode='x unified')
        st.plotly_chart(fig_rsi, use_container_width=True)
        
        current_rsi = rsi_values[-1] if rsi_values else 50
        if current_rsi > 70:
            rsi_status = 'RSI > 70，处于超买区域，可能面临回调风险'
        elif current_rsi < 30:
            rsi_status = 'RSI < 30，处于超卖区域，可能出现反弹机会'
        else:
            rsi_status = 'RSI 处于正常区间，多空力量均衡'
        st.markdown(f"""<div style="background: #f1f5f9; border-radius: 8px; padding: 12px; margin-bottom: 20px;"><p style="color: #1e3a5f; font-size: 13px; margin: 0;">{rsi_status}</p></div>""", unsafe_allow_html=True)
        
        st.markdown("""<div class="card"><h4 style="color: #1e3a5f; margin-bottom: 15px;">KDJ 随机指标</h4></div>""", unsafe_allow_html=True)
        
        k_values = tech['k'][-60:]
        d_values = tech['d'][-60:]
        
        fig_kdj = go.Figure()
        fig_kdj.add_trace(go.Scatter(x=rsi_dates, y=k_values, name='K', line=dict(color='#ef4444', width=2)))
        fig_kdj.add_trace(go.Scatter(x=rsi_dates, y=d_values, name='D', line=dict(color='#3b82f6', width=2)))
        fig_kdj.add_hline(y=80, line_dash='dash', line_color='#ef4444')
        fig_kdj.add_hline(y=20, line_dash='dash', line_color='#22c55e')
        fig_kdj.update_layout(height=200, template='plotly_white', hovermode='x unified')
        st.plotly_chart(fig_kdj, use_container_width=True)
    
    with col_indicators2:
        st.markdown("""<div class="card"><h4 style="color: #1e3a5f; margin-bottom: 15px;">MACD 指数平滑异同移动平均线</h4></div>""", unsafe_allow_html=True)
        
        macd_values = tech['macd'][-60:]
        signal_values = tech['macd_signal'][-60:]
        hist_values = tech['macd_hist'][-60:]
        
        fig_macd = go.Figure()
        fig_macd.add_trace(go.Scatter(x=rsi_dates, y=macd_values, name='MACD', line=dict(color='#ef4444', width=2)))
        fig_macd.add_trace(go.Scatter(x=rsi_dates, y=signal_values, name='Signal', line=dict(color='#3b82f6', width=2)))
        fig_macd.add_trace(go.Bar(x=rsi_dates, y=hist_values, name='Histogram', marker_color=['#ef4444' if h > 0 else '#22c55e' for h in hist_values]))
        fig_macd.add_hline(y=0, line_color='#94a3b8')
        fig_macd.update_layout(height=200, template='plotly_white', hovermode='x unified')
        st.plotly_chart(fig_macd, use_container_width=True)
        
        macd_status = ''
        if len(macd_values) >= 2 and len(signal_values) >= 2:
            if macd_values[-1] > signal_values[-1] and macd_values[-2] <= signal_values[-2]:
                macd_status = 'MACD 金叉信号，短期看多'
            elif macd_values[-1] < signal_values[-1] and macd_values[-2] >= signal_values[-2]:
                macd_status = 'MACD 死叉信号，短期看空'
            elif macd_values[-1] > 0:
                macd_status = 'MACD 处于正值区域，多头市场'
            else:
                macd_status = 'MACD 处于负值区域，空头市场'
        st.markdown(f"""<div style="background: #f1f5f9; border-radius: 8px; padding: 12px; margin-bottom: 20px;"><p style="color: #1e3a5f; font-size: 13px; margin: 0;">{macd_status}</p></div>""", unsafe_allow_html=True)
        
        st.markdown("""<div class="card"><h4 style="color: #1e3a5f; margin-bottom: 15px;">布林带</h4></div>""", unsafe_allow_html=True)
        
        upper = tech['bollinger_upper'][-60:]
        lower = tech['bollinger_lower'][-60:]
        mid = tech['bollinger_mid'][-60:]
        
        fig_boll = go.Figure()
        fig_boll.add_trace(go.Scatter(x=rsi_dates, y=upper, name='上轨', line=dict(color='#ef4444', width=1, dash='dash')))
        fig_boll.add_trace(go.Scatter(x=rsi_dates, y=mid, name='中轨', line=dict(color='#f59e0b', width=1.5)))
        fig_boll.add_trace(go.Scatter(x=rsi_dates, y=lower, name='下轨', line=dict(color='#22c55e', width=1, dash='dash')))
        fig_boll.add_trace(go.Scatter(x=rsi_dates, y=recent_closes[-60:], name='收盘价', line=dict(color='#3b82f6', width=2)))
        fig_boll.update_layout(height=200, template='plotly_white', hovermode='x unified')
        st.plotly_chart(fig_boll, use_container_width=True)
        
        current_price_boll = recent_closes[-1] if recent_closes else 0
        upper_val = upper[-1] if len(upper) > 0 else 0
        lower_val = lower[-1] if len(lower) > 0 else 0
        mid_val = mid[-1] if len(mid) > 0 else 0
        
        if current_price_boll > upper_val:
            boll_status = '股价突破布林带上轨，处于强势超买区域，短期内有回调风险'
        elif current_price_boll < lower_val:
            boll_status = '股价跌破布林带下轨，处于弱势超卖区域，可能出现技术性反弹'
        elif current_price_boll > mid_val:
            boll_status = '股价在布林带中轨与上轨之间运行，短期趋势偏多'
        else:
            boll_status = '股价在布林带中轨与下轨之间运行，短期趋势偏弱'
        
        band_width = ((upper_val - lower_val) / mid_val * 100) if mid_val > 0 else 0
        if band_width > 10:
            volatility_comment = '布林带开口较大，市场波动剧烈，趋势可能正在形成'
        elif band_width > 5:
            volatility_comment = '布林带宽度适中，市场波动正常'
        else:
            volatility_comment = '布林带收口，市场波动收窄，可能即将出现方向性突破'
        
        st.markdown(f"""
        <div style="background: #f1f5f9; border-radius: 8px; padding: 12px; margin-bottom: 20px;">
            <p style="color: #1e3a5f; font-size: 13px; margin: 0;">{boll_status}。{volatility_comment}。</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""<div class="card"><h3 style="color: #1e3a5f; margin-bottom: 15px;">技术面综合研判</h3></div>""", unsafe_allow_html=True)
    
    ma5_last = tech['ma5'][-1] if tech['ma5'] else 0
    ma20_last = tech['ma20'][-1] if tech['ma20'] else 0
    ma60_last = tech['ma60'][-1] if tech['ma60'] else 0
    current_price = tech['current_price']
    current_rsi = tech['rsi'][-1] if tech['rsi'] else 50
    macd_last = tech['macd'][-1] if tech['macd'] else 0
    signal_last = tech['macd_signal'][-1] if tech['macd_signal'] else 0
    
    trend_score = 0
    trend_notes = []
    
    if current_price > ma5_last:
        trend_score += 1
        trend_notes.append('股价位于MA5上方')
    else:
        trend_score -= 1
        trend_notes.append('股价位于MA5下方')
    
    if ma5_last > ma20_last:
        trend_score += 1
        trend_notes.append('MA5上穿MA20形成多头排列')
    else:
        trend_score -= 1
        trend_notes.append('MA5下穿MA20形成空头排列')
    
    if current_price > ma60_last:
        trend_score += 1
        trend_notes.append('股价位于MA60上方，中长期趋势向好')
    else:
        trend_score -= 1
        trend_notes.append('股价位于MA60下方，中长期趋势承压')
    
    if current_rsi > 50:
        trend_score += 1
        trend_notes.append('RSI大于50，买方力量占优')
    else:
        trend_score -= 1
        trend_notes.append('RSI小于50，卖方力量占优')
    
    if macd_last > signal_last:
        trend_score += 1
        trend_notes.append('MACD在信号线上方，动量偏多')
    else:
        trend_score -= 1
        trend_notes.append('MACD在信号线下方，动量偏空')
    
    if trend_score >= 3:
        overall_trend = '强烈看多'
        trend_color = '#22c55e'
    elif trend_score >= 1:
        overall_trend = '偏多震荡'
        trend_color = '#84cc16'
    elif trend_score >= -1:
        overall_trend = '方向不明'
        trend_color = '#f59e0b'
    elif trend_score >= -3:
        overall_trend = '偏空震荡'
        trend_color = '#f97316'
    else:
        overall_trend = '强烈看空'
        trend_color = '#ef4444'
    
    support_level = min(data['lows'][-20:]) if data['lows'] else current_price * 0.95
    resistance_level = max(data['highs'][-20:]) if data['highs'] else current_price * 1.05
    
    st.markdown(f"""
    <div style="background: #f8fafc; border-radius: 12px; padding: 20px;">
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <div style="background: {trend_color}; border-radius: 8px; padding: 10px 20px; margin-right: 15px;">
                <p style="color: white; font-size: 18px; font-weight: bold; margin: 0;">{overall_trend}</p>
            </div>
            <p style="color: #64748b; font-size: 13px; margin: 0;">技术面综合评分: {trend_score}/5</p>
        </div>
        <p style="color: #1e3a5f; font-size: 14px; line-height: 1.8; margin: 0;">
            <strong>指标综合解读：</strong>{'、'.join(trend_notes)}。<br><br>
            <strong>趋势判断：</strong>综合各项技术指标，该股票当前技术面呈现<strong style="color: {trend_color};">{overall_trend}</strong>信号。
            {'多项指标共振向上，短期内上涨概率较大，可考虑逢低介入。' if trend_score >= 3 else '部分指标显示积极信号，但力度有限，建议保持观望或轻仓参与。' if trend_score >= 1 else '多空指标交织，方向尚不明朗，建议等待明确信号后再做决策。' if trend_score >= -1 else '部分指标走弱，下行压力较大，建议控制仓位防范风险。' if trend_score >= -3 else '多项指标共振向下，短期内下跌风险较大，建议减仓避险。'}<br><br>
            <strong>支撑与压力：</strong>近期支撑位约为<strong>{support_level:.2f}</strong>，压力位约为<strong>{resistance_level:.2f}</strong>。
            当前价格距离支撑位约{abs((current_price - support_level) / support_level * 100):.1f}%，距离压力位约{abs((current_price - resistance_level) / resistance_level * 100):.1f}%。
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_tab3():
    st.markdown("""<div class="card"><h3 style="color: #1e3a5f; margin-bottom: 15px;">未来走势预测分析</h3></div>""", unsafe_allow_html=True)
    
    symbol = st.session_state.get('search_symbol', '600519')
    stock_info = get_stock_info(symbol)
    data = generate_simulation_data(stock_info['symbol'])
    tech = calculate_technical_indicators(data)
    val_result = calculate_valuation(data)
    
    col_pred1, col_pred2, col_pred3 = st.columns(3)
    
    with col_pred1:
        st.markdown(f"""
        <div style="background: {val_result['conclusion_color']}; border-radius: 12px; padding: 20px; text-align: center;">
            <p style="color: white; font-size: 13px; margin: 0; opacity: 0.9;">AI估值结论</p>
            <p style="color: white; font-size: 36px; font-weight: bold; margin: 10px 0;">{val_result['conclusion']}</p>
            <p style="color: white; font-size: 12px; margin: 0; opacity: 0.8;">基于多模型综合评估</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_pred2:
        st.markdown(f"""
        <div style="background: #f8fafc; border-radius: 12px; padding: 20px; text-align: center;">
            <p style="color: #64748b; font-size: 13px; margin: 0;">当前价格</p>
            <p style="color: #1e3a5f; font-size: 32px; font-weight: bold; margin: 10px 0;">{val_result['current_price']:.2f}</p>
            <p style="color: #94a3b8; font-size: 12px; margin: 0;">最新交易价格</p>
        </div>
        """, unsafe_allow_html=True)
    
    diff_color = '#22c55e' if val_result['valuation_diff'] > 0 else '#ef4444'
    with col_pred3:
        st.markdown(f"""
        <div style="background: #f8fafc; border-radius: 12px; padding: 20px; text-align: center;">
            <p style="color: #64748b; font-size: 13px; margin: 0;">AI合理估值</p>
            <p style="color: #1e3a5f; font-size: 32px; font-weight: bold; margin: 10px 0;">{val_result['fair_value']:.2f}</p>
            <p style="color: {diff_color}; font-size: 14px; font-weight: bold; margin: 0;">{val_result['valuation_diff']:+}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""<div class="card"><h4 style="color: #1e3a5f; margin-bottom: 15px;">多模型估值对比</h4></div>""", unsafe_allow_html=True)
    
    models = list(val_result['model_results'].keys())
    values = list(val_result['model_results'].values())
    
    fig_models = go.Figure()
    fig_models.add_trace(go.Bar(x=models, y=values, marker_color='#3b82f6'))
    fig_models.add_hline(y=val_result['current_price'], line_dash='dash', line_color='#ef4444', annotation_text=f'当前价 {val_result["current_price"]}')
    fig_models.add_hline(y=val_result['fair_value'], line_dash='dash', line_color='#22c55e', annotation_text=f'合理估值 {val_result["fair_value"]}')
    fig_models.update_layout(height=300, template='plotly_white', yaxis_title='估值')
    st.plotly_chart(fig_models, use_container_width=True)
    
    st.markdown("""<div class="card"><h4 style="color: #1e3a5f; margin-bottom: 15px;">未来价格走势预测</h4></div>""", unsafe_allow_html=True)
    
    last_price = tech['current_price']
    volatility = tech['volatility']
    prediction_days = 60
    
    future_dates = []
    future_prices_base = []
    future_prices_bull = []
    future_prices_bear = []
    
    current_date = tech['dates'][-1] if tech['dates'] else datetime.now()
    base_price = last_price
    bull_price = last_price
    bear_price = last_price
    
    for i in range(prediction_days):
        current_date += timedelta(days=1)
        if current_date.weekday() < 5:
            future_dates.append(current_date)
            
            base_price *= (1 + random.gauss(0, volatility/252))
            bull_price *= (1 + random.gauss(volatility/500, volatility/252))
            bear_price *= (1 + random.gauss(-volatility/500, volatility/252))
            
            future_prices_base.append(base_price)
            future_prices_bull.append(bull_price)
            future_prices_bear.append(bear_price)
    
    fig_pred = go.Figure()
    fig_pred.add_trace(go.Scatter(x=tech['dates'][-30:], y=tech['prices'][-30:], name='历史价格', line=dict(color='#94a3b8', width=2)))
    fig_pred.add_trace(go.Scatter(x=future_dates, y=future_prices_base, name='基准预测', line=dict(color='#3b82f6', width=2, dash='dash')))
    fig_pred.add_trace(go.Scatter(x=future_dates, y=future_prices_bull, name='乐观预测', line=dict(color='#22c55e', width=1.5, dash='dot')))
    fig_pred.add_trace(go.Scatter(x=future_dates, y=future_prices_bear, name='悲观预测', line=dict(color='#ef4444', width=1.5, dash='dot')))
    fig_pred.update_layout(height=350, template='plotly_white', hovermode='x unified', title='未来60个交易日价格预测')
    st.plotly_chart(fig_pred, use_container_width=True)
    
    avg_base = np.mean(future_prices_base) if future_prices_base else last_price
    avg_bull = np.mean(future_prices_bull) if future_prices_bull else last_price
    avg_bear = np.mean(future_prices_bear) if future_prices_bear else last_price
    
    pred_change_base = (future_prices_base[-1] - last_price) / last_price * 100 if future_prices_base else 0
    pred_change_bull = (future_prices_bull[-1] - last_price) / last_price * 100 if future_prices_bull else 0
    pred_change_bear = (future_prices_bear[-1] - last_price) / last_price * 100 if future_prices_bear else 0
    
    if pred_change_base > 10:
        outlook = '乐观'
        outlook_color = '#22c55e'
    elif pred_change_base > 0:
        outlook = '谨慎乐观'
        outlook_color = '#84cc16'
    elif pred_change_base > -10:
        outlook = '谨慎'
        outlook_color = '#f59e0b'
    else:
        outlook = '悲观'
        outlook_color = '#ef4444'
    
    st.markdown(f"""
    <div style="background: #f8fafc; border-radius: 12px; padding: 20px; margin-top: 15px;">
        <h4 style="color: #1e3a5f; margin: 0 0 15px 0;">预测情景分析</h4>
        <p style="color: #1e3a5f; font-size: 14px; line-height: 1.8; margin: 0;">
            <strong>基准情景：</strong>基于历史波动率和随机游走模型，未来60个交易日基准预测均价约为{avg_base:.2f}，
            期末价格较当前预计变动{pred_change_base:+.1f}%。该情景假设市场保持现有波动特征，无重大利好或利空事件。<br><br>
            <strong>乐观情景：</strong>若市场环境改善、业绩超预期或行业政策利好，期末价格较当前有望上涨{pred_change_bull:+.1f}%，
            均价约为{avg_bull:.2f}。此情景下股价可能突破近期高点，适合趋势跟踪策略。<br><br>
            <strong>悲观情景：</strong>若市场系统性风险上升、业绩不及预期或宏观环境恶化，期末价格较当前可能下跌{abs(pred_change_bear):.1f}%，
            均价约为{avg_bear:.2f}。此情景下需关注止损位设置，防范下行风险。<br><br>
            <strong>综合展望：</strong>当前 outlook 为 <strong style="color: {outlook_color};">{outlook}</strong>。
            {"基准情景显示股价有较好上涨空间，建议积极关注。" if pred_change_base > 10 else "基准情景偏正面，可适当参与。" if pred_change_base > 0 else "基准情景偏负面，建议保持谨慎。" if pred_change_base > -10 else "基准情景显示下行压力较大，建议控制仓位。"}
            乐观与悲观情景的价差幅度反映了未来不确定性的高低，投资者应根据自身风险承受能力选择合适的仓位。
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""<div class="card"><h4 style="color: #1e3a5f; margin-bottom: 15px;">估值模型解读</h4></div>""", unsafe_allow_html=True)
    
    model_results = val_result['model_results']
    model_explanations = {
        '零增长DDM': '假设公司股息永续不变，适用于成熟稳定型企业。估值结果反映公司当前股息的安全边际。',
        '戈登增长模型': '假设股息以固定增长率永续增长，适用于具有稳定分红政策的成长型企业。',
        '两阶段DDM': '假设前期高增长、后期稳定增长，更符合企业生命周期特征，适用于成长转成熟型企业。',
        'PE估值法': '基于当前市盈率与每股收益计算，反映市场对公司盈利能力的定价水平。',
        'PB估值法': '基于市净率与每股净资产计算，适用于资产驱动型企业或周期行业。',
        'Graham公式': '价值投资之父格雷厄姆的经典估值公式，兼顾盈利和净资产，寻找安全边际。',
        'PEG估值': '市盈率相对盈利增长比率，衡量估值与成长的匹配度，PEG小于1通常被认为低估。'
    }
    
    for model_name, model_value in model_results.items():
        diff_pct = (model_value - val_result['current_price']) / val_result['current_price'] * 100 if val_result['current_price'] > 0 else 0
        diff_color = '#22c55e' if diff_pct > 0 else '#ef4444'
        st.markdown(f"""
        <div style="background: #f1f5f9; border-radius: 8px; padding: 12px; margin-bottom: 8px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #1e3a5f; font-size: 13px; font-weight: bold;">{model_name}</span>
                <span style="color: {diff_color}; font-size: 13px; font-weight: bold;">{model_value:.2f} ({diff_pct:+.1f}%)</span>
            </div>
            <p style="color: #64748b; font-size: 12px; margin: 5px 0 0 0;">{model_explanations.get(model_name, '')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: #fef3c7; border-radius: 10px; padding: 15px; margin-top: 15px;">
        <p style="color: #92400e; font-size: 13px; line-height: 1.6; margin: 0;">
            <strong>模型综合解读：</strong>各模型估值结果存在差异，这反映了不同估值视角的侧重点不同。
            当前AI综合估值为<strong>{val_result['fair_value']:.2f}</strong>，较当前价格{'高估' if val_result['valuation_diff'] < 0 else '低估'}
            <strong>{abs(val_result['valuation_diff']):.1f}%</strong>。
            {"多数模型显示估值偏高，需警惕估值回归风险，关注业绩能否支撑当前股价。" if val_result['valuation_diff'] < -10 else "多数模型显示估值合理，股价与内在价值基本匹配。" if abs(val_result['valuation_diff']) <= 10 else "多数模型显示估值偏低，具备一定安全边际，可关注配置机会。"}
            建议结合行业周期、公司基本面变化和市场情绪综合判断。
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_tab4():
    st.markdown("""<div class="card"><h3 style="color: #1e3a5f; margin-bottom: 15px;">投资建议与结论</h3></div>""", unsafe_allow_html=True)
    
    symbol = st.session_state.get('search_symbol', '600519')
    stock_info = get_stock_info(symbol)
    data = generate_simulation_data(stock_info['symbol'])
    tech = calculate_technical_indicators(data)
    val_result = calculate_valuation(data)
    
    col_summary1, col_summary2 = st.columns(2)
    
    with col_summary1:
        st.markdown(f"""
        <div style="background: {val_result['conclusion_color']}; border-radius: 12px; padding: 25px;">
            <h3 style="color: white; margin: 0 0 15px 0;">投资价值判断</h3>
            <p style="color: white; font-size: 16px; margin: 0;">
                根据多模型综合估值分析，{stock_info['name']} 当前被{val_result['conclusion']}。
            </p>
            <div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.3);">
                <p style="color: white; font-size: 12px; opacity: 0.85; margin: 0;">当前价格: {val_result['current_price']:.2f}</p>
                <p style="color: white; font-size: 12px; opacity: 0.85; margin: 5px 0;">AI估值: {val_result['fair_value']:.2f}</p>
                <p style="color: white; font-size: 14px; font-weight: bold; margin: 5px 0;">偏差: {val_result['valuation_diff']:+}%</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_summary2:
        st.markdown("""<div style="background: #f8fafc; border-radius: 12px; padding: 25px;"><h3 style="color: #1e3a5f; margin: 0 0 15px 0;">当前位置判断</h3>""", unsafe_allow_html=True)
        
        prices = tech['prices'][-252:] if len(tech['prices']) >= 252 else tech['prices']
        if len(prices) >= 2:
            year_high = max(prices)
            year_low = min(prices)
            current_price = tech['current_price']
            position_pct = (current_price - year_low) / (year_high - year_low + 1e-10) * 100
            
            if position_pct > 80:
                position_status = '近期高点区域'
                position_color = '#ef4444'
            elif position_pct < 20:
                position_status = '近期低点区域'
                position_color = '#22c55e'
            else:
                position_status = '中位区间'
                position_color = '#64748b'
            
            st.markdown(f"""
                <p style="color: {position_color}; font-size: 20px; font-weight: bold; margin: 0;">{position_status}</p>
                <p style="color: #64748b; font-size: 13px; margin: 10px 0;">当前股价处于年内高低点的{position_pct:.1f}%位置</p>
                <div style="display: flex; justify-content: space-between; font-size: 12px; color: #94a3b8; margin-top: 15px;">
                    <span>年内低点: {year_low:.2f}</span>
                    <span>年内高点: {year_high:.2f}</span>
                </div>
            </div>""", unsafe_allow_html=True)
    
    st.markdown("""<div class="card"><h4 style="color: #1e3a5f; margin-bottom: 15px;">综合分析指标</h4></div>""", unsafe_allow_html=True)
    
    col_analysis1, col_analysis2, col_analysis3, col_analysis4 = st.columns(4)
    
    indicators = [
        ('估值状态', val_result['conclusion'], val_result['conclusion_color']),
        ('波动率', f'{tech["volatility"]*100:.1f}%', '#ef4444' if tech['volatility'] > 0.4 else '#22c55e'),
        ('夏普比率', f'{tech["sharpe_ratio"]:.2f}', '#22c55e' if tech['sharpe_ratio'] > 1 else '#f59e0b'),
        ('最大回撤', f'{tech["max_drawdown"]:.1f}%', '#ef4444')
    ]
    
    for i, (label, value, color) in enumerate(indicators):
        with [col_analysis1, col_analysis2, col_analysis3, col_analysis4][i]:
            st.markdown(f"""
            <div style="background: #f8fafc; border-radius: 10px; padding: 15px; border-left: 4px solid {color}; text-align: center;">
                <p style="color: #64748b; font-size: 12px; margin: 0;">{label}</p>
                <p style="color: {color}; font-size: 24px; font-weight: bold; margin: 5px 0;">{value}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("""<div class="card"><h4 style="color: #1e3a5f; margin-bottom: 15px;">投资建议</h4></div>""", unsafe_allow_html=True)
    
    rsi = tech['rsi'][-1] if tech['rsi'] else 50
    macd = tech['macd'][-1] if tech['macd'] else 0
    signal = tech['macd_signal'][-1] if tech['macd_signal'] else 0
    
    recommendation = ''
    if val_result['conclusion'] == '低估':
        if rsi < 40:
            recommendation = '强烈建议关注：股票估值偏低且技术面处于超卖区域，是较好的买入时机。建议逐步建仓，分批买入。'
        elif rsi > 60:
            recommendation = '建议等待：股票估值偏低，但短期技术面偏强，建议等待回调后再介入。'
        else:
            recommendation = '建议关注：股票估值偏低，可逢低建仓，设置合理止损位。'
    elif val_result['conclusion'] == '高估':
        if rsi > 60:
            recommendation = '建议谨慎：股票估值偏高且技术面处于超买区域，风险较大。建议减仓或观望。'
        elif rsi < 40:
            recommendation = '建议观望：股票估值偏高，但短期技术面偏弱，可能有反弹机会，但整体风险较大。'
        else:
            recommendation = '建议持有：股票估值偏高，已持有者可继续观察，未持有者建议等待估值回归。'
    else:
        if macd > signal:
            recommendation = '建议持有：股票估值合理，技术面呈现多头信号，可继续持有观察。'
        else:
            recommendation = '建议观望：股票估值合理，技术面方向不明，建议等待明确信号。'
    
    st.markdown(f"""
    <div style="background: #f1f5f9; border-radius: 12px; padding: 20px;">
        <p style="color: #1e3a5f; font-size: 15px; margin: 0;">{recommendation}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""<div class="card"><h4 style="color: #1e3a5f; margin-bottom: 15px;">操作策略与仓位建议</h4></div>""", unsafe_allow_html=True)
    
    volatility = tech['volatility']
    current_price = tech['current_price']
    fair_value = val_result['fair_value']
    
    if val_result['conclusion'] == '低估':
        if volatility < 0.25:
            position_size = '60%-80%'
            position_desc = '可重仓配置'
            strategy = '价值型投资策略'
        elif volatility < 0.4:
            position_size = '40%-60%'
            position_desc = '可中度配置'
            strategy = '均衡型投资策略'
        else:
            position_size = '20%-40%'
            position_desc = '轻仓试探'
            strategy = '防御型投资策略'
    elif val_result['conclusion'] == '高估':
        if volatility < 0.25:
            position_size = '20%-30%'
            position_desc = '减仓观望'
            strategy = '保守型投资策略'
        elif volatility < 0.4:
            position_size = '10%-20%'
            position_desc = '轻仓持有或减仓'
            strategy = '防御型投资策略'
        else:
            position_size = '0%-10%'
            position_desc = '建议清仓或极轻仓'
            strategy = '避险型投资策略'
    else:
        if volatility < 0.25:
            position_size = '40%-60%'
            position_desc = '可中度配置'
            strategy = '均衡型投资策略'
        elif volatility < 0.4:
            position_size = '30%-50%'
            position_desc = '适度参与'
            strategy = '稳健型投资策略'
        else:
            position_size = '20%-30%'
            position_desc = '轻仓参与'
            strategy = '谨慎型投资策略'
    
    stop_loss = current_price * 0.92 if val_result['conclusion'] == '低估' else current_price * 0.95
    take_profit = fair_value * 1.05 if val_result['conclusion'] == '低估' else current_price * 1.08
    
    st.markdown(f"""
    <div style="background: #f8fafc; border-radius: 12px; padding: 20px;">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
            <div style="background: #e0f2fe; border-radius: 8px; padding: 15px;">
                <p style="color: #64748b; font-size: 12px; margin: 0;">建议仓位比例</p>
                <p style="color: #1e3a5f; font-size: 24px; font-weight: bold; margin: 5px 0;">{position_size}</p>
                <p style="color: #64748b; font-size: 12px; margin: 0;">{position_desc}</p>
            </div>
            <div style="background: #fef3c7; border-radius: 8px; padding: 15px;">
                <p style="color: #64748b; font-size: 12px; margin: 0;">投资策略类型</p>
                <p style="color: #1e3a5f; font-size: 20px; font-weight: bold; margin: 5px 0;">{strategy}</p>
                <p style="color: #64748b; font-size: 12px; margin: 0;">基于估值与波动率匹配</p>
            </div>
        </div>
        <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #e2e8f0;">
            <p style="color: #1e3a5f; font-size: 14px; line-height: 1.8; margin: 0;">
                <strong>建仓策略：</strong>{'可采取分批建仓方式，在回调时分段买入，降低平均成本。首笔建仓建议不超过计划总仓位的30%，后续根据走势逐步加码。' if val_result['conclusion'] == '低估' else '建议观望为主，若已持有可考虑逢高减仓。新资金暂不入局，等待估值回归合理区间。' if val_result['conclusion'] == '高估' else '可小仓位试探性参与，等待方向明确后再加大投入。建议采用定投方式平滑成本。'}<br><br>
                <strong>止损设置：</strong>建议将止损位设在<strong>{stop_loss:.2f}</strong>元（约较当前价格下跌{abs((stop_loss - current_price) / current_price * 100):.1f}%）。
                {"估值低估提供了一定的安全垫，可适当放宽止损空间。" if val_result['conclusion'] == '低估' else "估值偏高时需严格控制风险，止损应更加敏感。" if val_result['conclusion'] == '高估' else "设置合理止损，保护本金安全。"}<br><br>
                <strong>止盈目标：</strong>第一目标位建议设在<strong>{take_profit:.2f}</strong>元（约较当前价格上涨{abs((take_profit - current_price) / current_price * 100):.1f}%）。
                到达目标后可考虑分批止盈，锁定部分利润，保留底仓观察后续走势。<br><br>
                <strong>持有周期：</strong>{'基于当前低估状态，建议中长期持有（6个月以上），等待估值修复。' if val_result['conclusion'] == '低估' else '基于当前高估状态，建议短期持有（1-3个月）或逢高减仓。' if val_result['conclusion'] == '高估' else '建议中短期持有（3-6个月），根据后续估值变化和技术面信号调整持仓。'}<br><br>
                <strong>关键监控指标：</strong>持续关注公司季度财报业绩变化、行业政策动向、大盘系统性风险。
                若基本面发生重大恶化或技术面出现破位信号，应及时调整策略。
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""<div class="card"><h4 style="color: #1e3a5f; margin-bottom: 15px;">历史走势回顾</h4></div>""", unsafe_allow_html=True)
    
    fig_history = go.Figure()
    fig_history.add_trace(
        go.Scatter(
            x=tech['dates'][-252:], 
            y=tech['prices'][-252:], 
            name='收盘价', 
            line=dict(color='#3b82f6', width=2), 
            fill='tozeroy', 
            fillcolor='rgba(59,130,246,0.1)'
        )
    )
    fig_history.add_trace(go.Scatter(x=tech['dates'][-252:], y=tech['ma60'][-252:], name='MA60', line=dict(color='#f59e0b', width=1.5)))
    fig_history.update_layout(height=300, template='plotly_white', xaxis_rangeslider_visible=True, hovermode='x unified', title='近一年价格走势')
    st.plotly_chart(fig_history, use_container_width=True)
    
    st.markdown("""
    <div style="background: #fef3c7; border-radius: 10px; padding: 15px; margin-top: 20px;">
        <p style="color: #92400e; font-size: 13px; margin: 0;">
            风险提示: 本系统提供的分析仅供参考，不构成投资建议。投资有风险，入市需谨慎。
            所有数据均为模拟数据，实际投资决策请参考真实市场数据和专业投资顾问意见。
        </p>
    </div>
    """, unsafe_allow_html=True)

def main():
    st.markdown("""
    <div class="header-container">
        <h1 class="main-title">普惠 AI 股息估值系统</h1>
        <p class="sub-title">多阶段股息贴现模型 · 专业金融内核 · 零门槛操作</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["股票概览", "技术指标", "走势预测", "投资建议"])
    
    with tab1:
        render_tab1()
    with tab2:
        render_tab2()
    with tab3:
        render_tab3()
    with tab4:
        render_tab4()
    
    st.markdown("""
    <div style="text-align: center; padding: 20px; margin-top: 20px; color: #94a3b8; font-size: 12px;">
        <p>教材依据：《公司理财》罗斯 | 《证券投资学》吴晓求 | 《金融数据分析与Python应用》</p>
        <p>风险声明：本系统仅供学习研究，不构成投资建议。投资有风险，决策需谨慎。</p>
        <p>数据来源：模拟数据 | 模型：多阶段股息贴现模型(DDM)</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()