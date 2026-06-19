import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

st.set_page_config(
    page_title="专业金融分析平台",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 50%, #1e3a5f 100%);
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 20px rgba(30, 58, 95, 0.3);
    }
    
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 18px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        border-left: 5px solid #2d5a87;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.12);
    }
    
    .positive-change {
        color: #22c55e;
        font-weight: bold;
    }
    
    .negative-change {
        color: #ef4444;
        font-weight: bold;
    }
    
    .info-box {
        background: #dbeafe;
        border-left: 4px solid #3b82f6;
        padding: 18px;
        border-radius: 8px;
        margin: 12px 0;
    }
    
    .warning-box {
        background: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 18px;
        border-radius: 8px;
        margin: 12px 0;
    }
    
    .success-box {
        background: #dcfce7;
        border-left: 4px solid #22c55e;
        padding: 18px;
        border-radius: 8px;
        margin: 12px 0;
    }
    
    .danger-box {
        background: #fee2e2;
        border-left: 4px solid #ef4444;
        padding: 18px;
        border-radius: 8px;
        margin: 12px 0;
    }
    
    .sidebar-section {
        background: #f8fafc;
        padding: 12px 15px;
        border-radius: 8px;
        margin: 8px 0;
        border: 1px solid #e2e8f0;
    }
    
    .nav-button {
        background: linear-gradient(135deg, #2d5a87 0%, #1e3a5f 100%);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 12px;
        font-weight: 600;
        width: 100%;
        text-align: left;
        margin: 3px 0;
        transition: all 0.2s;
        font-size: 14px;
    }
    
    .nav-button:hover {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
        padding-left: 15px;
    }
    
    h1, h2, h3 {
        color: #0f172a;
        margin-bottom: 8px;
    }
    
    .section-title {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 12px;
    }
    
    /* 优化侧边栏样式 */
    .css-1d391kg {
        padding-top: 1rem;
    }
    
    .css-1lcbmhc {
        padding: 1rem;
    }
    
    /* 优化数据展示卡片 */
    .stMetric {
        background: white;
        border-radius: 8px;
        padding: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border-left: 3px solid #2d5a87;
    }
    
    /* 优化图表容器 */
    .js-plotly-plot {
        border-radius: 8px;
    }
    
    /* 减少间距 */
    .streamlit-container {
        padding-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

STOCK_SYMBOLS = {
    '贵州茅台': {'symbol': '600519.SS', 'industry': '白酒', 'sector': '消费', 'market': 'A股', 
                'pe': 25.5, 'pb': 6.2, 'dividend': 2.8, 'eps': 48.5, 'revenue_growth': 18.2, 'net_profit_growth': 20.5,
                'roe': 29.8, 'roa': 15.2, 'debt_ratio': 21.5, 'current_ratio': 2.8, 'inventory_turnover': 1.2},
    '五粮液': {'symbol': '000858.SZ', 'industry': '白酒', 'sector': '消费', 'market': 'A股', 
                'pe': 18.3, 'pb': 4.5, 'dividend': 2.5, 'eps': 6.8, 'revenue_growth': 15.3, 'net_profit_growth': 16.8,
                'roe': 22.5, 'roa': 12.8, 'debt_ratio': 28.3, 'current_ratio': 2.2, 'inventory_turnover': 1.8},
    '招商银行': {'symbol': '600036.SS', 'industry': '银行', 'sector': '金融', 'market': 'A股', 
                'pe': 7.8, 'pb': 1.2, 'dividend': 4.5, 'eps': 5.2, 'revenue_growth': 8.5, 'net_profit_growth': 12.3,
                'roe': 16.8, 'roa': 1.2, 'debt_ratio': 92.5, 'current_ratio': 0.8, 'inventory_turnover': 0},
    '中国平安': {'symbol': '601318.SS', 'industry': '保险', 'sector': '金融', 'market': 'A股', 
                'pe': 9.2, 'pb': 1.1, 'dividend': 3.2, 'eps': 4.8, 'revenue_growth': 6.2, 'net_profit_growth': 15.8,
                'roe': 14.5, 'roa': 1.8, 'debt_ratio': 90.2, 'current_ratio': 1.2, 'inventory_turnover': 0},
    '比亚迪': {'symbol': '002594.SZ', 'industry': '新能源汽车', 'sector': '制造业', 'market': 'A股', 
                'pe': 85.6, 'pb': 8.9, 'dividend': 1.2, 'eps': 5.2, 'revenue_growth': 72.3, 'net_profit_growth': 128.5,
                'roe': 15.8, 'roa': 6.2, 'debt_ratio': 68.5, 'current_ratio': 1.3, 'inventory_turnover': 4.5},
    '宁德时代': {'symbol': '300750.SZ', 'industry': '动力电池', 'sector': '制造业', 'market': 'A股', 
                'pe': 45.2, 'pb': 6.8, 'dividend': 1.5, 'eps': 8.5, 'revenue_growth': 48.5, 'net_profit_growth': 82.1,
                'roe': 20.5, 'roa': 9.8, 'debt_ratio': 58.2, 'current_ratio': 1.5, 'inventory_turnover': 3.8},
    '腾讯控股': {'symbol': '00700.HK', 'industry': '互联网', 'sector': '科技', 'market': '港股', 
                'pe': 22.1, 'pb': 3.8, 'dividend': 1.8, 'eps': 12.5, 'revenue_growth': 10.5, 'net_profit_growth': 18.2,
                'roe': 25.8, 'roa': 18.5, 'debt_ratio': 25.2, 'current_ratio': 3.2, 'inventory_turnover': 0},
    '阿里巴巴': {'symbol': 'BABA', 'industry': '互联网', 'sector': '科技', 'market': '美股', 
                'pe': 16.5, 'pb': 2.1, 'dividend': 0.8, 'eps': 5.8, 'revenue_growth': 8.3, 'net_profit_growth': 25.6,
                'roe': 18.2, 'roa': 8.5, 'debt_ratio': 45.8, 'current_ratio': 1.8, 'inventory_turnover': 0},
    '苹果': {'symbol': 'AAPL', 'industry': '消费电子', 'sector': '科技', 'market': '美股', 
                'pe': 28.3, 'pb': 6.1, 'dividend': 0.6, 'eps': 6.1, 'revenue_growth': 2.5, 'net_profit_growth': 5.8,
                'roe': 31.5, 'roa': 21.8, 'debt_ratio': 72.5, 'current_ratio': 1.5, 'inventory_turnover': 7.2},
    '特斯拉': {'symbol': 'TSLA', 'industry': '新能源汽车', 'sector': '制造业', 'market': '美股', 
                'pe': 72.4, 'pb': 12.3, 'dividend': 0.0, 'eps': 3.8, 'revenue_growth': 37.6, 'net_profit_growth': 105.3,
                'roe': 18.5, 'roa': 9.2, 'debt_ratio': 55.8, 'current_ratio': 1.8, 'inventory_turnover': 3.5},
    '工商银行': {'symbol': '601398.SS', 'industry': '银行', 'sector': '金融', 'market': 'A股', 
                'pe': 5.8, 'pb': 0.7, 'dividend': 5.2, 'eps': 3.6, 'revenue_growth': 3.2, 'net_profit_growth': 5.8,
                'roe': 12.5, 'roa': 0.8, 'debt_ratio': 94.2, 'current_ratio': 0.6, 'inventory_turnover': 0},
    '中国移动': {'symbol': '600941.SS', 'industry': '通信', 'sector': '科技', 'market': 'A股', 
                'pe': 12.5, 'pb': 1.6, 'dividend': 3.8, 'eps': 6.8, 'revenue_growth': 8.8, 'net_profit_growth': 12.5,
                'roe': 14.2, 'roa': 4.8, 'debt_ratio': 35.5, 'current_ratio': 1.6, 'inventory_turnover': 0}
}

INDUSTRY_AVERAGES = {
    '白酒': {'pe': 22.5, 'pb': 5.8, 'dividend': 2.6, 'volatility': 25.0, 'roe': 24.5, 'roa': 13.5},
    '银行': {'pe': 6.5, 'pb': 0.8, 'dividend': 4.8, 'volatility': 18.0, 'roe': 14.2, 'roa': 1.0},
    '保险': {'pe': 10.2, 'pb': 1.3, 'dividend': 3.5, 'volatility': 22.0, 'roe': 13.8, 'roa': 1.5},
    '新能源汽车': {'pe': 45.0, 'pb': 6.5, 'dividend': 1.0, 'volatility': 35.0, 'roe': 16.5, 'roa': 7.2},
    '动力电池': {'pe': 38.0, 'pb': 5.2, 'dividend': 1.2, 'volatility': 32.0, 'roe': 18.2, 'roa': 8.5},
    '互联网': {'pe': 25.0, 'pb': 3.5, 'dividend': 1.5, 'volatility': 28.0, 'roe': 22.5, 'roa': 14.2},
    '消费电子': {'pe': 30.0, 'pb': 5.0, 'dividend': 0.8, 'volatility': 26.0, 'roe': 25.8, 'roa': 16.5},
    '通信': {'pe': 15.0, 'pb': 1.5, 'dividend': 3.0, 'volatility': 20.0, 'roe': 12.8, 'roa': 4.2}
}

def generate_stock_data(start_date, end_date, base_price=100, volatility=0.02):
    dates = []
    opens = []
    highs = []
    lows = []
    closes = []
    volumes = []
    
    current_date = start_date
    current_price = base_price
    
    while current_date <= end_date:
        if current_date.weekday() < 5:
            drift = 0.0005
            shock = random.gauss(0, volatility)
            price_change = drift + shock
            current_price = max(current_price * (1 + price_change), 10)
            
            open_price = current_price * (1 + random.uniform(-0.01, 0.01))
            high_price = max(current_price, open_price) * (1 + random.uniform(0, 0.02))
            low_price = min(current_price, open_price) * (1 - random.uniform(0, 0.02))
            
            base_volume = random.randint(5000000, 15000000)
            volume_multiplier = 1 + abs(price_change) * 10
            volume = int(base_volume * volume_multiplier)
            
            dates.append(current_date)
            opens.append(open_price)
            highs.append(high_price)
            lows.append(low_price)
            closes.append(current_price)
            volumes.append(volume)
        
        current_date += timedelta(days=1)
    
    return {'dates': dates, 'opens': opens, 'highs': highs, 'lows': lows, 'closes': closes, 'volumes': volumes}

def calculate_indicators(data):
    closes = data['closes']
    highs = data['highs']
    lows = data['lows']
    volumes = data['volumes']
    dates = data['dates']
    
    ma5, ma10, ma20, ma60 = [], [], [], []
    bb_upper, bb_middle, bb_lower = [], [], []
    rsi = []
    macd, macd_signal, macd_hist = [], [], []
    kdj_k, kdj_d, kdj_j = [], [], []
    atr = []
    obv = []
    roc = []
    cci = []
    wr = []
    
    for i in range(len(closes)):
        ma5.append(sum(closes[i-4:i+1]) / 5 if i >= 4 else None)
        ma10.append(sum(closes[i-9:i+1]) / 10 if i >= 9 else None)
        ma20.append(sum(closes[i-19:i+1]) / 20 if i >= 19 else None)
        ma60.append(sum(closes[i-59:i+1]) / 60 if i >= 59 else None)
        
        if i >= 19:
            period_closes = closes[i-19:i+1]
            middle = sum(period_closes) / 20
            std = (sum([(x - middle)**2 for x in period_closes]) / 20) ** 0.5
            bb_middle.append(middle)
            bb_upper.append(middle + 2 * std)
            bb_lower.append(middle - 2 * std)
        else:
            bb_middle.append(None)
            bb_upper.append(None)
            bb_lower.append(None)
        
        if i >= 13:
            gains = []
            losses = []
            for j in range(i-13, i+1):
                diff = closes[j] - closes[j-1] if j > 0 else 0
                if diff > 0:
                    gains.append(diff)
                else:
                    losses.append(-diff)
            avg_gain = sum(gains) / 14
            avg_loss = sum(losses) / 14 if sum(losses) > 0 else 1
            rsi.append(100 - (100 / (1 + avg_gain/avg_loss)))
        else:
            rsi.append(None)
        
        if i >= 25:
            ema12 = sum(closes[i-11:i+1]) / 12
            ema26 = sum(closes[i-25:i+1]) / 26
            macd_val = ema12 - ema26
        else:
            macd_val = None
        macd.append(macd_val)
        
        if i >= 33:
            signal_val = sum([x for x in macd[i-8:i+1] if x is not None]) / 9
        else:
            signal_val = None
        macd_signal.append(signal_val)
        macd_hist.append(macd_val - signal_val if macd_val and signal_val else None)
        
        if i >= 8:
            highest_high = max(highs[i-8:i+1])
            lowest_low = min(lows[i-8:i+1])
            rsv = (closes[i] - lowest_low) / (highest_high - lowest_low) * 100 if highest_high != lowest_low else 50
            k_val = (2/3) * (kdj_k[-1] if kdj_k and kdj_k[-1] else 50) + (1/3) * rsv
            d_val = (2/3) * (kdj_d[-1] if kdj_d and kdj_d[-1] else 50) + (1/3) * k_val
            j_val = 3 * k_val - 2 * d_val
            kdj_k.append(k_val)
            kdj_d.append(d_val)
            kdj_j.append(j_val)
        else:
            kdj_k.append(None)
            kdj_d.append(None)
            kdj_j.append(None)
        
        if i >= 13:
            tr_values = []
            for j in range(i-13, i+1):
                if j > 0:
                    tr = max(highs[j] - lows[j], abs(highs[j] - closes[j-1]), abs(lows[j] - closes[j-1]))
                else:
                    tr = highs[j] - lows[j]
                tr_values.append(tr)
            atr.append(sum(tr_values) / 14)
        else:
            atr.append(None)
        
        obv.append(volumes[i] if i == 0 else obv[-1] + volumes[i] if closes[i] > closes[i-1] else obv[-1] - volumes[i])
        
        roc.append((closes[i] - closes[i-12]) / closes[i-12] * 100 if i >= 12 else None)
        
        if i >= 19:
            tp = sum([highs[j] + lows[j] + closes[j] for j in range(i-19, i+1)]) / 60
            mean_dev = sum([abs((highs[j] + lows[j] + closes[j])/3 - tp) for j in range(i-19, i+1)]) / 20
            cci.append((((highs[i] + lows[i] + closes[i])/3 - tp) / (0.015 * mean_dev)) if mean_dev > 0 else 0)
        else:
            cci.append(None)
        
        if i >= 13:
            highest_high = max(highs[i-13:i+1])
            lowest_low = min(lows[i-13:i+1])
            wr.append((highest_high - closes[i]) / (highest_high - lowest_low) * 100 if highest_high != lowest_low else 50)
        else:
            wr.append(None)
    
    return {
        'dates': dates, 'ma5': ma5, 'ma10': ma10, 'ma20': ma20, 'ma60': ma60,
        'bb_upper': bb_upper, 'bb_middle': bb_middle, 'bb_lower': bb_lower,
        'rsi': rsi, 'macd': macd, 'macd_signal': macd_signal, 'macd_hist': macd_hist,
        'kdj_k': kdj_k, 'kdj_d': kdj_d, 'kdj_j': kdj_j, 'atr': atr, 'obv': obv,
        'roc': roc, 'cci': cci, 'wr': wr
    }

def calculate_fundamental_metrics(data, stock_info):
    closes = data['closes']
    volumes = data['volumes']
    
    current_price = closes[-1] if closes else 0
    market_cap = current_price * 1000000000
    
    daily_return = (closes[-1] - closes[-2]) / closes[-2] * 100 if len(closes) >= 2 else 0
    monthly_return = (closes[-1] - closes[-20]) / closes[-20] * 100 if len(closes) >= 20 else 0
    quarterly_return = (closes[-1] - closes[-60]) / closes[-60] * 100 if len(closes) >= 60 else 0
    yearly_return = (closes[-1] - closes[-250]) / closes[-250] * 100 if len(closes) >= 250 else 0
    
    returns = [(closes[i] - closes[i-1]) / closes[i-1] for i in range(1, len(closes))] if len(closes) >= 2 else []
    volatility = (sum([(r - sum(returns)/len(returns))**2 for r in returns]) / len(returns)) ** 0.5 * 100 if returns else 0
    
    avg_volume = sum(volumes[-20:]) / 20 if len(volumes) >= 20 else 0
    turnover_rate = (volumes[-1] / 1000000000) * 100 if volumes else 0
    
    industry_avg = INDUSTRY_AVERAGES.get(stock_info['industry'], {'pe': 20, 'pb': 2, 'dividend': 2, 'volatility': 25, 'roe': 15, 'roa': 10})
    pe_ratio = stock_info.get('pe', 0)
    pb_ratio = stock_info.get('pb', 0)
    dividend_yield = stock_info.get('dividend', 0)
    roe = stock_info.get('roe', 0)
    roa = stock_info.get('roa', 0)
    
    return {
        'current_price': current_price, 'market_cap': market_cap,
        'daily_return': daily_return, 'monthly_return': monthly_return,
        'quarterly_return': quarterly_return, 'yearly_return': yearly_return,
        'volatility': volatility, 'avg_volume': avg_volume, 'turnover_rate': turnover_rate,
        'pe_ratio': pe_ratio, 'pb_ratio': pb_ratio, 'dividend_yield': dividend_yield,
        'roe': roe, 'roa': roa,
        'pe_relative': pe_ratio / industry_avg['pe'] if industry_avg['pe'] > 0 else 1,
        'pb_relative': pb_ratio / industry_avg['pb'] if industry_avg['pb'] > 0 else 1,
        'industry_pe': industry_avg['pe'], 'industry_pb': industry_avg['pb'],
        'industry_roe': industry_avg['roe'], 'industry_roa': industry_avg['roa'],
        'eps': stock_info.get('eps', 0), 'revenue_growth': stock_info.get('revenue_growth', 0),
        'net_profit_growth': stock_info.get('net_profit_growth', 0),
        'debt_ratio': stock_info.get('debt_ratio', 0), 'current_ratio': stock_info.get('current_ratio', 0),
        'inventory_turnover': stock_info.get('inventory_turnover', 0)
    }

def analyze_technical(data, indicators):
    recent_closes = data['closes'][-30:]
    price_change = (recent_closes[-1] - recent_closes[0]) / recent_closes[0] * 100
    
    ma5_val = indicators['ma5'][-1] if indicators['ma5'][-1] else 0
    ma10_val = indicators['ma10'][-1] if indicators['ma10'][-1] else 0
    ma20_val = indicators['ma20'][-1] if indicators['ma20'][-1] else 0
    ma60_val = indicators['ma60'][-1] if indicators['ma60'][-1] else 0
    
    rsi_val = indicators['rsi'][-1] if indicators['rsi'][-1] else 50
    kdj_k = indicators['kdj_k'][-1] if indicators['kdj_k'][-1] else 50
    kdj_d = indicators['kdj_d'][-1] if indicators['kdj_d'][-1] else 50
    kdj_j = indicators['kdj_j'][-1] if indicators['kdj_j'][-1] else 50
    
    macd_val = indicators['macd'][-1] if indicators['macd'][-1] else 0
    macd_signal = indicators['macd_signal'][-1] if indicators['macd_signal'][-1] else 0
    
    atr_val = indicators['atr'][-1] if indicators['atr'][-1] else 0
    cci_val = indicators['cci'][-1] if indicators['cci'][-1] else 0
    wr_val = indicators['wr'][-1] if indicators['wr'][-1] else 50
    roc_val = indicators['roc'][-1] if indicators['roc'][-1] else 0
    
    analysis_points = []
    signals = []
    risk_level = "中等"
    
    if ma5_val > ma10_val > ma20_val > ma60_val:
        analysis_points.append("📈 **均线系统**: 完美多头排列，技术面强势")
        signals.append("买入")
    elif ma5_val > ma10_val and ma10_val > ma20_val:
        analysis_points.append("📈 **均线系统**: 短期多头排列，趋势向好")
        signals.append("买入")
    elif ma5_val < ma10_val < ma20_val < ma60_val:
        analysis_points.append("📉 **均线系统**: 空头排列，技术面弱势")
        signals.append("卖出")
    else:
        analysis_points.append("🔄 **均线系统**: 均线交织，震荡整理")
        signals.append("观望")
    
    if rsi_val > 80:
        analysis_points.append(f"⚠️ **RSI**: {rsi_val:.1f}，极度超买，强烈看空")
        risk_level = "高风险"
        signals.append("卖出")
    elif rsi_val > 70:
        analysis_points.append(f"🔴 **RSI**: {rsi_val:.1f}，超买区域，谨慎")
        risk_level = "中高风险"
    elif rsi_val < 20:
        analysis_points.append(f"💚 **RSI**: {rsi_val:.1f}，极度超卖，强烈看多")
        risk_level = "低风险"
        signals.append("买入")
    elif rsi_val < 30:
        analysis_points.append(f"🟢 **RSI**: {rsi_val:.1f}，超卖区域，关注反弹")
        risk_level = "中低风险"
    else:
        analysis_points.append(f"⚪ **RSI**: {rsi_val:.1f}，中性区间")
    
    if kdj_k > 80 and kdj_d > 80:
        analysis_points.append(f"🔴 **KDJ**: K={kdj_k:.1f}, D={kdj_d:.1f}，高位死叉风险")
        signals.append("卖出")
    elif kdj_k < 20 and kdj_d < 20:
        analysis_points.append(f"🟢 **KDJ**: K={kdj_k:.1f}, D={kdj_d:.1f}，低位金叉机会")
        signals.append("买入")
    elif kdj_k > kdj_d:
        analysis_points.append(f"📈 **KDJ**: K线上穿D线，金叉形成")
        signals.append("买入")
    else:
        analysis_points.append(f"📉 **KDJ**: K线下穿D线，死叉形成")
        signals.append("卖出")
    
    if macd_val > macd_signal and macd_val > 0:
        analysis_points.append(f"🟢 **MACD**: DIF={macd_val:.3f}, DEA={macd_signal:.3f}，强势上涨")
        signals.append("买入")
    elif macd_val > macd_signal and macd_val < 0:
        analysis_points.append(f"🟡 **MACD**: 弱势反弹，需确认")
    elif macd_val < macd_signal and macd_val > 0:
        analysis_points.append(f"🔴 **MACD**: 强势调整")
    else:
        analysis_points.append(f"🔴 **MACD**: 弱势下跌")
        signals.append("卖出")
    
    current_price = data['closes'][-1]
    bb_upper = indicators['bb_upper'][-1]
    bb_lower = indicators['bb_lower'][-1]
    
    if bb_upper and bb_lower:
        bb_position = (current_price - bb_lower) / (bb_upper - bb_lower) * 100
        if bb_position > 90:
            analysis_points.append(f"⚠️ **布林带**: 价格触及上轨({bb_position:.1f}%)，警惕回调")
        elif bb_position < 10:
            analysis_points.append(f"💚 **布林带**: 价格触及下轨({bb_position:.1f}%)，支撑较强")
        elif current_price > (bb_upper + bb_lower) / 2:
            analysis_points.append(f"📈 **布林带**: 价格在中轨上方")
        else:
            analysis_points.append(f"📉 **布林带**: 价格在中轨下方")
    
    if cci_val and abs(cci_val) > 100:
        if cci_val > 100:
            analysis_points.append(f"⚠️ **CCI**: {cci_val:.1f}，超买区域")
        else:
            analysis_points.append(f"💚 **CCI**: {cci_val:.1f}，超卖区域")
    
    if wr_val < 20:
        analysis_points.append(f"💚 **WR**: {wr_val:.1f}，超卖区域")
        signals.append("买入")
    elif wr_val > 80:
        analysis_points.append(f"⚠️ **WR**: {wr_val:.1f}，超买区域")
        signals.append("卖出")
    
    if roc_val > 10:
        analysis_points.append(f"📈 **ROC**: {roc_val:.1f}，上涨动力强劲")
    elif roc_val < -10:
        analysis_points.append(f"📉 **ROC**: {roc_val:.1f}，下跌动力强劲")
    
    if atr_val > 0:
        atr_percentage = (atr_val / current_price) * 100
        if atr_percentage > 3:
            analysis_points.append(f"📊 **波动率**: ATR={atr_val:.2f}({atr_percentage:.2f}%)，波动较大")
            risk_level = "高风险"
        elif atr_percentage > 1.5:
            analysis_points.append(f"📊 **波动率**: ATR={atr_val:.2f}({atr_percentage:.2f}%)，波动适中")
    
    if price_change > 20:
        analysis_points.append(f"🚀 **近30日涨幅**: {price_change:.1f}%，强势上涨")
    elif price_change < -20:
        analysis_points.append(f"📉 **近30日跌幅**: {abs(price_change):.1f}%，大幅下跌")
    
    return {
        'analysis_points': analysis_points,
        'signals': signals,
        'risk_level': risk_level,
        'summary': generate_summary(analysis_points, signals)
    }

def generate_summary(analysis_points, signals):
    positive = sum(1 for p in analysis_points if any(k in p for k in ['📈', '🟢', '💚', '🚀']))
    negative = sum(1 for p in analysis_points if any(k in p for k in ['📉', '🔴', '⚠️']))
    
    buy_signals = signals.count("买入")
    sell_signals = signals.count("卖出")
    
    if buy_signals >= sell_signals + 2:
        return "技术面整体向好，多项指标发出买入信号，建议关注回调机会入场。"
    elif sell_signals >= buy_signals + 2:
        return "技术面整体偏弱，多项指标发出卖出信号，建议谨慎操作或减仓。"
    elif buy_signals > sell_signals:
        return "技术面偏向多头，可适当参与但需控制仓位。"
    elif sell_signals > buy_signals:
        return "技术面偏向空头，建议保持观望。"
    else:
        return "技术面多空平衡，趋势不明朗，等待明确信号。"

def analyze_fundamental(metrics, stock_info):
    analysis_points = []
    
    pe_ratio = metrics['pe_ratio']
    pb_ratio = metrics['pb_ratio']
    pe_relative = metrics['pe_relative']
    pb_relative = metrics['pb_relative']
    
    if pe_relative < 0.7:
        analysis_points.append(f"💰 **PE估值**: {pe_ratio:.1f}倍(行业{metrics['industry_pe']:.1f}倍)，显著低估")
    elif pe_relative < 0.9:
        analysis_points.append(f"💰 **PE估值**: {pe_ratio:.1f}倍(行业{metrics['industry_pe']:.1f}倍)，略微低估")
    elif pe_relative > 1.3:
        analysis_points.append(f"⚠️ **PE估值**: {pe_ratio:.1f}倍(行业{metrics['industry_pe']:.1f}倍)，显著高估")
    elif pe_relative > 1.1:
        analysis_points.append(f"⚠️ **PE估值**: {pe_ratio:.1f}倍(行业{metrics['industry_pe']:.1f}倍)，略微高估")
    else:
        analysis_points.append(f"⚪ **PE估值**: {pe_ratio:.1f}倍(行业{metrics['industry_pe']:.1f}倍)，估值合理")
    
    if pb_relative < 0.7:
        analysis_points.append(f"💰 **PB估值**: {pb_ratio:.1f}倍(行业{metrics['industry_pb']:.1f}倍)，资产价值低估")
    elif pb_relative > 1.3:
        analysis_points.append(f"⚠️ **PB估值**: {pb_ratio:.1f}倍(行业{metrics['industry_pb']:.1f}倍)，资产价值高估")
    
    dividend_yield = metrics['dividend_yield']
    if dividend_yield > 4:
        analysis_points.append(f"💎 **股息率**: {dividend_yield:.1f}%，高股息，适合稳健投资者")
    elif dividend_yield > 2:
        analysis_points.append(f"💎 **股息率**: {dividend_yield:.1f}%，股息适中")
    else:
        analysis_points.append(f"💎 **股息率**: {dividend_yield:.1f}%，股息较低")
    
    roe = metrics['roe']
    industry_roe = metrics['industry_roe']
    if roe > industry_roe + 5:
        analysis_points.append(f"📊 **ROE**: {roe:.1f}%(行业{industry_roe:.1f}%)，盈利能力优秀")
    elif roe > industry_roe:
        analysis_points.append(f"📊 **ROE**: {roe:.1f}%(行业{industry_roe:.1f}%)，盈利能力良好")
    elif roe < industry_roe - 5:
        analysis_points.append(f"⚠️ **ROE**: {roe:.1f}%(行业{industry_roe:.1f}%)，盈利能力较弱")
    else:
        analysis_points.append(f"📊 **ROE**: {roe:.1f}%(行业{industry_roe:.1f}%)，盈利能力一般")
    
    revenue_growth = metrics['revenue_growth']
    profit_growth = metrics['net_profit_growth']
    
    if revenue_growth > 30:
        analysis_points.append(f"📈 **营收增长**: {revenue_growth:.1f}%，高速增长")
    elif revenue_growth > 15:
        analysis_points.append(f"📈 **营收增长**: {revenue_growth:.1f}%，稳健增长")
    elif revenue_growth > 0:
        analysis_points.append(f"📈 **营收增长**: {revenue_growth:.1f}%，小幅增长")
    else:
        analysis_points.append(f"📉 **营收增长**: {revenue_growth:.1f}%，负增长")
    
    if profit_growth > revenue_growth:
        analysis_points.append(f"✅ **净利润增长**: {profit_growth:.1f}%，盈利质量提升")
    elif profit_growth > 0:
        analysis_points.append(f"✅ **净利润增长**: {profit_growth:.1f}%")
    else:
        analysis_points.append(f"⚠️ **净利润增长**: {profit_growth:.1f}%，盈利下滑")
    
    debt_ratio = metrics['debt_ratio']
    if debt_ratio > 80:
        analysis_points.append(f"⚠️ **资产负债率**: {debt_ratio:.1f}%，负债较高")
    elif debt_ratio < 40:
        analysis_points.append(f"✅ **资产负债率**: {debt_ratio:.1f}%，财务稳健")
    
    current_ratio = metrics['current_ratio']
    if current_ratio < 1:
        analysis_points.append(f"⚠️ **流动比率**: {current_ratio:.1f}，短期偿债压力")
    elif current_ratio > 2:
        analysis_points.append(f"✅ **流动比率**: {current_ratio:.1f}，流动性充裕")
    
    return analysis_points

def generate_recommendation(technical, fundamental, metrics):
    score = 50
    
    buy_signals = technical['signals'].count("买入")
    sell_signals = technical['signals'].count("卖出")
    score += (buy_signals - sell_signals) * 10
    
    if technical['risk_level'] == '低风险':
        score += 10
    elif technical['risk_level'] == '高风险':
        score -= 10
    
    pe_relative = metrics['pe_relative']
    if pe_relative < 0.8:
        score += 15
    elif pe_relative > 1.2:
        score -= 15
    
    roe = metrics['roe']
    industry_roe = metrics['industry_roe']
    if roe > industry_roe + 5:
        score += 10
    elif roe < industry_roe - 5:
        score -= 10
    
    revenue_growth = metrics['revenue_growth']
    if revenue_growth > 20:
        score += 10
    elif revenue_growth < 0:
        score -= 10
    
    if score >= 80:
        return {'score': score, 'recommendation': '强烈推荐', 'level': 'A+', 'color': 'success'}
    elif score >= 70:
        return {'score': score, 'recommendation': '推荐买入', 'level': 'A', 'color': 'success'}
    elif score >= 60:
        return {'score': score, 'recommendation': '谨慎推荐', 'level': 'B+', 'color': 'info'}
    elif score >= 50:
        return {'score': score, 'recommendation': '中性观望', 'level': 'B', 'color': 'warning'}
    elif score >= 40:
        return {'score': score, 'recommendation': '谨慎持有', 'level': 'C+', 'color': 'warning'}
    else:
        return {'score': score, 'recommendation': '建议卖出', 'level': 'C', 'color': 'danger'}

def create_candlestick_chart(data, indicators, stock_name):
    fig = go.Figure()
    
    fig.add_trace(go.Candlestick(
        x=data['dates'],
        open=data['opens'],
        high=data['highs'],
        low=data['lows'],
        close=data['closes'],
        name='K线',
        increasing_line_color='#22c55e',
        decreasing_line_color='#ef4444',
        hovertemplate='<b>日期:</b> %{x}<br>' +
                      '<b>开盘:</b> ¥%{open:.2f}<br>' +
                      '<b>最高:</b> ¥%{high:.2f}<br>' +
                      '<b>最低:</b> ¥%{low:.2f}<br>' +
                      '<b>收盘:</b> ¥%{close:.2f}<br>' +
                      '<b>涨跌:</b> %{customdata[0]:+.2f} (%{customdata[1]:+.2f}%)<extra></extra>',
        customdata=[[(data['closes'][i] - data['opens'][i]), 
                     ((data['closes'][i] - data['opens'][i])/data['opens'][i]*100) 
                     if data['opens'][i] != 0 else 0] 
                    for i in range(len(data['closes']))]
    ))
    
    for ma_key, color in {'ma5': '#3b82f6', 'ma10': '#f59e0b', 'ma20': '#8b5cf6', 'ma60': '#22c55e'}.items():
        valid_data = [(d, v) for d, v in zip(data['dates'], indicators[ma_key]) if v is not None]
        if valid_data:
            fig.add_trace(go.Scatter(
                x=[x[0] for x in valid_data],
                y=[x[1] for x in valid_data],
                name=f'MA{ma_key[2:]}',
                line=dict(color=color, width=1.5),
                hovertemplate=f'<b>{ma_key.upper()}:</b> ¥%{{y:.2f}}<extra></extra>'
            ))
    
    valid_bb = [(d, u, l) for d, u, l in zip(data['dates'], indicators['bb_upper'], indicators['bb_lower']) if u and l]
    if valid_bb:
        fig.add_trace(go.Scatter(
            x=[x[0] for x in valid_bb],
            y=[x[1] for x in valid_bb],
            name='布林上轨',
            line=dict(color='#f59e0b', width=1, dash='dot'),
            opacity=0.5,
            hovertemplate='<b>布林上轨:</b> ¥%{y:.2f}<extra></extra>'
        ))
        fig.add_trace(go.Scatter(
            x=[x[0] for x in valid_bb],
            y=[x[2] for x in valid_bb],
            name='布林下轨',
            line=dict(color='#f59e0b', width=1, dash='dot'),
            opacity=0.5,
            fill='tonexty',
            fillcolor='rgba(245, 158, 11, 0.1)',
            hovertemplate='<b>布林下轨:</b> ¥%{y:.2f}<extra></extra>'
        ))
    
    fig.update_layout(
        title=f'{stock_name} K线图',
        xaxis_title='日期',
        yaxis_title='价格',
        height=500,
        template='plotly_white',
        xaxis_rangeslider_visible=False,
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='rgba(255, 255, 255, 0.95)',
            bordercolor='#3b82f6',
            borderwidth=1,
            font=dict(color='#1e3a5f', size=12)
        ),
        margin=dict(l=50, r=50, t=60, b=60)
    )
    
    fig.update_xaxes(
        showgrid=True,
        gridcolor='#e2e8f0',
        gridwidth=1,
        rangeslider=dict(visible=True, thickness=0.05),
        tickformat='%Y-%m-%d'
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridcolor='#e2e8f0',
        gridwidth=1
    )
    
    return fig

def create_indicator_chart(data, indicators, indicator_type):
    fig = go.Figure()
    
    if indicator_type == 'RSI':
        valid_data = [(d, v) for d, v in zip(data['dates'], indicators['rsi']) if v is not None]
        if valid_data:
            fig.add_trace(go.Scatter(
                x=[x[0] for x in valid_data], 
                y=[x[1] for x in valid_data], 
                name='RSI', 
                line=dict(color='#8b5cf6', width=2),
                hovertemplate='<b>日期:</b> %{x}<br><b>RSI:</b> %{y:.2f}<extra></extra>'
            ))
        fig.add_hline(y=70, line_dash="dash", line_color="#ef4444", annotation_text="超买", annotation_position="top left")
        fig.add_hline(y=30, line_dash="dash", line_color="#22c55e", annotation_text="超卖", annotation_position="bottom left")
        fig.update_layout(title='RSI相对强弱指标', yaxis_range=[0, 100], height=250, margin=dict(l=10, r=10, t=35, b=10))
    
    elif indicator_type == 'MACD':
        valid_macd = [(d, v) for d, v in zip(data['dates'], indicators['macd']) if v is not None]
        valid_signal = [(d, v) for d, v in zip(data['dates'], indicators['macd_signal']) if v is not None]
        valid_hist = [(d, v) for d, v in zip(data['dates'], indicators['macd_hist']) if v is not None]
        
        if valid_macd:
            fig.add_trace(go.Scatter(
                x=[x[0] for x in valid_macd], 
                y=[x[1] for x in valid_macd], 
                name='MACD', 
                line=dict(color='#3b82f6', width=2),
                hovertemplate='<b>日期:</b> %{x}<br><b>MACD:</b> %{y:.3f}<extra></extra>'
            ))
        if valid_signal:
            fig.add_trace(go.Scatter(
                x=[x[0] for x in valid_signal], 
                y=[x[1] for x in valid_signal], 
                name='Signal', 
                line=dict(color='#f59e0b', width=2),
                hovertemplate='<b>日期:</b> %{x}<br><b>Signal:</b> %{y:.3f}<extra></extra>'
            ))
        if valid_hist:
            colors = ['#22c55e' if x[1] >= 0 else '#ef4444' for x in valid_hist]
            fig.add_trace(go.Bar(
                x=[x[0] for x in valid_hist], 
                y=[x[1] for x in valid_hist], 
                name='Histogram', 
                marker_color=colors, 
                opacity=0.6,
                hovertemplate='<b>日期:</b> %{x}<br><b>柱状:</b> %{y:.3f}<extra></extra>'
            ))
        fig.add_hline(y=0, line_dash="dash", line_color="#6b7280")
        fig.update_layout(title='MACD指数平滑异同移动平均线', height=250, margin=dict(l=10, r=10, t=35, b=10))
    
    elif indicator_type == 'KDJ':
        valid_k = [(d, v) for d, v in zip(data['dates'], indicators['kdj_k']) if v is not None]
        valid_d = [(d, v) for d, v in zip(data['dates'], indicators['kdj_d']) if v is not None]
        valid_j = [(d, v) for d, v in zip(data['dates'], indicators['kdj_j']) if v is not None]
        
        if valid_k:
            fig.add_trace(go.Scatter(
                x=[x[0] for x in valid_k], 
                y=[x[1] for x in valid_k], 
                name='K', 
                line=dict(color='#3b82f6', width=2),
                hovertemplate='<b>日期:</b> %{x}<br><b>K:</b> %{y:.2f}<extra></extra>'
            ))
        if valid_d:
            fig.add_trace(go.Scatter(
                x=[x[0] for x in valid_d], 
                y=[x[1] for x in valid_d], 
                name='D', 
                line=dict(color='#f59e0b', width=2),
                hovertemplate='<b>日期:</b> %{x}<br><b>D:</b> %{y:.2f}<extra></extra>'
            ))
        if valid_j:
            fig.add_trace(go.Scatter(
                x=[x[0] for x in valid_j], 
                y=[x[1] for x in valid_j], 
                name='J', 
                line=dict(color='#8b5cf6', width=2),
                hovertemplate='<b>日期:</b> %{x}<br><b>J:</b> %{y:.2f}<extra></extra>'
            ))
        fig.add_hline(y=80, line_dash="dash", line_color="#ef4444", annotation_text="超买", annotation_position="top left")
        fig.add_hline(y=20, line_dash="dash", line_color="#22c55e", annotation_text="超卖", annotation_position="bottom left")
        fig.update_layout(title='KDJ随机指标', yaxis_range=[0, 120], height=250, margin=dict(l=10, r=10, t=35, b=10))
    
    elif indicator_type == 'OBV':
        valid_obv = [(d, v) for d, v in zip(data['dates'], indicators['obv']) if v is not None]
        if valid_obv:
            fig.add_trace(go.Scatter(
                x=[x[0] for x in valid_obv], 
                y=[x[1] for x in valid_obv], 
                name='OBV', 
                line=dict(color='#22c55e', width=2), 
                fill='tozeroy',
                hovertemplate='<b>日期:</b> %{x}<br><b>OBV:</b> %{y:,}<extra></extra>'
            ))
        fig.update_layout(title='OBV能量潮指标', height=250, margin=dict(l=10, r=10, t=35, b=10))
    
    elif indicator_type == 'CCI':
        valid_cci = [(d, v) for d, v in zip(data['dates'], indicators['cci']) if v is not None]
        if valid_cci:
            fig.add_trace(go.Scatter(
                x=[x[0] for x in valid_cci], 
                y=[x[1] for x in valid_cci], 
                name='CCI', 
                line=dict(color='#ec4899', width=2),
                hovertemplate='<b>日期:</b> %{x}<br><b>CCI:</b> %{y:.2f}<extra></extra>'
            ))
        fig.add_hline(y=100, line_dash="dash", line_color="#ef4444", annotation_text="超买", annotation_position="top left")
        fig.add_hline(y=-100, line_dash="dash", line_color="#22c55e", annotation_text="超卖", annotation_position="bottom left")
        fig.update_layout(title='CCI顺势指标', yaxis_range=[-200, 200], height=250, margin=dict(l=10, r=10, t=35, b=10))
    
    elif indicator_type == 'WR':
        valid_wr = [(d, v) for d, v in zip(data['dates'], indicators['wr']) if v is not None]
        if valid_wr:
            fig.add_trace(go.Scatter(
                x=[x[0] for x in valid_wr], 
                y=[x[1] for x in valid_wr], 
                name='WR', 
                line=dict(color='#f97316', width=2),
                hovertemplate='<b>日期:</b> %{x}<br><b>WR:</b> %{y:.2f}<extra></extra>'
            ))
        fig.add_hline(y=20, line_dash="dash", line_color="#ef4444", annotation_text="超买", annotation_position="top left")
        fig.add_hline(y=80, line_dash="dash", line_color="#22c55e", annotation_text="超卖", annotation_position="bottom left")
        fig.update_layout(title='WR威廉指标', yaxis_range=[0, 100], height=250, margin=dict(l=10, r=10, t=35, b=10))
    
    fig.update_layout(
        template='plotly_white',
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='rgba(255, 255, 255, 0.95)',
            bordercolor='#3b82f6',
            borderwidth=1,
            font=dict(color='#1e3a5f', size=11)
        ),
        xaxis=dict(tickformat='%Y-%m-%d'),
        showlegend=True
    )
    
    fig.update_xaxes(
        showgrid=True,
        gridcolor='#e2e8f0',
        gridwidth=1
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridcolor='#e2e8f0',
        gridwidth=1
    )
    
    return fig

def create_financial_ratio_chart(metrics, stock_info):
    industry_avg = INDUSTRY_AVERAGES.get(stock_info['industry'], {'pe': 20, 'pb': 2, 'dividend': 2, 'roe': 15, 'roa': 10})
    
    categories = ['PE', 'PB', '股息率(%)', 'ROE(%)', 'ROA(%)']
    stock_values = [metrics['pe_ratio'], metrics['pb_ratio'], metrics['dividend_yield'], metrics['roe'], metrics['roa']]
    industry_values = [industry_avg['pe'], industry_avg['pb'], industry_avg['dividend'], industry_avg['roe'], industry_avg['roa']]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name=stock_info.get('name', '股票'), x=categories, y=stock_values, marker_color='#3b82f6', marker_line_color='#2563eb', marker_line_width=1))
    fig.add_trace(go.Bar(name='行业平均', x=categories, y=industry_values, marker_color='#8b5cf6', marker_line_color='#7c3aed', marker_line_width=1))
    fig.update_layout(title='财务指标对比', barmode='group', height=320, template='plotly_white', margin=dict(l=0, r=0, t=40, b=0))
    
    return fig

def create_du_ponte_analysis(metrics):
    roe = metrics['roe']
    roa = metrics['roa']
    debt_ratio = metrics['debt_ratio']
    
    leverage = 1 / (1 - debt_ratio / 100) if debt_ratio < 100 else 1
    
    fig = go.Figure(go.Sunburst(
        labels=['ROE', 'ROA', '杠杆系数', '净利润率', '资产周转率'],
        parents=['', 'ROE', 'ROE', 'ROA', 'ROA'],
        values=[roe, roa, leverage * 10, 100, 100],
        branchvalues='total',
        marker=dict(colors=['#3b82f6', '#8b5cf6', '#f59e0b', '#22c55e', '#ec4899'])
    ))
    fig.update_layout(title='杜邦分析', height=380, margin=dict(l=0, r=0, t=40, b=0))
    
    return fig

def main():
    st.markdown("""
    <div class="main-header">
        <h1>🏦 专业金融分析平台</h1>
        <p>AI驱动的智能投资决策支持系统 | 专业版</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown('<div class="sidebar-section" style="padding: 10px 12px; margin: 5px 0;">', unsafe_allow_html=True)
        st.markdown("### 📊 股票选择")
        
        stock_name = st.selectbox("选择股票", list(STOCK_SYMBOLS.keys()), index=0, label_visibility="collapsed")
        stock_info = STOCK_SYMBOLS[stock_name]
        
        st.markdown(f"""
        <div style="font-size: 12px; color: #64748b; margin-top: 8px;">
        <strong>代码:</strong> {stock_info['symbol']} | <strong>行业:</strong> {stock_info['industry']} | <strong>市场:</strong> {stock_info['market']}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-section" style="padding: 10px 12px; margin: 5px 0;">', unsafe_allow_html=True)
        st.markdown("### 📅 分析周期")
        
        today = datetime.now()
        start_date = st.date_input("开始日期", datetime(today.year - 1, today.month, today.day), label_visibility="collapsed")
        end_date = st.date_input("结束日期", today, label_visibility="collapsed")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-section" style="padding: 10px 12px; margin: 5px 0;">', unsafe_allow_html=True)
        st.markdown("### 🔍 分析模块")
        
        analysis_modules = st.multiselect(
            "选择分析模块",
            ["技术分析", "基本面分析", "财务比率", "杜邦分析", "行业对比", "投资建议"],
            default=["技术分析", "基本面分析", "投资建议"],
            label_visibility="collapsed"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🚀 开始分析", use_container_width=True, type="primary"):
            base_price = 80 + list(STOCK_SYMBOLS.keys()).index(stock_name) * 15
            volatility = 0.015 + random.random() * 0.015
            
            data = generate_stock_data(start_date, end_date, base_price, volatility)
            indicators = calculate_indicators(data)
            metrics = calculate_fundamental_metrics(data, stock_info)
            
            st.session_state['stock_data'] = data
            st.session_state['indicators'] = indicators
            st.session_state['metrics'] = metrics
            st.session_state['stock_info'] = stock_info
            st.session_state['stock_name'] = stock_name
            st.session_state['analysis_modules'] = analysis_modules
    
    if 'stock_data' in st.session_state:
        data = st.session_state['stock_data']
        indicators = st.session_state['indicators']
        metrics = st.session_state['metrics']
        stock_info = st.session_state['stock_info']
        stock_name = st.session_state['stock_name']
        analysis_modules = st.session_state['analysis_modules']
        
        st.markdown("### 📈 关键指标概览")
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            st.metric("最新价格", f"¥{metrics['current_price']:.2f}", f"{metrics['daily_return']:+.2f}%")
        with col2:
            st.metric("市盈率", f"{metrics['pe_ratio']:.1f}倍")
        with col3:
            st.metric("市净率", f"{metrics['pb_ratio']:.1f}倍")
        with col4:
            st.metric("股息率", f"{metrics['dividend_yield']:.1f}%")
        with col5:
            st.metric("ROE", f"{metrics['roe']:.1f}%")
        with col6:
            st.metric("波动率", f"{metrics['volatility']:.1f}%")
        
        st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)
        
        if "技术分析" in analysis_modules:
            st.markdown("### 📊 技术分析")
            
            st.plotly_chart(create_candlestick_chart(data, indicators, stock_name), use_container_width=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.plotly_chart(create_indicator_chart(data, indicators, 'RSI'), use_container_width=True)
                st.plotly_chart(create_indicator_chart(data, indicators, 'KDJ'), use_container_width=True)
            with col2:
                st.plotly_chart(create_indicator_chart(data, indicators, 'MACD'), use_container_width=True)
                st.plotly_chart(create_indicator_chart(data, indicators, 'OBV'), use_container_width=True)
            with col3:
                st.plotly_chart(create_indicator_chart(data, indicators, 'CCI'), use_container_width=True)
                st.plotly_chart(create_indicator_chart(data, indicators, 'WR'), use_container_width=True)
            
            technical = analyze_technical(data, indicators)
            st.markdown("#### 📝 技术分析解读")
            for point in technical['analysis_points']:
                st.markdown(point)
            
            st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)
        
        if "基本面分析" in analysis_modules:
            st.markdown("### 💰 基本面分析")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 财务数据概览")
                st.markdown(f"""
                <div style="background: #f8fafc; padding: 15px; border-radius: 8px; border-left: 3px solid #3b82f6;">
                <table style="width: 100%; border-collapse: collapse;">
                <tr><td style="padding: 6px; border-bottom: 1px solid #e2e8f0;"><strong>每股收益(EPS)</strong></td><td style="padding: 6px; border-bottom: 1px solid #e2e8f0; text-align: right;">¥{metrics['eps']:.2f}</td></tr>
                <tr><td style="padding: 6px; border-bottom: 1px solid #e2e8f0;"><strong>营业收入增长率</strong></td><td style="padding: 6px; border-bottom: 1px solid #e2e8f0; text-align: right;">{metrics['revenue_growth']:.1f}%</td></tr>
                <tr><td style="padding: 6px; border-bottom: 1px solid #e2e8f0;"><strong>净利润增长率</strong></td><td style="padding: 6px; border-bottom: 1px solid #e2e8f0; text-align: right;">{metrics['net_profit_growth']:.1f}%</td></tr>
                <tr><td style="padding: 6px; border-bottom: 1px solid #e2e8f0;"><strong>资产负债率</strong></td><td style="padding: 6px; border-bottom: 1px solid #e2e8f0; text-align: right;">{metrics['debt_ratio']:.1f}%</td></tr>
                <tr><td style="padding: 6px; border-bottom: 1px solid #e2e8f0;"><strong>流动比率</strong></td><td style="padding: 6px; border-bottom: 1px solid #e2e8f0; text-align: right;">{metrics['current_ratio']:.2f}</td></tr>
                <tr><td style="padding: 6px;"><strong>存货周转率</strong></td><td style="padding: 6px; text-align: right;">{metrics['inventory_turnover']:.2f}</td></tr>
                </table>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("#### 增长趋势")
                fig = go.Figure()
                fig.add_trace(go.Bar(x=['营收增长', '净利润增长'], y=[metrics['revenue_growth'], metrics['net_profit_growth']], 
                                  marker_color=['#3b82f6', '#22c55e'], marker_line_color=['#2563eb', '#16a34a'], marker_line_width=1))
                fig.update_layout(height=220, template='plotly_white', margin=dict(l=0, r=0, t=30, b=0))
                st.plotly_chart(fig, use_container_width=True)
            
            fundamental = analyze_fundamental(metrics, stock_info)
            st.markdown("#### 📊 基本面分析解读")
            for point in fundamental:
                st.markdown(point)
            
            st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)
        
        if "财务比率" in analysis_modules:
            st.markdown("### 📈 财务比率分析")
            
            st.plotly_chart(create_financial_ratio_chart(metrics, stock_info), use_container_width=True)
            
            st.markdown("""
            <div class="info-box">
                <strong>财务比率解读:</strong>
                <ul>
                    <li><strong>PE(市盈率)</strong>: 衡量股价与盈利能力的关系，较低的PE通常表示估值较低</li>
                    <li><strong>PB(市净率)</strong>: 衡量股价与净资产的关系，反映资产价值</li>
                    <li><strong>股息率</strong>: 衡量分红回报水平，适合稳健型投资者</li>
                    <li><strong>ROE(净资产收益率)</strong>: 衡量股东权益回报率，反映盈利能力</li>
                    <li><strong>ROA(总资产收益率)</strong>: 衡量总资产利用效率</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)
        
        if "杜邦分析" in analysis_modules:
            st.markdown("### 🔬 杜邦分析")
            
            st.plotly_chart(create_du_ponte_analysis(metrics), use_container_width=True)
            
            roe = metrics['roe']
            roa = metrics['roa']
            debt_ratio = metrics['debt_ratio']
            leverage = 1 / (1 - debt_ratio / 100) if debt_ratio < 100 else 1
            
            st.markdown(f"""
            <div class="info-box">
                <strong>杜邦分解:</strong>
                <p><strong>ROE({roe:.1f}%) = ROA({roa:.1f}%) × 杠杆系数({leverage:.2f})</strong></p>
                <p>其中 ROA = 净利润率 × 资产周转率</p>
                <p>杠杆系数 = 1 / (1 - 资产负债率)</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)
        
        if "行业对比" in analysis_modules:
            st.markdown("### 🏢 行业对比分析")
            
            industry = stock_info['industry']
            peers = [k for k, v in STOCK_SYMBOLS.items() if v['industry'] == industry and k != stock_name]
            
            if peers:
                peer_data = []
                for peer in peers[:4]:
                    peer_info = STOCK_SYMBOLS[peer]
                    peer_data.append({
                        'name': peer,
                        'pe': peer_info['pe'],
                        'pb': peer_info['pb'],
                        'roe': peer_info['roe'],
                        'dividend': peer_info['dividend']
                    })
                
                fig = go.Figure()
                fig.add_trace(go.Bar(x=[p['name'] for p in peer_data], y=[p['pe'] for p in peer_data], name='PE', marker_color='#3b82f6'))
                fig.add_trace(go.Bar(x=[p['name'] for p in peer_data], y=[p['pb'] for p in peer_data], name='PB', marker_color='#8b5cf6'))
                fig.update_layout(title=f'{industry}行业PE/PB对比', barmode='group', height=320, template='plotly_white', margin=dict(l=0, r=0, t=40, b=0))
                st.plotly_chart(fig, use_container_width=True)
                
                fig2 = go.Figure()
                fig2.add_trace(go.Bar(x=[p['name'] for p in peer_data], y=[p['roe'] for p in peer_data], name='ROE', marker_color='#22c55e'))
                fig2.add_trace(go.Bar(x=[p['name'] for p in peer_data], y=[p['dividend'] for p in peer_data], name='股息率', marker_color='#f59e0b'))
                fig2.update_layout(title=f'{industry}行业ROE/股息率对比', barmode='group', height=320, template='plotly_white', margin=dict(l=0, r=0, t=40, b=0))
                st.plotly_chart(fig2, use_container_width=True)
            
            st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)
        
        if "投资建议" in analysis_modules:
            st.markdown("### 🎯 投资建议")
            
            technical = analyze_technical(data, indicators)
            fundamental = analyze_fundamental(metrics, stock_info)
            recommendation = generate_recommendation(technical, fundamental, metrics)
            
            color_map = {'success': '#22c55e', 'info': '#3b82f6', 'warning': '#f59e0b', 'danger': '#ef4444'}
            
            st.markdown(f"""
            <div style="background: {color_map[recommendation['color']]}; color: white; padding: 20px; border-radius: 12px; text-align: center; margin: 15px 0; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                <h2 style="margin: 0; font-size: 24px;">{recommendation['recommendation']}</h2>
                <h3 style="margin: 8px 0; font-size: 18px;">评级: {recommendation['level']}</h3>
                <p style="margin: 4px 0; font-size: 14px;">综合评分: {recommendation['score']}/100</p>
                <p style="margin: 4px 0; font-size: 14px;">风险等级: {technical['risk_level']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### 📋 投资策略建议")
            if recommendation['score'] >= 70:
                st.markdown("""
                <div class="success-box">
                <strong>积极策略:</strong>
                <ul>
                    <li>✅ 建议分批建仓，控制单次投入比例</li>
                    <li>✅ 设置止损位，控制下行风险</li>
                    <li>✅ 关注成交量变化，确认上涨动能</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
            elif recommendation['score'] >= 50:
                st.markdown("""
                <div class="info-box">
                <strong>中性策略:</strong>
                <ul>
                    <li>⚠️ 建议保持现有仓位，观察市场变化</li>
                    <li>⚠️ 可适当进行波段操作</li>
                    <li>⚠️ 关注关键支撑位和压力位</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="danger-box">
                <strong>保守策略:</strong>
                <ul>
                    <li>❌ 建议逐步减仓，降低风险敞口</li>
                    <li>❌ 等待更好的入场时机</li>
                    <li>❌ 关注基本面变化和市场环境</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("#### 📝 分析摘要")
            st.markdown(f"""
            <div class="info-box">
                <strong>技术面:</strong> {technical['summary']}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### ⚠️ 风险提示")
            st.markdown("""
            <div class="warning-box">
                <strong>重要提示:</strong>
                <ul>
                    <li>股票投资存在风险，历史表现不代表未来收益</li>
                    <li>本分析仅供参考，不构成投资建议</li>
                    <li>请根据自身风险承受能力做出投资决策</li>
                    <li>建议分散投资，控制单一股票仓位</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        st.markdown("""
        <div class="info-box">
            <h3>👋 欢迎使用专业金融分析平台</h3>
            <p>请在左侧选择股票和分析参数，然后点击"开始分析"按钮获取专业的投资分析报告。</p>
            <p><strong>专业功能:</strong></p>
            <ul>
                <li>📊 多维度技术分析（K线、均线、布林带、RSI、MACD、KDJ、OBV、CCI、WR）</li>
                <li>💰 深度基本面分析（估值、增长、财务健康）</li>
                <li>📈 财务比率分析（PE、PB、ROE、ROA等）</li>
                <li>🔬 杜邦分析（ROE分解）</li>
                <li>🏢 行业对比分析</li>
                <li>🎯 AI驱动的投资建议</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()