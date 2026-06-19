import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta

STOCK_SYMBOLS = {
    '贵州茅台': '600519.SS',
    '五粮液': '000858.SZ',
    '招商银行': '600036.SS',
    '中国平安': '601318.SS',
    '比亚迪': '002594.SZ',
    '宁德时代': '300750.SZ',
    '腾讯控股': '00700.HK',
    '阿里巴巴': 'BABA',
    '苹果': 'AAPL',
    '特斯拉': 'TSLA'
}

def generate_mock_stock_data(start_date, end_date, base_price=100):
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
            change = (np_random() - 0.5) * 4
            current_price = max(current_price + change, 50)
            open_price = current_price + (np_random() - 0.5) * 2
            high_price = max(current_price, open_price) * (1 + np_random() * 0.02)
            low_price = min(current_price, open_price) * (1 - np_random() * 0.02)
            
            dates.append(current_date)
            opens.append(open_price)
            highs.append(high_price)
            lows.append(low_price)
            closes.append(current_price)
            volumes.append(int(np_random() * 9000000 + 1000000))
        
        current_date += timedelta(days=1)
    
    return {
        'dates': dates,
        'opens': opens,
        'highs': highs,
        'lows': lows,
        'closes': closes,
        'volumes': volumes
    }

def np_random():
    import random
    return random.random()

def calculate_indicators(data):
    closes = data['closes']
    dates = data['dates']
    
    ma5 = []
    ma20 = []
    rsi = []
    macd = []
    signal = []
    
    for i in range(len(closes)):
        if i >= 4:
            ma5_val = sum(closes[i-4:i+1]) / 5
        else:
            ma5_val = None
        ma5.append(ma5_val)
        
        if i >= 19:
            ma20_val = sum(closes[i-19:i+1]) / 20
        else:
            ma20_val = None
        ma20.append(ma20_val)
        
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
        else:
            rsi_val = None
        rsi.append(rsi_val)
        
        if i >= 25:
            ema12 = sum(closes[i-11:i+1]) / 12
            ema26 = sum(closes[i-25:i+1]) / 26
            macd_val = ema12 - ema26
        else:
            macd_val = None
        macd.append(macd_val)
        
        if i >= 33:
            signal_val = sum(macd[i-8:i+1]) / 9
        else:
            signal_val = None
        signal.append(signal_val)
    
    return {
        'dates': dates,
        'ma5': ma5,
        'ma20': ma20,
        'rsi': rsi,
        'macd': macd,
        'signal': signal
    }

def analyze_stock_trend(data, indicators):
    recent_closes = data['closes'][-30:]
    price_change = (recent_closes[-1] - recent_closes[0]) / recent_closes[0] * 100
    
    ma5_val = indicators['ma5'][-1] if indicators['ma5'][-1] else 0
    ma20_val = indicators['ma20'][-1] if indicators['ma20'][-1] else 0
    rsi_val = indicators['rsi'][-1] if indicators['rsi'][-1] else 50
    
    analysis = []
    
    if ma5_val > ma20_val > 0:
        analysis.append("均线呈多头排列，趋势向上")
    elif ma5_val < ma20_val and ma20_val > 0:
        analysis.append("均线呈空头排列，趋势向下")
    else:
        analysis.append("均线交织，趋势不明朗")
    
    if rsi_val > 70:
        analysis.append(f"RSI({rsi_val:.1f})处于超买区域，可能面临回调风险")
    elif rsi_val < 30:
        analysis.append(f"RSI({rsi_val:.1f})处于超卖区域，可能存在买入机会")
    else:
        analysis.append(f"RSI({rsi_val:.1f})处于正常区间")
    
    if price_change > 10:
        analysis.append(f"近30日涨幅{price_change:.1f}%，表现强势")
    elif price_change < -10:
        analysis.append(f"近30日跌幅{abs(price_change):.1f}%，表现弱势")
    else:
        analysis.append(f"近30日涨跌{price_change:.1f}%，表现平稳")
    
    return "\n".join(analysis)

def generate_recommendation(data, stock_info):
    recent_closes = data['closes'][-60:]
    price_change = (recent_closes[-1] - recent_closes[0]) / recent_closes[0] * 100
    
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
    
    ma5_val = stock_info.get('ma5', 0)
    ma20_val = stock_info.get('ma20', 0)
    if ma5_val > ma20_val > 0:
        score += 10
    
    rsi_val = stock_info.get('rsi', 50)
    if rsi_val < 40:
        score += 5
    elif rsi_val > 60:
        score -= 5
    
    if score >= 75:
        recommendation = "强烈推荐买入"
    elif score >= 60:
        recommendation = "推荐买入"
    elif score >= 40:
        recommendation = "观望"
    else:
        recommendation = "建议卖出"
    
    return {'score': score, 'recommendation': recommendation}

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

def generate_news(symbol):
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

def main():
    st.set_page_config(page_title="AI金融大数据分析平台", page_icon="📈", layout="wide")
    st.title("📈 AI驱动的金融大数据分析平台")
    st.markdown("---")
    
    tabs = st.tabs(["📊 股票分析", "💰 投资组合", "🔮 AI预测", "📰 财经资讯"])
    
    with tabs[0]:
        stock_analysis_tab()
    
    with tabs[1]:
        portfolio_tab()
    
    with tabs[2]:
        ai_prediction_tab()
    
    with tabs[3]:
        news_tab()

def stock_analysis_tab():
    col1, col2 = st.columns([1, 3])
    
    with col1:
        stock_name = st.selectbox("选择股票", list(STOCK_SYMBOLS.keys()), index=0)
        symbol = STOCK_SYMBOLS[stock_name]
        
        today = datetime.now()
        start_date = st.date_input("开始日期", datetime(today.year - 1, today.month, today.day))
        end_date = st.date_input("结束日期", today)
        
        if st.button("获取数据"):
            data = generate_mock_stock_data(start_date, end_date, base_price=100 + list(STOCK_SYMBOLS.keys()).index(stock_name) * 20)
            indicators = calculate_indicators(data)
            st.session_state['stock_data'] = data
            st.session_state['indicators'] = indicators
            st.session_state['current_symbol'] = symbol
            st.session_state['current_stock_name'] = stock_name
    
    with col2:
        if 'stock_data' in st.session_state:
            display_stock_analysis()

def display_stock_analysis():
    data = st.session_state['stock_data']
    indicators = st.session_state['indicators']
    symbol = st.session_state['current_symbol']
    stock_name = st.session_state['current_stock_name']
    
    info = get_stock_info(symbol)
    last_close = data['closes'][-1] if data['closes'] else 0
    prev_close = data['closes'][-2] if len(data['closes']) > 1 else last_close
    change = ((last_close - prev_close) / prev_close * 100) if prev_close > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("最新价格", f"{last_close:.2f}", f"{change:.2f}%")
    with col2:
        st.metric("市盈率(PE)", f"{info['pe']:.1f}")
    with col3:
        st.metric("市净率(PB)", f"{info['pb']:.1f}")
    with col4:
        st.metric("股息率(%)", f"{info['dividend']:.1f}%")
    
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=data['dates'],
                                  open=data['opens'],
                                  high=data['highs'],
                                  low=data['lows'],
                                  close=data['closes'],
                                  name='K线图'))
    
    valid_ma5 = [(d, v) for d, v in zip(data['dates'], indicators['ma5']) if v is not None]
    if valid_ma5:
        fig.add_trace(go.Scatter(x=[x[0] for x in valid_ma5], y=[x[1] for x in valid_ma5], name='MA5', line=dict(color='blue', width=1)))
    
    valid_ma20 = [(d, v) for d, v in zip(data['dates'], indicators['ma20']) if v is not None]
    if valid_ma20:
        fig.add_trace(go.Scatter(x=[x[0] for x in valid_ma20], y=[x[1] for x in valid_ma20], name='MA20', line=dict(color='orange', width=1)))
    
    fig.update_layout(title=f'{stock_name} 价格走势', xaxis_title='日期', yaxis_title='价格', height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        valid_rsi = [(d, v) for d, v in zip(data['dates'], indicators['rsi']) if v is not None]
        if valid_rsi:
            fig_rsi = go.Figure()
            fig_rsi.add_trace(go.Scatter(x=[x[0] for x in valid_rsi], y=[x[1] for x in valid_rsi], name='RSI', line=dict(color='purple')))
            fig_rsi.add_hline(y=70, line_dash="dash", line_color="red")
            fig_rsi.add_hline(y=30, line_dash="dash", line_color="green")
            fig_rsi.update_layout(title='RSI指标', yaxis_range=[0, 100], height=300)
            st.plotly_chart(fig_rsi, use_container_width=True)
    
    with col2:
        valid_macd = [(d, v) for d, v in zip(data['dates'], indicators['macd']) if v is not None]
        valid_signal = [(d, v) for d, v in zip(data['dates'], indicators['signal']) if v is not None]
        if valid_macd:
            fig_macd = go.Figure()
            fig_macd.add_trace(go.Scatter(x=[x[0] for x in valid_macd], y=[x[1] for x in valid_macd], name='MACD', line=dict(color='blue')))
            if valid_signal:
                fig_macd.add_trace(go.Scatter(x=[x[0] for x in valid_signal], y=[x[1] for x in valid_signal], name='Signal', line=dict(color='red')))
            fig_macd.update_layout(title='MACD指标', height=300)
            st.plotly_chart(fig_macd, use_container_width=True)
    
    st.subheader("📊 AI智能分析")
    trend_analysis = analyze_stock_trend(data, indicators)
    st.write(trend_analysis)
    
    rec_info = info.copy()
    rec_info['ma5'] = indicators['ma5'][-1] if indicators['ma5'][-1] else 0
    rec_info['ma20'] = indicators['ma20'][-1] if indicators['ma20'][-1] else 0
    rec_info['rsi'] = indicators['rsi'][-1] if indicators['rsi'][-1] else 50
    
    recommendation = generate_recommendation(data, rec_info)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("综合评分", recommendation['score'], recommendation['recommendation'])
    with col2:
        st.write("### 推荐建议")
        st.success(recommendation['recommendation'])

def portfolio_tab():
    st.subheader("💰 投资组合管理")
    
    selected_stocks = st.multiselect("选择股票", list(STOCK_SYMBOLS.keys()), default=['贵州茅台', '招商银行'])
    
    if len(selected_stocks) > 0:
        weights = []
        for stock in selected_stocks:
            weight = st.slider(f"{stock} 权重 (%)", 0, 100, int(100/len(selected_stocks)), key=stock)
            weights.append(weight)
        
        if sum(weights) != 100:
            st.warning("权重总和必须为100%")
        else:
            if st.button("生成组合报告"):
                import random
                report = {
                    'total_return': random.uniform(-10, 30),
                    'annual_return': random.uniform(5, 25),
                    'volatility': random.uniform(15, 40),
                    'sharpe_ratio': random.uniform(0.5, 2.0),
                    'max_drawdown': random.uniform(-5, -25)
                }
                
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.metric("总收益率", f"{report['total_return']:.2f}%")
                with col2:
                    st.metric("年化收益率", f"{report['annual_return']:.2f}%")
                with col3:
                    st.metric("波动率", f"{report['volatility']:.2f}%")
                with col4:
                    st.metric("夏普比率", f"{report['sharpe_ratio']:.2f}")
                with col5:
                    st.metric("最大回撤", f"{report['max_drawdown']:.2f}%")
                
                fig = go.Figure(data=[go.Pie(labels=selected_stocks, values=weights)])
                fig.update_layout(title='组合权重分布')
                st.plotly_chart(fig, use_container_width=True)
                
                st.subheader("📋 组合分析报告")
                st.write(f"""
                **风险等级评估**: {'低风险' if report['volatility'] < 20 else '中等风险' if report['volatility'] < 30 else '高风险'}
                
                **收益预期**: 该组合预期年化收益率为 {report['annual_return']:.1f}%，在同类组合中处于 {'优秀' if report['annual_return'] > 15 else '良好' if report['annual_return'] > 10 else '一般'} 水平。
                
                **风险提示**: 历史最大回撤为 {report['max_drawdown']:.1f}%，建议根据自身风险承受能力调整仓位。
                """)

def ai_prediction_tab():
    st.subheader("🔮 AI价格预测")
    
    stock_name = st.selectbox("选择股票", list(STOCK_SYMBOLS.keys()), index=0, key='pred_stock')
    symbol = STOCK_SYMBOLS[stock_name]
    
    days = st.slider("预测天数", 7, 60, 30)
    
    if st.button("开始预测"):
        today = datetime.now()
        start_date = today - timedelta(days=100)
        data = generate_mock_stock_data(start_date, today, base_price=100 + list(STOCK_SYMBOLS.keys()).index(stock_name) * 20)
        
        last_price = data['closes'][-1] if data['closes'] else 100
        predictions = []
        upper_bounds = []
        lower_bounds = []
        current_price = last_price
        
        import random
        for i in range(days):
            trend = (random.random() - 0.5) * 0.02
            noise = (random.random() - 0.5) * 0.02 * current_price
            next_price = current_price * (1 + trend) + noise
            predictions.append(next_price)
            upper_bounds.append(next_price * 1.05)
            lower_bounds.append(next_price * 0.95)
            current_price = next_price
        
        pred_dates = [today + timedelta(days=i+1) for i in range(days)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['dates'][-30:], y=data['closes'][-30:], name='历史价格', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=pred_dates, y=predictions, name='预测价格', line=dict(color='red', dash='dash')))
        fig.add_trace(go.Scatter(x=pred_dates, y=upper_bounds, name='上限', line=dict(color='green', dash='dot')))
        fig.add_trace(go.Scatter(x=pred_dates, y=lower_bounds, name='下限', line=dict(color='orange', dash='dot')))
        fig.update_layout(title=f'{stock_name} 价格预测', xaxis_title='日期', yaxis_title='价格', height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("📊 预测摘要")
        predicted_price = predictions[-1]
        change = ((predicted_price - last_price) / last_price * 100) if last_price > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("当前价格", f"{last_price:.2f}")
        with col2:
            st.metric(f"{days}天后预测", f"{predicted_price:.2f}", f"{change:.2f}%")
        with col3:
            st.metric("预测区间", f"{lower_bounds[-1]:.2f} - {upper_bounds[-1]:.2f}")

def news_tab():
    st.subheader("📰 财经资讯")
    
    stock_name = st.selectbox("选择股票查看相关新闻", list(STOCK_SYMBOLS.keys()), index=0, key='news_stock')
    symbol = STOCK_SYMBOLS[stock_name]
    
    news = generate_news(symbol)
    
    for item in news:
        color = 'green' if item['impact'] == 'positive' else 'red' if item['impact'] == 'negative' else 'gray'
        with st.container():
            st.markdown(f"**[{item['date']}] {item['title']}**")
            st.markdown(f"<span style='color:{color}'>影响: {'正面' if item['impact'] == 'positive' else '负面' if item['impact'] == 'negative' else '中性'}</span>", unsafe_allow_html=True)
            st.markdown("---")

if __name__ == "__main__":
    main()