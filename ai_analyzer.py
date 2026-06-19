import numpy as np
import json

def analyze_stock_trend(data):
    if len(data) < 20:
        return "数据不足，无法进行趋势分析"
    
    recent_data = data[-30:]
    price_change = (recent_data['Close'].iloc[-1] - recent_data['Close'].iloc[0]) / recent_data['Close'].iloc[0] * 100
    
    ma5 = recent_data['MA5'].iloc[-1]
    ma20 = recent_data['MA20'].iloc[-1]
    ma60 = recent_data['MA60'].iloc[-1]
    rsi = recent_data['RSI'].iloc[-1]
    
    analysis = []
    
    if ma5 > ma20 > ma60:
        analysis.append("均线呈多头排列，趋势向上")
    elif ma5 < ma20 < ma60:
        analysis.append("均线呈空头排列，趋势向下")
    else:
        analysis.append("均线交织，趋势不明朗")
    
    if rsi > 70:
        analysis.append(f"RSI({rsi:.1f})处于超买区域，可能面临回调风险")
    elif rsi < 30:
        analysis.append(f"RSI({rsi:.1f})处于超卖区域，可能存在买入机会")
    else:
        analysis.append(f"RSI({rsi:.1f})处于正常区间")
    
    if price_change > 10:
        analysis.append(f"近30日涨幅{price_change:.1f}%，表现强势")
    elif price_change < -10:
        analysis.append(f"近30日跌幅{abs(price_change):.1f}%，表现弱势")
    else:
        analysis.append(f"近30日涨跌{price_change:.1f}%，表现平稳")
    
    return "\n".join(analysis)

def generate_investment_recommendation(data, stock_info):
    recent_data = data[-60:]
    price_change = (recent_data['Close'].iloc[-1] - recent_data['Close'].iloc[0]) / recent_data['Close'].iloc[0] * 100
    
    score = 50
    
    if stock_info['pe'] > 0 and stock_info['pe'] < 20:
        score += 15
    elif stock_info['pe'] >= 20 and stock_info['pe'] < 30:
        score += 5
    
    if stock_info['pb'] > 0 and stock_info['pb'] < 3:
        score += 10
    elif stock_info['pb'] >= 3 and stock_info['pb'] < 5:
        score += 5
    
    if stock_info['dividend'] > 2:
        score += 10
    elif stock_info['dividend'] > 1:
        score += 5
    
    ma5 = recent_data['MA5'].iloc[-1]
    ma20 = recent_data['MA20'].iloc[-1]
    if ma5 > ma20:
        score += 10
    
    rsi = recent_data['RSI'].iloc[-1]
    if rsi < 40:
        score += 5
    elif rsi > 60:
        score -= 5
    
    if score >= 75:
        recommendation = "强烈推荐买入"
    elif score >= 60:
        recommendation = "推荐买入"
    elif score >= 40:
        recommendation = "观望"
    else:
        recommendation = "建议卖出"
    
    return {
        'score': score,
        'recommendation': recommendation,
        'factors': {
            'valuation_score': min(25, (20 - min(stock_info['pe'], 20)) * 1.25 + (3 - min(stock_info['pb'], 3)) * 3.33),
            'dividend_score': min(10, stock_info['dividend'] * 5),
            'trend_score': 10 if ma5 > ma20 else 0,
            'momentum_score': 5 if rsi < 40 else (-5 if rsi > 60 else 0)
        }
    }

def ai_price_prediction(data, days=30):
    if len(data) < 60:
        return {"error": "数据不足，无法进行预测"}
    
    close_prices = data['Close'].values
    mean_price = np.mean(close_prices[-30:])
    volatility = np.std(close_prices[-30:])
    
    predictions = []
    last_price = close_prices[-1]
    
    for i in range(days):
        trend = np.random.normal(0, 0.01)
        noise = np.random.normal(0, volatility * 0.02)
        next_price = last_price * (1 + trend) + noise
        predictions.append(next_price)
        last_price = next_price
    
    prediction_df = {
        'date': pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=days).strftime('%Y-%m-%d').tolist(),
        'predicted_price': predictions,
        'upper_bound': [p * 1.05 for p in predictions],
        'lower_bound': [p * 0.95 for p in predictions]
    }
    
    return prediction_df

import pandas as pd

def generate_financial_news(symbol):
    news_items = {
        '600519.SS': [
            {'title': '茅台一季度营收同比增长18%', 'date': '2024-04-15', 'impact': 'positive'},
            {'title': '白酒行业迎来消费复苏', 'date': '2024-04-10', 'impact': 'positive'},
            {'title': '茅台宣布提价5%', 'date': '2024-04-05', 'impact': 'positive'}
        ],
        '000858.SZ': [
            {'title': '五粮液数字化转型初见成效', 'date': '2024-04-14', 'impact': 'positive'},
            {'title': '高端白酒市场竞争加剧', 'date': '2024-04-08', 'impact': 'neutral'}
        ],
        '600036.SS': [
            {'title': '招商银行净利润同比增长12%', 'date': '2024-04-15', 'impact': 'positive'},
            {'title': '银行板块估值修复行情启动', 'date': '2024-04-12', 'impact': 'positive'}
        ],
        '601318.SS': [
            {'title': '中国平安业绩超预期', 'date': '2024-04-16', 'impact': 'positive'},
            {'title': '保险行业改革持续推进', 'date': '2024-04-11', 'impact': 'neutral'}
        ],
        '002594.SZ': [
            {'title': '比亚迪新能源销量创新高', 'date': '2024-04-15', 'impact': 'positive'},
            {'title': '新能源汽车补贴政策调整', 'date': '2024-04-09', 'impact': 'negative'}
        ],
        '300750.SZ': [
            {'title': '宁德时代发布新一代电池技术', 'date': '2024-04-14', 'impact': 'positive'},
            {'title': '动力电池价格持续下降', 'date': '2024-04-07', 'impact': 'negative'}
        ],
        '00700.HK': [
            {'title': '腾讯游戏业务收入增长', 'date': '2024-04-15', 'impact': 'positive'},
            {'title': '监管政策影响科技股', 'date': '2024-04-10', 'impact': 'negative'}
        ],
        'BABA': [
            {'title': '阿里巴巴云计算业务增长强劲', 'date': '2024-04-16', 'impact': 'positive'},
            {'title': '电商行业竞争激烈', 'date': '2024-04-08', 'impact': 'neutral'}
        ],
        'AAPL': [
            {'title': '苹果新品发布会即将召开', 'date': '2024-04-15', 'impact': 'positive'},
            {'title': '全球智能手机市场疲软', 'date': '2024-04-11', 'impact': 'negative'}
        ],
        'TSLA': [
            {'title': '特斯拉降价促销效果显著', 'date': '2024-04-14', 'impact': 'positive'},
            {'title': '新能源汽车市场竞争白热化', 'date': '2024-04-06', 'impact': 'neutral'}
        ]
    }
    return news_items.get(symbol, [{'title': '暂无相关新闻', 'date': '2024-04-15', 'impact': 'neutral'}])