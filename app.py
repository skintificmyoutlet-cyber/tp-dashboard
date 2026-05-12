import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from google_sheets_reader import GoogleSheetsReader

st.set_page_config(page_title="TP投放数据看板", layout="wide", page_icon="📊")

@st.cache_resource
def get_reader():
    return GoogleSheetsReader()

@st.cache_data(ttl=3600)
def load_data(market, channel):
    reader = get_reader()
    if channel == 'FB':
        return reader.get_fb_data(market)
    else:
        return reader.get_sp_data(market)

def calculate_metrics(df, date_col, spend_col, revenue_col=None):
    if df.empty:
        return {}

    df_sorted = df.sort_values(date_col)
    latest_date = df_sorted[date_col].max()
    prev_date = latest_date - timedelta(days=1)

    latest_data = df_sorted[df_sorted[date_col] == latest_date]
    prev_data = df_sorted[df_sorted[date_col] == prev_date]

    metrics = {
        'latest_date': latest_date,
        'spend': latest_data[spend_col].sum() if not latest_data.empty else 0,
        'prev_spend': prev_data[spend_col].sum() if not prev_data.empty else 0,
    }

    if revenue_col and revenue_col in df.columns:
        metrics['revenue'] = latest_data[revenue_col].sum() if not latest_data.empty else 0
        metrics['prev_revenue'] = prev_data[revenue_col].sum() if not prev_data.empty else 0
        metrics['roas'] = metrics['revenue'] / metrics['spend'] if metrics['spend'] > 0 else 0
        metrics['prev_roas'] = metrics['prev_revenue'] / metrics['prev_spend'] if metrics['prev_spend'] > 0 else 0

    return metrics

st.title("📊 TP投放数据看板")
st.markdown("---")

markets = ['ID', 'MY', 'TH']
channels = ['FB', 'SP']

col1, col2, col3 = st.columns(3)
with col1:
    selected_market = st.selectbox("选择市场", markets)
with col2:
    selected_channel = st.selectbox("选择渠道", channels)
with col3:
    view_mode = st.radio("查看模式", ["昨日数据", "上周汇总"], horizontal=True)

try:
    df = load_data(selected_market, selected_channel)

    if df.empty:
        st.warning(f"暂无 {selected_channel}-{selected_market} 数据")
    else:
        date_col = 'date' if selected_channel == 'FB' else 'run_date'
        spend_col = 'spend' if selected_channel == 'FB' else 'expense'

        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df = df.dropna(subset=[date_col])

        if view_mode == "昨日数据":
            latest_date = df[date_col].max()
            df_filtered = df[df[date_col] == latest_date]
            st.subheader(f"📅 {latest_date.strftime('%Y-%m-%d')} 数据")
        else:
            today = datetime.now()
            last_monday = today - timedelta(days=today.weekday() + 7)
            last_sunday = last_monday + timedelta(days=6)
            df_filtered = df[(df[date_col] >= last_monday) & (df[date_col] <= last_sunday)]
            st.subheader(f"📅 上周数据 ({last_monday.strftime('%m/%d')} - {last_sunday.strftime('%m/%d')})")

        if selected_channel == 'FB':
            metrics = calculate_metrics(df, date_col, spend_col, 'purchase_value')

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("花费", f"${metrics.get('spend', 0):,.2f}",
                         delta=f"{((metrics.get('spend', 0) - metrics.get('prev_spend', 0)) / metrics.get('prev_spend', 1) * 100):.1f}%")
            with col2:
                st.metric("转化金额", f"${metrics.get('revenue', 0):,.2f}",
                         delta=f"{((metrics.get('revenue', 0) - metrics.get('prev_revenue', 0)) / metrics.get('prev_revenue', 1) * 100):.1f}%")
            with col3:
                st.metric("ROAS", f"{metrics.get('roas', 0):.2f}",
                         delta=f"{(metrics.get('roas', 0) - metrics.get('prev_roas', 0)):.2f}")
            with col4:
                st.metric("购买次数", f"{df_filtered['purchase_count'].sum():.0f}")

            st.markdown("---")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("💰 花费 Top 10 广告")
                if 'ad_name' in df_filtered.columns:
                    top_spend = df_filtered.groupby('ad_name')[spend_col].sum().sort_values(ascending=False).head(10)
                    fig = px.bar(x=top_spend.values, y=top_spend.index, orientation='h',
                               labels={'x': '花费 ($)', 'y': '广告名称'})
                    st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.subheader("🎯 转化 Top 10 广告")
                if 'ad_name' in df_filtered.columns and 'purchase_value' in df_filtered.columns:
                    top_revenue = df_filtered.groupby('ad_name')['purchase_value'].sum().sort_values(ascending=False).head(10)
                    fig = px.bar(x=top_revenue.values, y=top_revenue.index, orientation='h',
                               labels={'x': '转化金额 ($)', 'y': '广告名称'})
                    st.plotly_chart(fig, use_container_width=True)

            st.markdown("---")
            st.subheader("📈 趋势分析")

            daily_stats = df.groupby(date_col).agg({
                spend_col: 'sum',
                'purchase_value': 'sum',
                'impressions': 'sum',
                'clicks': 'sum'
            }).reset_index()
            daily_stats['ROAS'] = daily_stats['purchase_value'] / daily_stats[spend_col]

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=daily_stats[date_col], y=daily_stats[spend_col],
                                   mode='lines+markers', name='花费'))
            fig.add_trace(go.Scatter(x=daily_stats[date_col], y=daily_stats['purchase_value'],
                                   mode='lines+markers', name='转化金额'))
            fig.update_layout(title='花费 vs 转化趋势', xaxis_title='日期', yaxis_title='金额 ($)')
            st.plotly_chart(fig, use_container_width=True)

        else:
            if 'ROAS' in df_filtered.columns:
                avg_roas = df_filtered['ROAS'].mean()
            else:
                avg_roas = 0

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("花费", f"${df_filtered[spend_col].sum():,.2f}")
            with col2:
                st.metric("平均ROAS", f"{avg_roas:.2f}")
            with col3:
                if 'ACOS' in df_filtered.columns:
                    st.metric("平均ACOS", f"{df_filtered['ACOS'].mean():.2%}")
            with col4:
                if 'Product Clicks' in df_filtered.columns:
                    st.metric("总点击", f"{df_filtered['Product Clicks'].sum():.0f}")

            st.markdown("---")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("💰 花费 Top 10 广告")
                if 'Ad Name' in df_filtered.columns:
                    top_spend = df_filtered.groupby('Ad Name')[spend_col].sum().sort_values(ascending=False).head(10)
                    fig = px.bar(x=top_spend.values, y=top_spend.index, orientation='h',
                               labels={'x': '花费 ($)', 'y': '广告名称'})
                    st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.subheader("🎯 ROAS Top 10 广告")
                if 'Ad Name' in df_filtered.columns and 'ROAS' in df_filtered.columns:
                    ad_roas = df_filtered.groupby('Ad Name')['ROAS'].mean().sort_values(ascending=False).head(10)
                    fig = px.bar(x=ad_roas.values, y=ad_roas.index, orientation='h',
                               labels={'x': 'ROAS', 'y': '广告名称'})
                    st.plotly_chart(fig, use_container_width=True)

            st.markdown("---")
            st.subheader("📈 趋势分析")

            daily_stats = df.groupby(date_col).agg({
                spend_col: 'sum',
                'ROAS': 'mean'
            }).reset_index()

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=daily_stats[date_col], y=daily_stats[spend_col],
                                   mode='lines+markers', name='花费'))
            fig.update_layout(title='花费趋势', xaxis_title='日期', yaxis_title='花费 ($)')
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.subheader("📋 原始数据")
        st.dataframe(df_filtered, use_container_width=True)

except FileNotFoundError as e:
    st.error(str(e))
except Exception as e:
    st.error(f"加载数据时出错: {str(e)}")
    st.info("请确保已完成Google API授权")
