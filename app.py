import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from config import STOCK_SYMBOLS, DEFAULT_START_DATE, DEFAULT_END_DATE
from data_utils import fetch_stock_data, calculate_technical_indicators, get_stock_info, generate_portfolio_report
from ai_analyzer import analyze_stock_trend, generate_investment_recommendation, ai_price_prediction, generate_financial_news

st.set_page_config(page_title="AI金融大数据分析平台", page_icon="📈", layout="wide")

def main():
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
            fetch_and_display_data(symbol, stock_name, start_date, end_date)
    
    with col2:
        if 'stock_data' in st.session_state:
            display_stock_analysis()

def fetch_and_display_data(symbol, stock_name, start_date, end_date):
    data = fetch_stock_data(symbol, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
    data = calculate_technical_indicators(data)
    
    st.session_state['stock_data'] = data
    st.session_state['current_symbol'] = symbol
    st.session_state['current_stock_name'] = stock_name

def display_stock_analysis():
    data = st.session_state['stock_data']
    symbol = st.session_state['current_symbol']
    stock_name = st.session_state['current_stock_name']
    
    info = get_stock_info(symbol)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("最新价格", f"{data['Close'].iloc[-1]:.2f}", f"{((data['Close'].iloc[-1] - data['Close'].iloc[-2])/data['Close'].iloc[-2]*100):.2f}%")
    with col2:
        st.metric("市盈率(PE)", f"{info['pe']:.1f}")
    with col3:
        st.metric("市净率(PB)", f"{info['pb']:.1f}")
    with col4:
        st.metric("股息率(%)", f"{info['dividend']:.1f}%")
    
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=data.index,
                                  open=data['Open'],
                                  high=data['High'],
                                  low=data['Low'],
                                  close=data['Close'],
                                  name='K线图'))
    fig.add_trace(go.Scatter(x=data.index, y=data['MA5'], name='MA5', line=dict(color='blue', width=1)))
    fig.add_trace(go.Scatter(x=data.index, y=data['MA20'], name='MA20', line=dict(color='orange', width=1)))
    fig.add_trace(go.Scatter(x=data.index, y=data['MA60'], name='MA60', line=dict(color='green', width=1)))
    fig.update_layout(title=f'{stock_name} 价格走势', xaxis_title='日期', yaxis_title='价格', height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_rsi = go.Figure()
        fig_rsi.add_trace(go.Scatter(x=data.index, y=data['RSI'], name='RSI', line=dict(color='purple')))
        fig_rsi.add_hline(y=70, line_dash="dash", line_color="red")
        fig_rsi.add_hline(y=30, line_dash="dash", line_color="green")
        fig_rsi.update_layout(title='RSI指标', yaxis_range=[0, 100], height=300)
        st.plotly_chart(fig_rsi, use_container_width=True)
    
    with col2:
        fig_macd = go.Figure()
        fig_macd.add_trace(go.Scatter(x=data.index, y=data['MACD'], name='MACD', line=dict(color='blue')))
        fig_macd.add_trace(go.Scatter(x=data.index, y=data['Signal'], name='Signal', line=dict(color='red')))
        fig_macd.update_layout(title='MACD指标', height=300)
        st.plotly_chart(fig_macd, use_container_width=True)
    
    st.subheader("📊 AI智能分析")
    trend_analysis = analyze_stock_trend(data)
    st.write(trend_analysis)
    
    recommendation = generate_investment_recommendation(data, info)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("综合评分", recommendation['score'], recommendation['recommendation'])
    with col2:
        st.write("### 推荐建议")
        st.success(recommendation['recommendation'])
    
    st.write("#### 评分构成")
    factors = recommendation['factors']
    factor_df = pd.DataFrame({
        '指标': ['估值评分', '股息评分', '趋势评分', '动量评分'],
        '分数': [factors['valuation_score'], factors['dividend_score'], factors['trend_score'], factors['momentum_score']]
    })
    st.bar_chart(factor_df.set_index('指标'))

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
                report = generate_portfolio_report(selected_stocks, weights)
                
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
                
                fig = px.pie(values=weights, names=selected_stocks, title='组合权重分布')
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
        data = fetch_stock_data(symbol, DEFAULT_START_DATE, datetime.now().strftime('%Y-%m-%d'))
        data = calculate_technical_indicators(data)
        
        prediction = ai_price_prediction(data, days)
        
        if 'error' in prediction:
            st.error(prediction['error'])
        else:
            pred_df = pd.DataFrame(prediction)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data.index[-30:], y=data['Close'].values[-30:], name='历史价格', line=dict(color='blue')))
            fig.add_trace(go.Scatter(x=pred_df['date'], y=pred_df['predicted_price'], name='预测价格', line=dict(color='red', dash='dash')))
            fig.add_trace(go.Scatter(x=pred_df['date'], y=pred_df['upper_bound'], name='上限', line=dict(color='green', dash='dot')))
            fig.add_trace(go.Scatter(x=pred_df['date'], y=pred_df['lower_bound'], name='下限', line=dict(color='orange', dash='dot')))
            fig.update_layout(title=f'{stock_name} 价格预测', xaxis_title='日期', yaxis_title='价格', height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("📊 预测摘要")
            last_price = data['Close'].iloc[-1]
            predicted_price = pred_df['predicted_price'].iloc[-1]
            change = ((predicted_price - last_price) / last_price * 100)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("当前价格", f"{last_price:.2f}")
            with col2:
                st.metric(f"{days}天后预测", f"{predicted_price:.2f}", f"{change:.2f}%")
            with col3:
                st.metric("预测区间", f"{pred_df['lower_bound'].iloc[-1]:.2f} - {pred_df['upper_bound'].iloc[-1]:.2f}")

def news_tab():
    st.subheader("📰 财经资讯")
    
    stock_name = st.selectbox("选择股票查看相关新闻", list(STOCK_SYMBOLS.keys()), index=0, key='news_stock')
    symbol = STOCK_SYMBOLS[stock_name]
    
    news = generate_financial_news(symbol)
    
    for item in news:
        color = 'green' if item['impact'] == 'positive' else 'red' if item['impact'] == 'negative' else 'gray'
        with st.container():
            st.markdown(f"**[{item['date']}] {item['title']}**")
            st.markdown(f"<span style='color:{color}'>影响: {'正面' if item['impact'] == 'positive' else '负面' if item['impact'] == 'negative' else '中性'}</span>", unsafe_allow_html=True)
            st.markdown("---")

if __name__ == "__main__":
    main()