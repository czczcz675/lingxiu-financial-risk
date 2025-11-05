import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time

# 页面配置
st.set_page_config(
    page_title="灵嗅金融风险监测系统",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 高级CSS样式 - 优化文字可见度和整体布局
st.markdown("""
<style>
    /* 全局样式 */
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        color: #333;
        line-height: 1.6;
        background-color: #f5f7fa;
    }
    
    /* 确保所有文本清晰可见 */
    * {
        text-shadow: none !important;
    }
    
    /* 调整主标题样式 */
    .main-header {
        font-size: 2.5rem !important;
        font-weight: 900 !important;
        color: #ffffff !important;
        margin-bottom: 2rem !important;
        text-align: center !important;
        padding: 1.5rem !important;
        background: linear-gradient(135deg, #2c3e50 0%, #1a1a2e 100%) !important;
        border-radius: 15px !important;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15) !important;
        letter-spacing: 0.5px !important;
    }
    
    /* 调整副标题样式 */
    .sub-header {
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        color: #2c3e50 !important;
        margin: 2rem 0 1.5rem 0 !important;
        padding-left: 15px !important;
        border-left: 5px solid #3498db !important;
        background: linear-gradient(90deg, #f8f9fa, transparent);
    }
    
    /* 高级指标卡片 - 增强可见度 */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem !important;
        border-radius: 15px;
        color: white;
        margin: 0.8rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        border: 1px solid rgba(255,255,255,0.2);
        transition: transform 0.3s ease;
        text-align: center;
        height: 250px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.2);
    }
    
    .metric-card div {
        margin: 0.5rem 0;
    }
    
    /* 数据表格样式优化 - 提高字体大小 */
    .dataframe {
        font-size: 16px !important;
        line-height: 1.6;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Streamlit组件样式优化 */
    .stDataFrame {
        font-size: 16px !important;
        margin-top: 1rem;
        border-radius: 8px !important;
        overflow: hidden !important;
    }
    
    .stPlotlyChart {
        margin: 1.5rem 0;
        background-color: white !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* 风险等级样式 - 增强对比度和字体大小 */
    .risk-high {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        color: white;
        padding: 0.8rem 1.2rem;
        border-radius: 8px;
        text-align: center;
        font-weight: 700;
        font-size: 1.1rem !important;
        box-shadow: 0 4px 15px rgba(255,107,107,0.3);
    }
    
    .risk-medium {
        background: linear-gradient(135deg, #ffa726 0%, #f57c00 100%);
        color: white;
        padding: 0.8rem 1.2rem;
        border-radius: 8px;
        text-align: center;
        font-weight: 700;
        font-size: 1.1rem !important;
        box-shadow: 0 4px 15px rgba(255,167,38,0.3);
    }
    
    .risk-low {
        background: linear-gradient(135deg, #66bb6a 0%, #4caf50 100%);
        color: white;
        padding: 0.8rem 1.2rem;
        border-radius: 8px;
        text-align: center;
        font-weight: 700;
        font-size: 1.1rem !important;
        box-shadow: 0 4px 15px rgba(102,187,106,0.3);
    }
    
    /* 确保按钮文本清晰 */
    .stButton button {
        font-size: 18px !important;
        font-weight: 700 !important;
        padding: 0.8rem 1.5rem !important;
        color: white !important;
        background-color: #3498db !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton button:hover {
        background-color: #2980b9 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(52, 152, 219, 0.4) !important;
    }
    
    /* 增强表格可读性 */
    .dataframe th {
        background-color: #34495e !important;
        color: white !important;
        font-weight: 700 !important;
        padding: 15px !important;
        text-align: center !important;
        font-size: 1.1rem !important;
    }
    
    .dataframe td {
        padding: 12px !important;
        text-align: center !important;
        font-size: 1rem !important;
    }
    
    /* 确保所有文本元素的对比度 */
    p, div, span, label {
        color: #333 !important;
        font-weight: normal;
    }
    
    /* 减少整体页面边距，使内容更紧凑 */
    .css-1v3fvcr {
        padding: 1rem;
    }
    
    /* 改善滚动条体验 */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 8px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #3498db;
        border-radius: 8px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #2980b9;
    }
    
    /* 预警卡片样式优化 */
    .alert-card {
        background-color: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        border-left: 5px solid #e0e0e0;
    }
    
    /* 表格样式增强 */
    table {
        width: 100% !important;
    }
    
    /* 页脚样式 */
    .footer-note {
        font-size: 1.1rem !important;
        color: #34495e !important;
        font-weight: bold !important;
        text-align: center !important;
        margin-top: 1rem !important;
        padding: 1rem !important;
        background-color: #f8f9fa !important;
        border-radius: 8px !important;
    }
    
    /* 响应式设计 */
    @media (max-width: 1024px) {
        .main-header {
            font-size: 2.2rem !important;
        }
        
        .sub-header {
            font-size: 1.6rem !important;
        }
        
        .metric-card {
            height: 220px;
            padding: 1.5rem !important;
        }
    }
    
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem !important;
            padding: 1.2rem !important;
        }
        
        .sub-header {
            font-size: 1.4rem !important;
        }
        
        .metric-card {
            height: 200px;
            padding: 1.2rem !important;
        }
        
        th, td {
            font-size: 1rem !important;
            padding: 8px !important;
        }
        
        .stButton > button {
            font-size: 1rem !important;
            padding: 0.6rem 1rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

class AdvancedFinancialRiskMonitor:
    def __init__(self):
        self.initialize_data()
    
    def initialize_data(self):
        """初始化高级模拟数据"""
        np.random.seed(42)
        
        # 生成更真实的时间序列数据
        dates = pd.date_range(start='2024-01-01', end='2024-03-20', freq='D')
        
        # 创建有趋势和季节性的风险数据
        t = np.arange(len(dates))
        market_trend = 60 + 0.1 * t + 10 * np.sin(2 * np.pi * t / 30)
        credit_trend = 45 + 0.05 * t + 8 * np.sin(2 * np.pi * t / 45)
        liquidity_trend = 35 + 0.03 * t + 6 * np.sin(2 * np.pi * t / 60)
        operational_trend = 25 + 0.02 * t + 4 * np.sin(2 * np.pi * t / 90)
        
        self.risk_data = pd.DataFrame({
            'date': dates,
            'market_risk': market_trend + np.random.normal(0, 5, len(dates)),
            'credit_risk': credit_trend + np.random.normal(0, 4, len(dates)),
            'liquidity_risk': liquidity_trend + np.random.normal(0, 3, len(dates)),
            'operational_risk': operational_trend + np.random.normal(0, 2, len(dates))
        })
        
        # 更丰富的预警事件数据
        self.alerts_data = pd.DataFrame({
            '时间': pd.date_range('2024-03-15', periods=12, freq='2h'),
            '风险类型': ['市场风险', '信用风险', '流动性风险', '操作风险', 
                      '市场风险', '信用风险', '系统性风险', '合规风险',
                      '汇率风险', '利率风险', '操作风险', '信用风险'],
            '风险等级': ['高', '中', '高', '低', '高', '中', '高', '中', '中', '低', '中', '高'],
            '风险描述': [
                '沪深300指数异常波动超过3σ',
                '某城商行信用评级下调至AA-',
                '银行间市场流动性紧张度上升',
                '内部交易系统出现技术故障',
                '市场恐慌指数VIX大幅上升',
                '企业债券违约风险显著增加',
                '跨市场风险传导效应增强',
                '新监管政策合规性检查预警',
                '人民币汇率波动率超出阈值',
                '国债收益率曲线异常变动',
                '交易系统响应延迟超过阈值',
                '信贷资产质量下行压力增大'
            ],
            '影响程度': ['严重', '中等', '较高', '较低', '严重', '中等', '严重', '中等', '中等', '较低', '中等', '较高'],
            '处置状态': ['已处理', '处理中', '待处理', '已处理', '处理中', '待处理', '紧急处理', '已处理', '处理中', '已处理', '待处理', '紧急处理']
        })
        
        # 更详细的机构风险数据
        self.institution_risk = pd.DataFrame({
            '机构名称': ['招商银行', '中信证券', '华夏基金', '平安保险', '浦发银行', 
                      '国泰君安', '易方达基金', '中国人寿', '兴业银行', '海通证券',
                      '广发证券', '光大银行'],
            '风险评分': [85, 72, 68, 79, 82, 75, 65, 78, 81, 70, 74, 80],
            '风险等级': ['A', 'B', 'B', 'A', 'A', 'B', 'C', 'B', 'A', 'B', 'B', 'A'],
            '所属板块': ['银行', '证券', '基金', '保险', '银行', 
                      '证券', '基金', '保险', '银行', '证券', '证券', '银行'],
            '资产规模(亿元)': [89000, 12000, 8500, 105000, 82000, 9800, 7200, 48000, 78000, 8500, 9200, 65000],
            '风险变化': ['↓2.1%', '↑1.5%', '↑3.2%', '↓0.8%', '↓1.2%', '↑2.1%', '↑4.5%', '↓0.5%', '↓1.8%', '↑1.9%', '↑2.3%', '↓0.9%']
        })

    def create_advanced_dashboard(self):
        """创建高级风险监测仪表盘"""
        # 第一行：关键性能指标
        st.markdown('<div class="sub-header">📊 核心性能指标</div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            self.create_metric_card("实时风险识别准确率", "95.2%", "+2.5%", "accuracy")
            
        with col2:
            self.create_metric_card("平均预警提前时间", "72小时", "+8小时", "time")
            
        with col3:
            self.create_metric_card("系统可用性", "99.95%", "+0.2%", "availability")
            
        with col4:
            self.create_metric_card("数据处理能力", "15万条/秒", "+5%", "throughput")
        
        # 第二行：风险趋势和实时预警
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<div class="sub-header">📈 多维度风险趋势分析</div>', unsafe_allow_html=True)
            self.create_advanced_risk_chart()
            
        with col2:
            st.markdown('<div class="sub-header">⚠️ 实时风险预警</div>', unsafe_allow_html=True)
            self.display_advanced_alerts()
        
        # 第三行：机构分析和AI洞察
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="sub-header">🏛️ 金融机构风险画像</div>', unsafe_allow_html=True)
            self.create_advanced_institution_chart()
            
        with col2:
            st.markdown('<div class="sub-header">🤖 AI智能风险洞察</div>', unsafe_allow_html=True)
            self.display_advanced_ai_analysis()

    def create_metric_card(self, title, value, delta, icon_type):
        """创建高级指标卡片"""
        icons = {
            "accuracy": "🎯",
            "time": "⏰", 
            "availability": "🛡️",
            "throughput": "⚡"
        }
        
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{icons[icon_type]}</div>
            <div style="font-size: 1.2rem; opacity: 0.9;">{title}</div>
            <div style="font-size: 2rem; font-weight: 800; margin: 0.5rem 0;">{value}</div>
            <div style="font-size: 1rem; opacity: 0.8;">{delta}</div>
        </div>
        """, unsafe_allow_html=True)

    def create_advanced_risk_chart(self):
        """创建高级风险趋势图表"""
        fig = go.Figure()
        
        # 使用更丰富的图表样式
        risk_colors = ['#ff6b6b', '#ffa726', '#66bb6a', '#42a5f5']
        risk_names = ['市场风险', '信用风险', '流动性风险', '操作风险']
        risk_data_columns = ['market_risk', 'credit_risk', 'liquidity_risk', 'operational_risk']
        
        for i, (col, name, color) in enumerate(zip(risk_data_columns, risk_names, risk_colors)):
            fig.add_trace(go.Scatter(
                x=self.risk_data['date'],
                y=self.risk_data[col],
                name=name,
                line=dict(color=color, width=4),
                fill='tozeroy' if i == 0 else None,
                fillcolor=f'rgba{tuple(int(color.lstrip("#")[j:j+2], 16) for j in (0, 2, 4)) + (0.1,)}'
            ))
        
        fig.update_layout(
            title=dict(
                text='<b>多维度风险趋势实时监测</b>',
                x=0.5,
                xanchor='center',
                font=dict(size=20, color='#2c3e50')
            ),
            xaxis=dict(
                title='时间',
                gridcolor='#f0f0f0',
                showline=True,
                linecolor='#e0e0e0'
            ),
            yaxis=dict(
                title='风险指数',
                gridcolor='#f0f0f0',
                showline=True,
                linecolor='#e0e0e0'
            ),
            height=450,
            template='plotly_white',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def display_advanced_alerts(self):
        """显示高级预警信息"""
        # 添加搜索和筛选功能
        col1, col2 = st.columns([2, 1])
        with col1:
            search_term = st.text_input("🔍 搜索预警信息", placeholder="输入风险类型或描述...")
        with col2:
            risk_filter = st.selectbox("筛选风险等级", ["全部", "高", "中", "低"])
        
        filtered_alerts = self.alerts_data.copy()
        if search_term:
            filtered_alerts = filtered_alerts[
                filtered_alerts['风险类型'].str.contains(search_term) | 
                filtered_alerts['风险描述'].str.contains(search_term)
            ]
        if risk_filter != "全部":
            filtered_alerts = filtered_alerts[filtered_alerts['风险等级'] == risk_filter]
        
        for idx, alert in filtered_alerts.iterrows():
            if alert['风险等级'] == '高':
                border_color = '#ff6b6b'
                risk_class = 'risk-high'
            elif alert['风险等级'] == '中':
                border_color = '#ffa726'
                risk_class = 'risk-medium'
            else:
                border_color = '#66bb6a'
                risk_class = 'risk-low'
                
            st.markdown(f"""
            <div class="alert-card" style="border-left-color: {border_color};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="{risk_class}" style="font-size: 0.9rem;">{alert['风险等级']}风险</span>
                    <span style="font-size: 0.9rem; color: #666;">{alert['时间'].strftime('%m-%d %H:%M')}</span>
                </div>
                <div style="font-weight: 700; color: #2c3e50; margin: 0.5rem 0; font-size: 1.1rem;">
                    {alert['风险类型']}
                </div>
                <div style="color: #555; line-height: 1.4; margin-bottom: 0.5rem;">
                    {alert['风险描述']}
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.9rem;">
                    <span style="color: #777;">影响: {alert['影响程度']}</span>
                    <span style="color: { '#4caf50' if alert['处置状态'] == '已处理' else '#ff9800' if alert['处置状态'] == '处理中' else '#f44336' };">
                        {alert['处置状态']}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    def create_advanced_institution_chart(self):
        """创建高级机构风险分布图"""
        # 使用太阳图替代树状图
        fig = px.sunburst(
            self.institution_risk,
            path=['所属板块', '机构名称'],
            values='资产规模(亿元)',
            color='风险评分',
            color_continuous_scale='RdYlGn_r',
            title='金融机构风险与资产规模分布'
        )
        fig.update_layout(
            height=400,
            font=dict(size=12)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 添加风险评分表格
        st.markdown("#### 📋 机构风险评分详情")
        display_df = self.institution_risk[['机构名称', '所属板块', '风险评分', '风险等级', '风险变化']].copy()

        # 使用兼容的样式方法
        def color_risk_score(val):
            if val >= 80:
                return 'background-color: #4caf50; color: white; font-weight: bold;'
            elif val >= 70:
                return 'background-color: #ff9800; color: white; font-weight: bold;'
            else:
                return 'background-color: #f44336; color: white; font-weight: bold;'

        styled_df = display_df.style.map(color_risk_score, subset=['风险评分'])
        st.dataframe(styled_df, use_container_width=True)

    def display_advanced_ai_analysis(self):
        """显示高级AI分析结果"""
        # AI分析仪表盘
        col1, col2 = st.columns(2)
        
        with col1:
            # 创建模型性能仪表盘
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = 95.2,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "实体识别准确率", 'font': {'size': 16}},
                delta = {'reference': 82.7, 'increasing': {'color': "#4caf50"}},
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#2c3e50"},
                    'bar': {'color': "#667eea"},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 70], 'color': '#ffcdd2'},
                        {'range': [70, 90], 'color': '#fff9c4'},
                        {'range': [90, 100], 'color': '#c8e6c9'}],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90}}
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            # 关键指标对比
            metrics_comparison = pd.DataFrame({
                '指标': ['实体识别准确率', '关系抽取F1值', '风险预警准确率', '响应时间'],
                '灵嗅系统': [95.2, 94.8, 87.3, 0.5],
                '行业平均': [82.7, 79.3, 75.2, 2.1]
            })
            
            st.markdown("#### 📊 性能指标对比")
            for _, row in metrics_comparison.iterrows():
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.write(f"**{row['指标']}**")
                with col2:
                    st.metric("灵嗅系统", f"{row['灵嗅系统']}", delta=f"+{row['灵嗅系统'] - row['行业平均']:.1f}")
                with col3:
                    st.write(f"行业: {row['行业平均']}")
                st.progress(row['灵嗅系统'] / 100)
        
        # AI洞察报告
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 15px; color: white; margin-top: 1rem;'>
            <h4 style='color: white; margin-bottom: 1rem;'>🧠 BERT-BiLSTM-CRF 智能分析洞察</h4>
            <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px;'>
                <p style='margin: 0.5rem 0;'>🚨 <strong>风险预警：</strong>检测到中小银行板块流动性风险传导效应增强，建议重点关注</p>
                <p style='margin: 0.5rem 0;'>📈 <strong>趋势预测：</strong>市场风险指数预计在未来72小时内上升12-15%</p>
                <p style='margin: 0.5rem 0;'>🔍 <strong>异常检测：</strong>发现3家机构信用风险指标异常波动</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    def create_risk_heatmap(self):
        """创建高级风险热力图"""
        st.markdown('<div class="sub-header">🔥 跨市场风险热力图</div>', unsafe_allow_html=True)
        
        # 生成更真实的热力数据
        sectors = ['商业银行', '证券公司', '保险公司', '基金公司', '信托公司', '租赁公司', '支付机构', '金融科技']
        risk_types = ['市场风险', '信用风险', '流动性风险', '操作风险', '合规风险', '系统性风险']
        
        # 创建有相关性的风险数据
        base_risk = np.random.randint(20, 80, len(sectors))
        heatmap_data = []
        for risk in risk_types:
            row = base_risk * (0.8 + 0.4 * np.random.random(len(sectors)))
            heatmap_data.append(row)
        
        heatmap_df = pd.DataFrame(
            heatmap_data,
            index=risk_types,
            columns=sectors
        )
        
        fig = px.imshow(
            heatmap_df,
            text_auto=True,
            aspect="auto",
            color_continuous_scale='RdYlGn_r',
            title='金融机构风险暴露热力图'
        )
        fig.update_layout(
            height=500,
            font=dict(size=12)
        )
        st.plotly_chart(fig, use_container_width=True)

    def create_technical_dashboard(self):
        """创建技术架构展示页面"""
        st.markdown('<div class="sub-header">🏗️ 系统架构设计</div>', unsafe_allow_html=True)
        
        # 系统架构概览
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: white; border-radius: 10px; border: 2px dashed #667eea;">
                <h5 style="color: #667eea;">🔮 灵嗅系统架构图</h5>
                <p style="color: #666; margin-top: 1rem;">数据采集层 → 数据处理层 → AI分析层 → 应用服务层</p>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1.5rem;">
                    <div style="background: #e3f2fd; padding: 1rem; border-radius: 8px;">
                        <strong>数据源</strong><br>API/爬虫/数据库
                    </div>
                    <div style="background: #e8f5e8; padding: 1rem; border-radius: 8px;">
                        <strong>BERT模型</strong><br>实体识别
                    </div>
                    <div style="background: #fff3e0; padding: 1rem; border-radius: 8px;">
                        <strong>BiLSTM</strong><br>序列分析
                    </div>
                    <div style="background: #fce4ec; padding: 1rem; border-radius: 8px;">
                        <strong>CRF层</strong><br>标签优化
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("#### 🔧 核心技术栈")
            
            tech_stack = {
                "AI框架": ["TensorFlow 2.8", "PyTorch 1.12", "HuggingFace Transformers"],
                "数据处理": ["Apache Spark 3.2", "Apache Flink 1.14", "Apache Airflow 2.3"],
                "数据库": ["PostgreSQL 14", "MongoDB 5.0", "Redis 7.0", "Neo4j 4.4"],
                "部署运维": ["Docker", "Kubernetes", "Prometheus", "Grafana"]
            }
            
            for category, technologies in tech_stack.items():
                st.markdown(f"""
                <div style="margin-bottom: 1.5rem;">
                    <h5 style="color: #667eea; margin-bottom: 0.5rem;">{category}</h5>
                    <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
                        {''.join([f'<span style="background: #f0f2f6; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem;">{tech}</span>' for tech in technologies])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # 性能指标展示
        st.markdown('<div class="sub-header">📊 性能指标对比</div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = 95.2,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "实体识别准确率"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#667eea"},
                    'steps': [
                        {'range': [0, 70], 'color': "lightgray"},
                        {'range': [70, 90], 'color': "gray"},
                        {'range': [90, 100], 'color': "lightgreen"}],
                }
            ))
            fig.update_layout(height=250)
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = 94.8,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "关系抽取F1值"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#667eea"},
                }
            ))
            fig.update_layout(height=250)
            st.plotly_chart(fig, use_container_width=True)
            
        with col3:
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = 87.3,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "风险预警准确率"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#667eea"},
                }
            ))
            fig.update_layout(height=250)
            st.plotly_chart(fig, use_container_width=True)
            
        with col4:
            fig = go.Figure(go.Indicator(
                mode = "number+delta",
                value = 0.3,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "平均响应时间(秒)"},
                delta = {'reference': 2.1, 'position': "bottom"},
                number = {'suffix': "s"}
            ))
            fig.update_layout(height=250)
            st.plotly_chart(fig, use_container_width=True)
        
        # 技术优势展示
        st.markdown('<div class="sub-header">🚀 技术优势与创新</div>', unsafe_allow_html=True)
        
        advantages = [
            {
                "title": "BERT-BiLSTM-CRF混合模型",
                "description": "结合预训练语言模型和序列标注优势，实现95.2%的实体识别准确率",
                "icon": "🧠"
            },
            {
                "title": "多模态数据融合",
                "description": "整合文本、数值、时序数据，提供全方位风险画像",
                "icon": "🔗"
            },
            {
                "title": "实时流处理",
                "description": "基于Apache Flink实现毫秒级风险识别与预警",
                "icon": "⚡"
            },
            {
                "title": "可解释AI",
                "description": "提供风险决策依据可视化，增强模型可信度",
                "icon": "🔍"
            }
        ]
        
        cols = st.columns(2)
        for i, advantage in enumerate(advantages):
            with cols[i % 2]:
                st.markdown(f"""
                <div style="background: white; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                        <span style="font-size: 2rem; margin-right: 1rem;">{advantage['icon']}</span>
                        <h5 style="color: #2c3e50; margin: 0;">{advantage['title']}</h5>
                    </div>
                    <p style="color: #555; line-height: 1.6;">{advantage['description']}</p>
                </div>
                """, unsafe_allow_html=True)

def main():
    # 高级侧边栏
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h1 style="color: white; margin-bottom: 0.5rem;">🔮 灵嗅</h1>
            <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">金融风险智能监测平台</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 导航菜单
        st.markdown("### 🧭 导航菜单")
        page = st.selectbox(
            "选择页面",
            ["风险监测仪表盘", "技术架构展示", "预警管理中心", "数据分析报告", "系统设置"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # 实时数据状态
        st.markdown("### 📡 系统状态")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("数据流", "正常", delta="实时")
        with col2:
            st.metric("API状态", "在线", delta="稳定")
        
        # 数据更新时间
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin-top: 1rem;">
            <p style="color: white; margin: 0; font-size: 0.9rem;">🕐 最后更新</p>
            <p style="color: white; margin: 0; font-weight: 700;">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 实例化监测系统
    monitor = AdvancedFinancialRiskMonitor()
    
    # 页面路由
    if page == "风险监测仪表盘":
        st.markdown('<div class="main-header">🔮 灵嗅金融风险智能监测平台</div>', unsafe_allow_html=True)
        monitor.create_advanced_dashboard()
        monitor.create_risk_heatmap()
        
    elif page == "技术架构展示":
        st.markdown('<div class="main-header">🛠️ 技术架构与核心能力</div>', unsafe_allow_html=True)
        monitor.create_technical_dashboard()
        
    elif page == "预警管理中心":
        st.markdown('<div class="main-header">⚠️ 智能预警管理中心</div>', unsafe_allow_html=True)
        
        # 预警统计概览
        col1, col2, col3, col4 = st.columns(4)
        
        # 计算风险数据
        high_risk_count = len(monitor.alerts_data[monitor.alerts_data['风险等级'] == '高'])
        high_risk_pending = len(monitor.alerts_data[(monitor.alerts_data['风险等级'] == '高') & (monitor.alerts_data['处置状态'] == '待处理')])
        medium_risk_count = len(monitor.alerts_data[monitor.alerts_data['风险等级'] == '中'])
        medium_risk_pending = len(monitor.alerts_data[(monitor.alerts_data['风险等级'] == '中') & (monitor.alerts_data['处置状态'] == '待处理')])
        low_risk_count = len(monitor.alerts_data[monitor.alerts_data['风险等级'] == '低'])
        low_risk_pending = len(monitor.alerts_data[(monitor.alerts_data['风险等级'] == '低') & (monitor.alerts_data['处置状态'] == '待处理')])
        total_alerts = len(monitor.alerts_data)
        resolved_alerts = len(monitor.alerts_data[monitor.alerts_data['处置状态'] == '已处理'])
        completion_rate = resolved_alerts/total_alerts*100 if total_alerts > 0 else 0
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">🔴</div>
                <div style="font-size: 1.2rem; opacity: 0.9;">高风险预警</div>
                <div style="font-size: 2rem; font-weight: 800; margin: 0.5rem 0;">{high_risk_count}</div>
                <div style="font-size: 1rem; opacity: 0.8;">待处理: {high_risk_pending}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">🟡</div>
                <div style="font-size: 1.2rem; opacity: 0.9;">中风险预警</div>
                <div style="font-size: 2rem; font-weight: 800; margin: 0.5rem 0;">{medium_risk_count}</div>
                <div style="font-size: 1rem; opacity: 0.8;">待处理: {medium_risk_pending}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">🟢</div>
                <div style="font-size: 1.2rem; opacity: 0.9;">低风险预警</div>
                <div style="font-size: 2rem; font-weight: 800; margin: 0.5rem 0;">{low_risk_count}</div>
                <div style="font-size: 1rem; opacity: 0.8;">待处理: {low_risk_pending}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">📈</div>
                <div style="font-size: 1.2rem; opacity: 0.9;">处理进度</div>
                <div style="font-size: 2rem; font-weight: 800; margin: 0.5rem 0;">{resolved_alerts}/{total_alerts}</div>
                <div style="font-size: 1rem; opacity: 0.8;">完成率: {completion_rate:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<div class="sub-header">📋 预警事件总览</div>', unsafe_allow_html=True)
            
            # 显示预警表格
            display_data = monitor.alerts_data.copy()
            display_data['时间'] = display_data['时间'].dt.strftime('%Y-%m-%d %H:%M')
            st.dataframe(display_data, use_container_width=True, height=400)
            
        with col2:
            st.markdown('<div class="sub-header">🔔 预警统计分析</div>', unsafe_allow_html=True)
            
            # 风险等级分布统计
            alert_stats = monitor.alerts_data['风险等级'].value_counts()
            fig = px.pie(
                values=alert_stats.values,
                names=alert_stats.index,
                title="风险等级分布",
                color=alert_stats.index,
                color_discrete_map={'高':'#e74c3c', '中':'#f39c12', '低':'#27ae60'}
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            
            # 处置状态统计
            status_stats = monitor.alerts_data['处置状态'].value_counts()
            fig2 = px.bar(
                x=status_stats.values,
                y=status_stats.index,
                orientation='h',
                title="处置状态统计",
                color=status_stats.index,
                color_discrete_sequence=['#27ae60', '#f39c12', '#e74c3c']
            )
            fig2.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)
            
    elif page == "数据分析报告":
        st.markdown('<div class="main-header">📊 智能分析报告</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 风险趋势深度分析")
            st.markdown("""
            <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <h4 style="color: #2c3e50; border-bottom: 2px solid #667eea; padding-bottom: 0.5rem;">核心发现</h4>
                
                <div style="margin: 1.5rem 0;">
                    <h5 style="color: #ff6b6b; margin-bottom: 0.5rem;">🚨 高风险信号</h5>
                    <ul style="color: #555;">
                        <li>市场风险指数月环比上升<strong>15.2%</strong></li>
                        <li>3家中小银行流动性覆盖率逼近监管红线</li>
                        <li>信用债市场违约风险显著提升</li>
                    </ul>
                </div>
                
                <div style="margin: 1.5rem 0;">
                    <h5 style="color: #ffa726; margin-bottom: 0.5rem;">📊 趋势分析</h5>
                    <ul style="color: #555;">
                        <li>系统性风险传导效应持续增强</li>
                        <li>操作风险集中在科技系统领域</li>
                        <li>合规风险受新监管政策影响显著</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("### 🤖 AI模型性能报告")
            st.markdown("""
            <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <h4 style="color: #2c3e50; border-bottom: 2px solid #667eea; padding-bottom: 0.5rem;">性能指标</h4>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1.5rem 0;">
                    <div style="text-align: center; padding: 1rem; background: #e8f5e8; border-radius: 10px;">
                        <div style="font-size: 2rem; font-weight: 800; color: #4caf50;">95.2%</div>
                        <div style="color: #555;">实体识别准确率</div>
                    </div>
                    <div style="text-align: center; padding: 1rem; background: #e3f2fd; border-radius: 10px;">
                        <div style="font-size: 2rem; font-weight: 800; color: #2196f3;">94.8%</div>
                        <div style="color: #555;">关系抽取F1值</div>
                    </div>
                    <div style="text-align: center; padding: 1rem; background: #fff3e0; border-radius: 10px;">
                        <div style="font-size: 2rem; font-weight: 800; color: #ff9800;">87.3%</div>
                        <div style="color: #555;">风险预警准确率</div>
                    </div>
                    <div style="text-align: center; padding: 1rem; background: #fce4ec; border-radius: 10px;">
                        <div style="font-size: 2rem; font-weight: 800; color: #e91e63;">0.3s</div>
                        <div style="color: #555;">平均响应时间</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
    elif page == "系统设置":
        st.markdown('<div class="main-header">⚙️ 系统配置与管理</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔧 系统参数配置")
            
            st.number_input("风险预警阈值", min_value=0, max_value=100, value=75)
            st.slider("数据刷新频率(秒)", min_value=1, max_value=60, value=5)
            st.selectbox("默认风险等级", ["高", "中", "低"])
            st.text_input("API端点地址", value="https://api.lingxiu-risk.com/v1")
            
            if st.button("💾 保存配置", use_container_width=True):
                st.success("系统配置已保存！")
                
        with col2:
            st.markdown("### 👥 用户权限管理")
            
            st.text_input("用户名", value="admin")
            st.text_input("密码", type="password")
            st.selectbox("用户角色", ["管理员", "分析师", "观察员"])
            st.multiselect("数据访问权限", 
                          ["市场数据", "信用数据", "流动性数据", "操作数据", "系统数据"])
            
            if st.button("👤 创建用户", use_container_width=True):
                st.success("用户创建成功！")

    # 添加页脚
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem; padding: 1rem;">
        <p>🔮 灵嗅金融风险监测系统 | BERT-BiLSTM-CRF混合模型驱动 | © 2024 灵嗅科技</p>
        <p>风险预警提前72小时 | 实体识别准确率95.2% | 系统可用性99.95%</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
