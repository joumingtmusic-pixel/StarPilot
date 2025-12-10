"""
銷售數據分析儀表板 - Streamlit 範例
可直接部署到 Streamlit Cloud

使用方式：
1. 確保有 data/sales.csv 檔案
2. 本地測試：streamlit run streamlit_範例_銷售儀表板.py
3. 部署到 Streamlit Cloud
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# 頁面設定
st.set_page_config(
    page_title="銷售數據分析儀表板",
    page_icon="📊",
    layout="wide"
)

# 標題
st.title("📊 銷售數據分析儀表板")
st.markdown("---")

# 載入資料


@st.cache_data
def load_data():
    """載入銷售資料"""
    # 嘗試從不同路徑載入
    possible_paths = [
        "data/sales.csv",
        "../data/sales.csv",
        "../../data/sales.csv"
    ]

    for path in possible_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            # 確保日期格式正確
            if '日期' in df.columns:
                df['日期'] = pd.to_datetime(df['日期'])
            elif 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
            return df

    # 如果找不到檔案，使用範例資料
    st.warning("⚠️ 找不到 sales.csv，使用範例資料")
    return create_sample_data()


def create_sample_data():
    """建立範例資料"""
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    products = ['產品A', '產品B', '產品C', '產品D', '產品E']

    data = []
    for date in dates:
        for product in products:
            data.append({
                '日期': date,
                '產品': product,
                '數量': pd.np.random.randint(10, 100),
                '金額': pd.np.random.randint(1000, 10000)
            })

    return pd.DataFrame(data)


# 載入資料
try:
    df = load_data()

    # 資料預處理
    if '日期' in df.columns:
        df['年月'] = df['日期'].dt.to_period('M').astype(str)
        df['年'] = df['日期'].dt.year
        df['月'] = df['日期'].dt.month

    # 側邊欄 - 篩選器
    st.sidebar.header("📋 資料篩選")

    # 年份篩選
    if '年' in df.columns:
        years = sorted(df['年'].unique())
        selected_year = st.sidebar.selectbox("選擇年份", years, index=len(years)-1)
        df_filtered = df[df['年'] == selected_year]
    else:
        df_filtered = df

    # 產品篩選
    if '產品' in df.columns:
        all_products = ['全部'] + sorted(df_filtered['產品'].unique().tolist())
        selected_product = st.sidebar.selectbox("選擇產品", all_products)
        if selected_product != '全部':
            df_filtered = df_filtered[df_filtered['產品'] == selected_product]

    # 重新整理按鈕
    if st.sidebar.button("🔄 重新整理資料"):
        st.cache_data.clear()
        st.rerun()

    # 主要指標
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_sales = df_filtered['金額'].sum()
        st.metric("總銷售額", f"NT$ {total_sales:,.0f}")

    with col2:
        total_quantity = df_filtered['數量'].sum()
        st.metric("總銷售數量", f"{total_quantity:,.0f}")

    with col3:
        avg_order = df_filtered['金額'].mean()
        st.metric("平均訂單金額", f"NT$ {avg_order:,.0f}")

    with col4:
        total_orders = len(df_filtered)
        st.metric("訂單總數", f"{total_orders:,}")

    st.markdown("---")

    # 圖表區域
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 每月銷售趨勢")
        if '年月' in df_filtered.columns:
            monthly_sales = df_filtered.groupby('年月')['金額'].sum().reset_index()
            fig1 = px.line(
                monthly_sales,
                x='年月',
                y='金額',
                markers=True,
                title="每月銷售額變化"
            )
            fig1.update_layout(
                xaxis_title="月份",
                yaxis_title="銷售額 (NT$)",
                hovermode='x unified'
            )
            st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("🏆 產品銷售排名")
        if '產品' in df_filtered.columns:
            product_sales = df_filtered.groupby(
                '產品')['金額'].sum().sort_values(ascending=False).head(10)
            fig2 = px.bar(
                x=product_sales.values,
                y=product_sales.index,
                orientation='h',
                title="前 10 名產品銷售額",
                labels={'x': '銷售額 (NT$)', 'y': '產品'}
            )
            fig2.update_layout(showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)

    # 詳細數據表
    st.subheader("📋 詳細數據")

    # 統計摘要
    if '產品' in df_filtered.columns:
        summary = df_filtered.groupby('產品').agg({
            '數量': 'sum',
            '金額': ['sum', 'mean', 'count']
        }).round(2)
        summary.columns = ['總數量', '總金額', '平均金額', '訂單數']
        summary = summary.sort_values('總金額', ascending=False)
        st.dataframe(summary, use_container_width=True)

    # 匯出功能
    st.markdown("---")
    col1, col2 = st.columns([3, 1])

    with col1:
        st.info("💡 提示：你可以直接在表格上排序和篩選資料")

    with col2:
        # 轉換為 CSV
        csv = df_filtered.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 下載篩選後的資料",
            data=csv,
            file_name=f"sales_filtered_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

except Exception as e:
    st.error(f"❌ 載入資料時發生錯誤：{str(e)}")
    st.info("請確保 data/sales.csv 檔案存在，或系統會自動使用範例資料")

# 頁尾
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    <p>📊 銷售數據分析儀表板 | 由 AI 協作開發 | 
    <a href='https://github.com/yourusername/StarPilot' target='_blank'>StarPilot 專案</a>
    </p>
    </div>
    """,
    unsafe_allow_html=True
)
