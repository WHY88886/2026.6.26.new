import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

# 设置页面配置
st.set_page_config(
    page_title="专业金融分析平台",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        color: white;
        text-align: center;
    }
    
    .metric-card {
        background: white;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    
    .positive-change {
        color: #00C853;
        font-weight: bold;
    }
    
    .negative-change {
        color: #FF5252;
        font-weight: bold;
    }
    
    .info-box {
        background: #E3F2FD;
        border-left: 4px solid #2196F3;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .warning-box {
        background: #FFF3E0;
        border-left: 4px solid #FF9800;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .success-box {
        background: #E8F5E9;
        border-left: 4px solid #4CAF50;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .danger-box {
        background: #FFEBEE;
        border-left: 4px solid #F44336;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .stPlotlyChart {
        border-radius: 10px;
        overflow: hidden;
    }
    
    .sidebar-section {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    h1, h2, h3 {
        color: #1a1a2e;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
</style>
""", unsafe_allow_html=True)

# 股票数据配置
STOCK_SYMBOLS = {
    '贵州茅台': {'symbol': '600519.SS', 'industry': '白酒', 'sector': '消费', 'market': 'A股', 'pe': 25.5, 'pb': 6.2, 'dividend': 2.8, 'eps': 48.5, 'revenue_growth': 18.2, 'net_profit_growth': 20.5},
    '五粮液': {'symbol': '000858.SZ', 'industry': '白酒', 'sector': '消费', 'market': 'A股', 'pe': 18.3, 'pb': 4.5, 'dividend': 2.5, 'eps': 6.8, 'revenue_growth': 15.3, 'net_profit_growth': 16.8},
    '招商银行': {'symbol': '600036.SS', 'industry': '银行', 'sector': '金融', 'market': 'A股', 'pe': 7.8, 'pb': 1.2, 'dividend': 4.5, 'eps': 5.2, 'revenue_growth': 8.5, 'net_profit_growth': 12.3},
    '中国平安': {'symbol': '601318.SS', 'industry': '保险', 'sector': '金融', 'market': 'A股', 'pe': 9.2, 'pb': 1.1, 'dividend': 3.2, 'eps': 4.8, 'revenue_growth': 6.2, 'net_profit_growth': 15.8},
    '比亚迪': {'symbol': '002594.SZ', 'industry': '新能源汽车', 'sector': '制造业', 'market': 'A股', 'pe': 85.6, 'pb': 8.9, 'dividend': 1.2, 'eps': 5.2, 'revenue_growth': 72.3, 'net_profit_growth': 128.5},
    '宁德时代': {'symbol': '300750.SZ', 'industry': '动力电池', 'sector': '制造业', 'market': 'A股', 'pe': 45.2, 'pb': 6.8, 'dividend': 1.5, 'eps': 8.5, 'revenue_growth': 48.5, 'net_profit_growth': 82.1},
    '腾讯控股': {'symbol': '00700.HK', 'industry': '互联网', 'sector': '科技', 'market': '港股', 'pe': 22.1, 'pb': 3.8, 'dividend': 1.8, 'eps': 12.5, 'revenue_growth': 10.5, 'net_profit_growth': 18.2},
    '阿里巴巴': {'symbol': 'BABA', 'industry': '互联网', 'sector': '科技', 'market': '美股', 'pe': 16.5, 'pb': 2.1, 'dividend': 0.8, 'eps': 5.8, 'revenue_growth': 8.3, 'net_profit_growth': 25.6},
    '苹果': {'symbol': 'AAPL', 'industry': '消费电子', 'sector': '科技', 'market': '美股', 'pe': 28.3, 'pb': 6.1, 'dividend': 0.6, 'eps': 6.1, 'revenue_growth': 2.5, 'net_profit_growth': 5.8},
    '特斯拉': {'symbol': 'TSLA', 'industry': '新能源汽车', 'sector': '制造业', 'market': '美股', 'pe': 72.4, 'pb': 12.3, 'dividend': 0.0, 'eps': 3.8, 'revenue_growth': 37.6, 'net_profit_growth': 105.3},
    '工商银行': {'symbol': '601398.SS', 'industry': '银行', 'sector': '金融', 'market': 'A股', 'pe': 5.8, 'pb': 0.7, 'dividend': 5.2, 'eps': 3.6, 'revenue_growth': 3.2, 'net_profit_growth': 5.8},
    '中国移动': {'symbol': '600941.SS', 'industry': '通信', 'sector': '科技', 'market': 'A股', 'pe': 12.5, 'pb': 1.6, 'dividend': 3.8, 'eps': 6.8, 'revenue_growth': 8.8, 'net_profit_growth': 12.5}
}

# 行业平均指标
INDUSTRY_AVERAGES = {
    '白酒': {'pe': 22.5, 'pb': 5.8, 'dividend': 2.6, 'volatility': 25.0},
    '银行': {'pe': 6.5, 'pb': 0.8, 'dividend': 4.8, 'volatility': 18.0},
    '保险': {'pe': 10.2, 'pb': 1.3, 'dividend': 3.5, 'volatility': 22.0},
    '新能源汽车': {'pe': 45.0, 'pb': 6.5, 'dividend': 1.0, 'volatility': 35.0},
    '动力电池': {'pe': 38.0, 'pb': 5.2, 'dividend': 1.2, 'volatility': 32.0},
    '互联网': {'pe': 25.0, 'pb': 3.5, 'dividend': 1.5, 'volatility': 28.0},
    '消费电子': {'pe': 30.0, 'pb': 5.0, 'dividend': 0.8, 'volatility': 26.0},
    '通信': {'pe': 15.0, 'pb': 1.5, 'dividend': 3.0, 'volatility': 20.0}
}

def generate_professional_stock_data(start_date, end_date, base_price=100, volatility=0.02):
    """生成专业的股票模拟数据"""
    dates = []
    opens = []
    highs = []
    lows = []
    closes = []
    volumes = []
    
    current_date = start_date
    current_price = base_price
    
    while current_date <= end_date:
        if current_date.weekday() < 5:  # 工作日
            # 使用几何布朗运动模拟价格
            drift = 0.0005  # 每日预期收益率
            shock = random.gauss(0, volatility)
            price_change = drift + shock
            current_price = current_price * (1 + price_change)
            current_price = max(current_price, 10)  # 确保价格不低于10
            
            # 生成OHLC数据
            open_price = current_price * (1 + random.uniform(-0.01, 0.01))
            high_price = max(current_price, open_price) * (1 + random.uniform(0, 0.02))
            low_price = min(current_price, open_price) * (1 - random.uniform(0, 0.02))
            
            # 生成成交量（与价格变化相关）
            base_volume = random.randint(5000000, 15000000)
            volume_multiplier = 1 + abs(price_change) * 10  # 价格变化越大，成交量越大
            volume = int(base_volume * volume_multiplier)
            
            dates.append(current_date)
            opens.append(open_price)
            highs.append(high_price)
            lows.append(low_price)
            closes.append(current_price)
            volumes.append(volume)
        
        current_date += timedelta(days=1)
    
    return {
        'dates': dates,
        'opens': opens,
        'highs': highs,
        'lows': lows,
        'closes': closes,
        'volumes': volumes
    }

def calculate_advanced_indicators(data):
    """计算高级技术指标"""
    closes = data['closes']
    highs = data['highs']
    lows = data['lows']
    volumes = data['volumes']
    dates = data['dates']
    
    # 移动平均线
    ma5 = []
    ma10 = []
    ma20 = []
    ma60 = []
    
    # 布林带
    bb_upper = []
    bb_middle = []
    bb_lower = []
    
    # RSI
    rsi = []
    
    # MACD
    macd = []
    macd_signal = []
    macd_hist = []
    
    # KDJ
    kdj_k = []
    kdj_d = []
    kdj_j = []
    
    # ATR (平均真实波幅)
    atr = []
    
    # OBV (能量潮)
    obv = []
    
    for i in range(len(closes)):
        # 移动平均线
        if i >= 4:
            ma5.append(sum(closes[i-4:i+1]) / 5)
        else:
            ma5.append(None)
        
        if i >= 9:
            ma10.append(sum(closes[i-9:i+1]) / 10)
        else:
            ma10.append(None)
        
        if i >= 19:
            ma20.append(sum(closes[i-19:i+1]) / 20)
        else:
            ma20.append(None)
        
        if i >= 59:
            ma60.append(sum(closes[i-59:i+1]) / 60)
        else:
            ma60.append(None)
        
        # 布林带
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
        
        # RSI
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
            rs = avg_gain / avg_loss
            rsi_val = 100 - (100 / (1 + rs))
            rsi.append(rsi_val)
        else:
            rsi.append(None)
        
        # MACD
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
        
        if macd_val is not None and signal_val is not None:
            macd_hist.append(macd_val - signal_val)
        else:
            macd_hist.append(None)
        
        # KDJ
        if i >= 8:
            period_highs = highs[i-8:i+1]
            period_lows = lows[i-8:i+1]
            period_closes = closes[i-8:i+1]
            
            highest_high = max(period_highs)
            lowest_low = min(period_lows)
            
            if highest_high != lowest_low:
                rsv = (closes[i] - lowest_low) / (highest_high - lowest_low) * 100
            else:
                rsv = 50
            
            k_val = (2/3) * (kdj_k[-1] if kdj_k and kdj_k[-1] is not None else 50) + (1/3) * rsv
            d_val = (2/3) * (kdj_d[-1] if kdj_d and kdj_d[-1] is not None else 50) + (1/3) * k_val
            j_val = 3 * k_val - 2 * d_val
            
            kdj_k.append(k_val)
            kdj_d.append(d_val)
            kdj_j.append(j_val)
        else:
            kdj_k.append(None)
            kdj_d.append(None)
            kdj_j.append(None)
        
        # ATR
        if i >= 13:
            tr_values = []
            for j in range(i-13, i+1):
                if j > 0:
                    tr = max(highs[j] - lows[j], 
                             abs(highs[j] - closes[j-1]), 
                             abs(lows[j] - closes[j-1]))
                else:
                    tr = highs[j] - lows[j]
                tr_values.append(tr)
            atr.append(sum(tr_values) / 14)
        else:
            atr.append(None)
        
        # OBV
        if i == 0:
            obv.append(volumes[i])
        else:
            if closes[i] > closes[i-1]:
                obv.append(obv[-1] + volumes[i])
            elif closes[i] < closes[i-1]:
                obv.append(obv[-1] - volumes[i])
            else:
                obv.append(obv[-1])
    
    return {
        'dates': dates,
        'ma5': ma5,
        'ma10': ma10,
        'ma20': ma20,
        'ma60': ma60,
        'bb_upper': bb_upper,
        'bb_middle': bb_middle,
        'bb_lower': bb_lower,
        'rsi': rsi,
        'macd': macd,
        'macd_signal': macd_signal,
        'macd_hist': macd_hist,
        'kdj_k': kdj_k,
        'kdj_d': kdj_d,
        'kdj_j': kdj_j,
        'atr': atr,
        'obv': obv
    }

def calculate_fundamental_metrics(data, stock_info):
    """计算基本面指标"""
    closes = data['closes']
    volumes = data['volumes']
    
    # 基本财务指标
    current_price = closes[-1] if closes else 0
    market_cap = current_price * 1000000000  # 假设总股本10亿股
    
    # 计算收益率
    if len(closes) >= 2:
        daily_return = (closes[-1] - closes[-2]) / closes[-2] * 100
    else:
        daily_return = 0
    
    if len(closes) >= 20:
        monthly_return = (closes[-1] - closes[-20]) / closes[-20] * 100
    else:
        monthly_return = 0
    
    if len(closes) >= 60:
        quarterly_return = (closes[-1] - closes[-60]) / closes[-60] * 100
    else:
        quarterly_return = 0
    
    # 计算波动率
    if len(closes) >= 20:
        returns = [(closes[i] - closes[i-1]) / closes[i-1] for i in range(1, len(closes))]
        volatility = (sum([(r - sum(returns)/len(returns))**2 for r in returns[-20:]]) / 20) ** 0.5 * 100
    else:
        volatility = 0
    
    # 计算平均成交量
    avg_volume = sum(volumes[-20:]) / 20 if len(volumes) >= 20 else 0
    
    # 计算换手率
    turnover_rate = (volumes[-1] / 1000000000) * 100 if volumes else 0
    
    # 计算市盈率相对行业水平
    industry_avg = INDUSTRY_AVERAGES.get(stock_info['industry'], {'pe': 20, 'pb': 2, 'dividend': 2})
    pe_ratio = stock_info['pe']
    pb_ratio = stock_info['pb']
    
    pe_relative = pe_ratio / industry_avg['pe'] if industry_avg['pe'] > 0 else 1
    pb_relative = pb_ratio / industry_avg['pb'] if industry_avg['pb'] > 0 else 1
    
    return {
        'current_price': current_price,
        'market_cap': market_cap,
        'daily_return': daily_return,
        'monthly_return': monthly_return,
        'quarterly_return': quarterly_return,
        'volatility': volatility,
        'avg_volume': avg_volume,
        'turnover_rate': turnover_rate,
        'pe_ratio': pe_ratio,
        'pb_ratio': pb_ratio,
        'dividend_yield': stock_info['dividend'],
        'pe_relative': pe_relative,
        'pb_relative': pb_relative,
        'industry_pe': industry_avg['pe'],
        'industry_pb': industry_avg['pb']
    }

def professional_technical_analysis(data, indicators):
    """专业的技术分析"""
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
    
    analysis_points = []
    signals = []
    risk_level = "中等"
    
    # 均线分析
    if ma5_val > ma10_val > ma20_val > ma60_val:
        analysis_points.append("📈 **均线系统**: 多头排列，短期、中期、长期均线均呈上升趋势，技术面强势")
        signals.append("买入信号")
    elif ma5_val < ma10_val < ma20_val < ma60_val:
        analysis_points.append("📉 **均线系统**: 空头排列，各均线呈下降趋势，技术面弱势")
        signals.append("卖出信号")
    else:
        analysis_points.append("🔄 **均线系统**: 均线交织，趋势不明朗，建议观望")
        signals.append("观望")
    
    # RSI分析
    if rsi_val > 80:
        analysis_points.append(f"⚠️ **RSI指标**: {rsi_val:.1f}，处于极度超买区域，短期回调风险极高")
        risk_level = "高风险"
    elif rsi_val > 70:
        analysis_points.append(f"🔴 **RSI指标**: {rsi_val:.1f}，处于超买区域，可能面临短期调整")
        risk_level = "中高风险"
    elif rsi_val < 20:
        analysis_points.append(f"💚 **RSI指标**: {rsi_val:.1f}，处于极度超卖区域，存在反弹机会")
        risk_level = "低风险"
    elif rsi_val < 30:
        analysis_points.append(f"🟢 **RSI指标**: {rsi_val:.1f}，处于超卖区域，可能存在买入机会")
        risk_level = "中低风险"
    else:
        analysis_points.append(f"⚪ **RSI指标**: {rsi_val:.1f}，处于正常区间，无明显超买超卖信号")
    
    # KDJ分析
    if kdj_k > 80 and kdj_d > 80:
        analysis_points.append(f"🔴 **KDJ指标**: K={kdj_k:.1f}, D={kdj_d:.1f}, J={kdj_j:.1f}，高位死叉风险，注意回调")
    elif kdj_k < 20 and kdj_d < 20:
        analysis_points.append(f"🟢 **KDJ指标**: K={kdj_k:.1f}, D={kdj_d:.1f}, J={kdj_j:.1f}，低位金叉机会，关注反弹")
    elif kdj_k > kdj_d:
        analysis_points.append(f"📈 **KDJ指标**: K线上穿D线，形成金叉，短期看涨")
    else:
        analysis_points.append(f"📉 **KDJ指标**: K线下穿D线，形成死叉，短期看跌")
    
    # MACD分析
    if macd_val > macd_signal and macd_val > 0:
        analysis_points.append(f"🟢 **MACD指标**: DIF={macd_val:.3f}, DEA={macd_signal:.3f}，金叉且在零轴上方，强势上涨")
    elif macd_val > macd_signal and macd_val < 0:
        analysis_points.append(f"🟡 **MACD指标**: DIF={macd_val:.3f}, DEA={macd_signal:.3f}，金叉但在零轴下方，弱势反弹")
    elif macd_val < macd_signal and macd_val > 0:
        analysis_points.append(f"🔴 **MACD指标**: DIF={macd_val:.3f}, DEA={macd_signal:.3f}，死叉但在零轴上方，强势调整")
    else:
        analysis_points.append(f"🔴 **MACD指标**: DIF={macd_val:.3f}, DEA={macd_signal:.3f}，死叉且在零轴下方，弱势下跌")
    
    # 布林带分析
    current_price = data['closes'][-1]
    bb_upper = indicators['bb_upper'][-1]
    bb_lower = indicators['bb_lower'][-1]
    bb_middle = indicators['bb_middle'][-1]
    
    if bb_upper and bb_lower and bb_middle:
        bb_position = (current_price - bb_lower) / (bb_upper - bb_lower) * 100
        if bb_position > 90:
            analysis_points.append(f"⚠️ **布林带**: 价格位于上轨附近({bb_position:.1f}%)，突破风险较大")
        elif bb_position < 10:
            analysis_points.append(f"💚 **布林带**: 价格位于下轨附近({bb_position:.1f}%)，支撑较强")
        elif current_price > bb_middle:
            analysis_points.append(f"📈 **布林带**: 价格位于中轨上方，趋势向上")
        else:
            analysis_points.append(f"📉 **布林带**: 价格位于中轨下方，趋势向下")
    
    # ATR分析
    if atr_val > 0:
        atr_percentage = (atr_val / current_price) * 100
        if atr_percentage > 3:
            analysis_points.append(f"📊 **波动率**: ATR={atr_val:.2f}({atr_percentage:.2f}%)，波动较大，注意风险控制")
        elif atr_percentage > 1.5:
            analysis_points.append(f"📊 **波动率**: ATR={atr_val:.2f}({atr_percentage:.2f}%)，波动适中")
        else:
            analysis_points.append(f"📊 **波动率**: ATR={atr_val:.2f}({atr_percentage:.2f}%)，波动较小")
    
    # 价格表现分析
    if price_change > 20:
        analysis_points.append(f"🚀 **价格表现**: 近30日涨幅{price_change:.1f}%，表现极为强势，但需注意回调风险")
    elif price_change > 10:
        analysis_points.append(f"📈 **价格表现**: 近30日涨幅{price_change:.1f}%，表现强势")
    elif price_change < -20:
        analysis_points.append(f"📉 **价格表现**: 近30日跌幅{abs(price_change):.1f}%，表现极为弱势")
    elif price_change < -10:
        analysis_points.append(f"📉 **价格表现**: 近30日跌幅{abs(price_change):.1f}%，表现弱势")
    else:
        analysis_points.append(f"➡️ **价格表现**: 近30日涨跌{price_change:.1f}%，表现平稳")
    
    return {
        'analysis_points': analysis_points,
        'signals': signals,
        'risk_level': risk_level,
        'summary': generate_analysis_summary(analysis_points, risk_level)
    }

def generate_analysis_summary(analysis_points, risk_level):
    """生成分析摘要"""
    positive_signals = sum(1 for point in analysis_points if any(keyword in point for keyword in ['📈', '🟢', '💚', '🚀']))
    negative_signals = sum(1 for point in analysis_points if any(keyword in point for keyword in ['📉', '🔴', '⚠️']))
    
    if positive_signals > negative_signals + 2:
        return "综合技术面分析显示，该股票目前处于强势上涨阶段，多项技术指标发出买入信号。建议投资者关注回调机会，逢低布局。"
    elif negative_signals > positive_signals + 2:
        return "综合技术面分析显示，该股票目前处于弱势调整阶段，多项技术指标发出卖出信号。建议投资者谨慎操作，控制仓位。"
    elif positive_signals > negative_signals:
        return "综合技术面分析显示，该股票目前走势相对乐观，技术面偏向多头。建议投资者可适当参与，注意风险控制。"
    elif negative_signals > positive_signals:
        return "综合技术面分析显示，该股票目前走势相对谨慎，技术面偏向空头。建议投资者保持观望，等待更好的入场时机。"
    else:
        return "综合技术面分析显示，该股票目前多空信号相对平衡，趋势不甚明朗。建议投资者保持耐心，等待更明确的方向信号。"

def professional_fundamental_analysis(metrics, stock_info):
    """专业的基本面分析"""
    analysis_points = []
    
    # 估值分析
    pe_ratio = metrics['pe_ratio']
    pb_ratio = metrics['pb_ratio']
    pe_relative = metrics['pe_relative']
    pb_relative = metrics['pb_relative']
    
    if pe_relative < 0.8:
        analysis_points.append(f"💰 **估值水平**: PE={pe_ratio:.1f}倍，相对行业平均{metrics['industry_pe']:.1f}倍偏低{abs(1-pe_relative)*100:.0f}%，估值具有吸引力")
    elif pe_relative > 1.2:
        analysis_points.append(f"⚠️ **估值水平**: PE={pe_ratio:.1f}倍，相对行业平均{metrics['industry_pe']:.1f}倍偏高{(pe_relative-1)*100:.0f}%，估值偏高")
    else:
        analysis_points.append(f"⚪ **估值水平**: PE={pe_ratio:.1f}倍，与行业平均{metrics['industry_pe']:.1f}倍相当，估值合理")
    
    if pb_relative < 0.8:
        analysis_points.append(f"💰 **估值水平**: PB={pb_ratio:.1f}倍，相对行业平均{metrics['industry_pb']:.1f}倍偏低，资产价值被低估")
    elif pb_relative > 1.2:
        analysis_points.append(f"⚠️ **估值水平**: PB={pb_ratio:.1f}倍，相对行业平均{metrics['industry_pb']:.1f}倍偏高，资产价值被高估")
    
    # 股息率分析
    dividend_yield = metrics['dividend_yield']
    if dividend_yield > 4:
        analysis_points.append(f"💎 **股息收益**: 股息率{dividend_yield:.1f}%，收益较高，适合稳健型投资者")
    elif dividend_yield > 2:
        analysis_points.append(f"💎 **股息收益**: 股息率{dividend_yield:.1f}%，收益适中，具有一定的投资价值")
    elif dividend_yield > 0:
        analysis_points.append(f"💎 **股息收益**: 股息率{dividend_yield:.1f}%，收益较低，主要关注资本增值")
    else:
        analysis_points.append(f"💎 **股息收益**: 暂无分红，公司可能处于成长期，注重业务发展")
    
    # 市值分析
    market_cap = metrics['market_cap']
    if market_cap > 1000000000000:  # 超过1万亿
        analysis_points.append(f"🏢 **市值规模**: {market_cap/1000000000000:.1f}万亿，大盘蓝筹股，稳定性强")
    elif market_cap > 100000000000:  # 超过1000亿
        analysis_points.append(f"🏢 **市值规模**: {market_cap/100000000000:.1f}千亿，中盘股，成长性与稳定性兼备")
    else:
        analysis_points.append(f"🏢 **市值规模**: {market_cap/100000000:.1f}亿，小盘股，成长潜力大但波动性高")
    
    # 流动性分析
    turnover_rate = metrics['turnover_rate']
    if turnover_rate > 10:
        analysis_points.append(f"📊 **流动性**: 换手率{turnover_rate:.1f}%，交投活跃，流动性好")
    elif turnover_rate > 5:
        analysis_points.append(f"📊 **流动性**: 换手率{turnover_rate:.1f}%，交投适中，流动性良好")
    else:
        analysis_points.append(f"📊 **流动性**: 换手率{turnover_rate:.1f}%，交投相对清淡，需关注流动性风险")
    
    # 波动性分析
    volatility = metrics['volatility']
    if volatility > 30:
        analysis_points.append(f"📈 **波动性**: 年化波动率{volatility:.1f}%，波动较大，适合风险承受能力强的投资者")
    elif volatility > 20:
        analysis_points.append(f"📈 **波动性**: 年化波动率{volatility:.1f}%，波动适中，风险收益平衡")
    else:
        analysis_points.append(f"📈 **波动性**: 年化波动率{volatility:.1f}%，波动较小，相对稳健")
    
    return analysis_points

def generate_professional_recommendation(technical_analysis, fundamental_analysis, metrics):
    """生成专业投资建议"""
    score = 50
    
    # 技术面评分
    tech_signals = technical_analysis['signals']
    if '买入信号' in tech_signals:
        score += 20
    elif '卖出信号' in tech_signals:
        score -= 20
    
    # 风险调整
    risk_level = technical_analysis['risk_level']
    if risk_level == '低风险':
        score += 10
    elif risk_level == '高风险':
        score -= 10
    
    # 基本面评分
    pe_relative = metrics['pe_relative']
    if pe_relative < 0.8:
        score += 15
    elif pe_relative > 1.2:
        score -= 15
    
    dividend_yield = metrics['dividend_yield']
    if dividend_yield > 3:
        score += 10
    elif dividend_yield > 1:
        score += 5
    
    # 波动性调整
    volatility = metrics['volatility']
    if volatility < 20:
        score += 5
    elif volatility > 30:
        score -= 5
    
    # 确定推荐等级
    if score >= 80:
        recommendation = "强烈推荐"
        level = "A+"
        color = "success"
    elif score >= 70:
        recommendation = "推荐买入"
        level = "A"
        color = "success"
    elif score >= 60:
        recommendation = "谨慎推荐"
        level = "B+"
        color = "info"
    elif score >= 50:
        recommendation = "中性观望"
        level = "B"
        color = "warning"
    elif score >= 40:
        recommendation = "谨慎持有"
        level = "C+"
        color = "warning"
    else:
        recommendation = "建议卖出"
        level = "C"
        color = "danger"
    
    # 投资策略建议
    strategies = []
    if score >= 70:
        strategies.append("建议分批建仓，控制单次投入比例")
        strategies.append("设置止损位，控制下行风险")
        if dividend_yield > 2:
            strategies.append("适合长期持有，享受股息收益")
    elif score >= 50:
        strategies.append("建议保持现有仓位，观察市场变化")
        strategies.append("可适当进行波段操作")
    else:
        strategies.append("建议逐步减仓，降低风险敞口")
        strategies.append("等待更好的入场时机")
    
    return {
        'score': score,
        'recommendation': recommendation,
        'level': level,
        'color': color,
        'strategies': strategies,
        'risk_assessment': risk_level,
        'investment_horizon': '长期' if score >= 60 else '短期' if score < 40 else '中期'
    }

def create_candlestick_chart(data, indicators, stock_name):
    """创建专业的K线图"""
    fig = go.Figure()
    
    # K线图
    fig.add_trace(go.Candlestick(
        x=data['dates'],
        open=data['opens'],
        high=data['highs'],
        low=data['lows'],
        close=data['closes'],
        name='K线',
        increasing_line_color='#00C853',
        decreasing_line_color='#FF5252'
    ))
    
    # 移动平均线
    colors = {'ma5': '#2196F3', 'ma10': '#FF9800', 'ma20': '#9C27B0', 'ma60': '#4CAF50'}
    labels = {'ma5': 'MA5', 'ma10': 'MA10', 'ma20': 'MA20', 'ma60': 'MA60'}
    
    for ma_key, color in colors.items():
        valid_data = [(d, v) for d, v in zip(data['dates'], indicators[ma_key]) if v is not None]
        if valid_data:
            fig.add_trace(go.Scatter(
                x=[x[0] for x in valid_data],
                y=[x[1] for x in valid_data],
                name=labels[ma_key],
                line=dict(color=color, width=1.5),
                opacity=0.8
            ))
    
    # 布林带
    valid_bb_upper = [(d, v) for d, v in zip(data['dates'], indicators['bb_upper']) if v is not None]
    valid_bb_lower = [(d, v) for d, v in zip(data['dates'], indicators['bb_lower']) if v is not None]
    
    if valid_bb_upper and valid_bb_lower:
        fig.add_trace(go.Scatter(
            x=[x[0] for x in valid_bb_upper],
            y=[x[1] for x in valid_bb_upper],
            name='布林上轨',
            line=dict(color='#FF9800', width=1, dash='dot'),
            opacity=0.5
        ))
        fig.add_trace(go.Scatter(
            x=[x[0] for x in valid_bb_lower],
            y=[x[1] for x in valid_bb_lower],
            name='布林下轨',
            line=dict(color='#FF9800', width=1, dash='dot'),
            opacity=0.5,
            fill='tonexty',
            fillcolor='rgba(255, 152, 0, 0.1)'
        ))
    
    fig.update_layout(
        title=f'{stock_name} 技术分析图表',
        xaxis_title='日期',
        yaxis_title='价格',
        height=600,
        template='plotly_white',
        xaxis_rangeslider_visible=False,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_indicator_chart(data, indicators, indicator_type, stock_name):
    """创建技术指标图表"""
    fig = go.Figure()
    
    if indicator_type == 'RSI':
        valid_data = [(d, v) for d, v in zip(data['dates'], indicators['rsi']) if v is not None]
        if valid_data:
            fig.add_trace(go.Scatter(
                x=[x[0] for x in valid_data],
                y=[x[1] for x in valid_data],
                name='RSI',
                line=dict(color='#9C27B0', width=2)
            ))
        
        fig.add_hline(y=70, line_dash="dash", line_color="#FF5252", annotation_text="超买区")
        fig.add_hline(y=30, line_dash="dash", line_color="#00C853", annotation_text="超卖区")
        fig.update_layout(title='RSI相对强弱指标', yaxis_range=[0, 100], height=300)
    
    elif indicator_type == 'MACD':
        valid_macd = [(d, v) for d, v in zip(data['dates'], indicators['macd']) if v is not None]
        valid_signal = [(d, v) for d, v in zip(data['dates'], indicators['macd_signal']) if v is not None]
        valid_hist = [(d, v) for d, v in zip(data['dates'], indicators['macd_hist']) if v is not None]
        
        if valid_macd:
            fig.add_trace(go.Scatter(
                x=[x[0] for x in valid_macd],
                y=[x[1] for x in valid_macd],
                name='MACD',
                line=dict(color='#2196F3', width=2)
            ))
        
        if valid_signal:
            fig.add_trace(go.Scatter(
                x=[x[0] for x in valid_signal],
                y=[x[1] for x in valid_signal],
                name='Signal',
                line=dict(color='#FF9800', width=2)
            ))
        
        if valid_hist:
            colors = ['#00C853' if x[1] >= 0 else '#FF5252' for x in valid_hist]
            fig.add_trace(go.Bar(
                x=[x[0] for x in valid_hist],
                y=[x[1] for x in valid_hist],
                name='Histogram',
                marker_color=colors,
                opacity=0.6
            ))
        
        fig.update_layout(title='MACD指标', height=300)
    
    elif indicator_type == 'KDJ':
        valid_k = [(d, v) for d, v in zip(data['dates'], indicators['kdj_k']) if v is not None]
        valid_d = [(d, v) for d, v in zip(data['dates'], indicators['kdj_d']) if v is not None]
        valid_j = [(d, v) for d, v in zip(data['dates'], indicators['kdj_j']) if v is not None]
        
        if valid_k:
            fig.add_trace(go.Scatter(
                x=[x[0] for x in valid_k],
                y=[x[1] for x in valid_k],
                name='K',
                line=dict(color='#2196F3', width=2)
            ))
        
        if valid_d:
            fig.add_trace(go.Scatter(
                x=[x[0] for x in valid_d],
                y=[x[1] for x in valid_d],
                name='D',
                line=dict(color='#FF9800', width=2)
            ))
        
        if valid_j:
            fig.add_trace(go.Scatter(
                x=[x[0] for x in valid_j],
                y=[x[1] for x in valid_j],
                name='J',
                line=dict(color='#9C27B0', width=2)
            ))
        
        fig.add_hline(y=80, line_dash="dash", line_color="#FF5252", annotation_text="超买")
        fig.add_hline(y=20, line_dash="dash", line_color="#00C853", annotation_text="超卖")
        fig.update_layout(title='KDJ随机指标', yaxis_range=[0, 120], height=300)
    
    elif indicator_type == 'OBV':
        valid_obv = [(d, v) for d, v in zip(data['dates'], indicators['obv']) if v is not None]
        if valid_obv:
            fig.add_trace(go.Scatter(
                x=[x[0] for x in valid_obv],
                y=[x[1] for x in valid_obv],
                name='OBV',
                line=dict(color='#4CAF50', width=2),
                fill='tozeroy'
            ))
        
        fig.update_layout(title='OBV能量潮指标', height=300)
    
    fig.update_layout(template='plotly_white')
    return fig

def create_industry_comparison_chart(stock_info, metrics):
    """创建行业对比图表"""
    industry = stock_info['industry']
    industry_avg = INDUSTRY_AVERAGES.get(industry, {'pe': 20, 'pb': 2, 'dividend': 2, 'volatility': 25})
    
    fig = go.Figure()
    
    categories = ['市盈率(PE)', '市净率(PB)', '股息率(%)', '波动率(%)']
    stock_values = [metrics['pe_ratio'], metrics['pb_ratio'], metrics['dividend_yield'], metrics['volatility']]
    industry_values = [industry_avg['pe'], industry_avg['pb'], industry_avg['dividend'], industry_avg['volatility']]
    
    fig.add_trace(go.Bar(
        name=stock_info['name'],
        x=categories,
        y=stock_values,
        marker_color='#667eea'
    ))
    
    fig.add_trace(go.Bar(
        name='行业平均',
        x=categories,
        y=industry_values,
        marker_color='#764ba2'
    ))
    
    fig.update_layout(
        title=f'{stock_info["name"]} vs {industry}行业平均',
        barmode='group',
        height=400,
        template='plotly_white'
    )
    
    return fig

def main():
    # 主标题
    st.markdown("""
    <div class="main-header">
        <h1>🏦 专业金融分析平台</h1>
        <p>AI驱动的智能投资决策支持系统</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 侧边栏
    with st.sidebar:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.header("📊 股票选择")
        
        stock_name = st.selectbox("选择股票", list(STOCK_SYMBOLS.keys()), index=0)
        stock_info = STOCK_SYMBOLS[stock_name]
        symbol = stock_info['symbol']
        
        st.markdown(f"""
        **股票代码**: {symbol}  
        **所属行业**: {stock_info['industry']}  
        **所属板块**: {stock_info['sector']}  
        **交易市场**: {stock_info['market']}
        """)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.header("📅 分析周期")
        
        today = datetime.now()
        default_start = datetime(today.year - 1, today.month, today.day)
        
        start_date = st.date_input("开始日期", default_start)
        end_date = st.date_input("结束日期", today)
        
        analysis_type = st.radio(
            "分析类型",
            ["综合分析", "技术分析", "基本面分析"],
            index=0
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🚀 开始分析", use_container_width=True):
            # 生成数据
            base_price = 100 + list(STOCK_SYMBOLS.keys()).index(stock_name) * 20
            volatility = 0.015 + random.random() * 0.02
            
            data = generate_professional_stock_data(start_date, end_date, base_price, volatility)
            indicators = calculate_advanced_indicators(data)
            metrics = calculate_fundamental_metrics(data, stock_info)
            
            # 存储到session state
            st.session_state['stock_data'] = data
            st.session_state['indicators'] = indicators
            st.session_state['metrics'] = metrics
            st.session_state['stock_info'] = stock_info
            st.session_state['stock_name'] = stock_name
            st.session_state['symbol'] = symbol
    
    # 主要内容区域
    if 'stock_data' in st.session_state:
        data = st.session_state['stock_data']
        indicators = st.session_state['indicators']
        metrics = st.session_state['metrics']
        stock_info = st.session_state['stock_info']
        stock_name = st.session_state['stock_name']
        
        # 关键指标卡片
        st.subheader("📈 关键指标概览")
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            change_color = "positive-change" if metrics['daily_return'] >= 0 else "negative-change"
            st.metric(
                "最新价格",
                f"¥{metrics['current_price']:.2f}",
                f"{metrics['daily_return']:+.2f}%",
                delta_color="normal"
            )
        
        with col2:
            st.metric("市盈率(PE)", f"{metrics['pe_ratio']:.1f}倍")
        
        with col3:
            st.metric("市净率(PB)", f"{metrics['pb_ratio']:.1f}倍")
        
        with col4:
            st.metric("股息率", f"{metrics['dividend_yield']:.1f}%")
        
        with col5:
            st.metric("换手率", f"{metrics['turnover_rate']:.2f}%")
        
        with col6:
            st.metric("波动率", f"{metrics['volatility']:.1f}%")
        
        st.markdown("---")
        
        # 根据分析类型显示不同内容
        if analysis_type == "综合分析" or analysis_type == "技术分析":
            # 技术分析部分
            st.subheader("📊 技术分析")
            
            # K线图
            col1, col2 = st.columns([3, 1])
            with col1:
                fig = create_candlestick_chart(data, indicators, stock_name)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### 技术指标解读")
                technical_analysis = professional_technical_analysis(data, indicators)
                
                for point in technical_analysis['analysis_points']:
                    st.markdown(point)
            
            # 技术指标图表
            st.subheader("📈 技术指标详情")
            
            col1, col2 = st.columns(2)
            with col1:
                fig_rsi = create_indicator_chart(data, indicators, 'RSI', stock_name)
                st.plotly_chart(fig_rsi, use_container_width=True)
                
                fig_macd = create_indicator_chart(data, indicators, 'MACD', stock_name)
                st.plotly_chart(fig_macd, use_container_width=True)
            
            with col2:
                fig_kdj = create_indicator_chart(data, indicators, 'KDJ', stock_name)
                st.plotly_chart(fig_kdj, use_container_width=True)
                
                fig_obv = create_indicator_chart(data, indicators, 'OBV', stock_name)
                st.plotly_chart(fig_obv, use_container_width=True)
        
        if analysis_type == "综合分析" or analysis_type == "基本面分析":
            # 基本面分析部分
            st.subheader("💰 基本面分析")
            
            fundamental_analysis = professional_fundamental_analysis(metrics, stock_info)
            
            for point in fundamental_analysis:
                st.markdown(point)
            
            # 行业对比
            st.subheader("🏢 行业对比分析")
            
            fig_industry = create_industry_comparison_chart(stock_info, metrics)
            st.plotly_chart(fig_industry, use_container_width=True)
        
        # 投资建议
        if analysis_type == "综合分析":
            st.markdown("---")
            st.subheader("🎯 投资建议")
            
            technical_analysis = professional_technical_analysis(data, indicators)
            fundamental_analysis = professional_fundamental_analysis(metrics, stock_info)
            recommendation = generate_professional_recommendation(technical_analysis, fundamental_analysis, metrics)
            
            # 显示推荐等级
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                color_map = {
                    'success': '#4CAF50',
                    'info': '#2196F3',
                    'warning': '#FF9800',
                    'danger': '#F44336'
                }
                
                st.markdown(f"""
                <div style="background: {color_map[recommendation['color']]}; color: white; padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0;">
                    <h2 style="color: white; margin: 0;">{recommendation['recommendation']}</h2>
                    <h3 style="color: white; margin: 10px 0;">评级: {recommendation['level']}</h3>
                    <p style="color: white; margin: 5px 0;">综合评分: {recommendation['score']}/100</p>
                    <p style="color: white; margin: 5px 0;">风险等级: {recommendation['risk_assessment']}</p>
                    <p style="color: white; margin: 5px 0;">投资周期: {recommendation['investment_horizon']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # 投资策略
            st.markdown("### 📋 投资策略建议")
            for strategy in recommendation['strategies']:
                st.markdown(f"- {strategy}")
            
            # 分析摘要
            st.markdown("### 📝 分析摘要")
            st.markdown(f"""
            <div class="info-box">
                <strong>技术面分析:</strong> {technical_analysis['summary']}
            </div>
            """, unsafe_allow_html=True)
            
            # 风险提示
            st.markdown("### ⚠️ 风险提示")
            st.markdown("""
            <div class="warning-box">
                <strong>重要提示:</strong>
                <ul>
                    <li>股票投资存在风险，历史表现不代表未来收益</li>
                    <li>本分析仅供参考，不构成投资建议</li>
                    <li>请根据自身风险承受能力做出投资决策</li>
                    <li>建议分散投资，控制单一股票仓位</li>
                    <li>关注市场整体环境和政策变化</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        # 初始提示
        st.markdown("""
        <div class="info-box">
            <h3>👋 欢迎使用专业金融分析平台</h3>
            <p>请在左侧选择股票和分析参数，然后点击"开始分析"按钮获取专业的投资分析报告。</p>
            <p><strong>功能特点:</strong></p>
            <ul>
                <li>📊 多维度技术分析（K线、均线、布林带、RSI、MACD、KDJ、OBV等）</li>
                <li>💰 深度基本面分析（估值、股息、市值、流动性等）</li>
                <li>🏢 行业对比分析</li>
                <li>🎯 AI驱动的投资建议</li>
                <li>⚠️ 专业的风险评估</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()