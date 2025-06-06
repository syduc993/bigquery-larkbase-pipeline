import streamlit as st
import pandas as pd
from typing import Optional

def render_status_card(title: str, status: str, is_connected: bool):
    """Render status card với Material UI styling"""
    status_icon = "🟢" if is_connected else "🔴"
    card_class = "metric-card"
    
    st.markdown(f"""
    <div class="{card_class}">
        <h4>{title}</h4>
        <p>{status_icon} {status}</p>
    </div>
    """, unsafe_allow_html=True)

def render_data_preview(df: pd.DataFrame, title: str = "📋 Xem trước dữ liệu"):
    """Render data preview với styling"""
    if df is not None and not df.empty:
        st.markdown(f"### {title}")
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📝 Số dòng", len(df))
        with col2:
            st.metric("📋 Số cột", len(df.columns))
        with col3:
            memory_usage = df.memory_usage(deep=True).sum() / 1024
            st.metric("💾 Kích thước", f"{memory_usage:.1f} KB")
        
        # Data display
        st.dataframe(
            df.head(10),
            use_container_width=True,
            height=400
        )
        
        return True
    return False

def render_query_builder():
    """Render query builder interface"""
    st.markdown("### 🔧 Query Builder")
    
    col1, col2 = st.columns(2)
    
    with col1:
        query_type = st.selectbox(
            "Loại truy vấn",
            ["Custom SQL", "Select Table", "Sample Queries"]
        )
    
    with col2:
        if query_type == "Sample Queries":
            sample_query = st.selectbox(
                "Mẫu truy vấn",
                [
                    "Shakespeare Sample",
                    "Weather Data",
                    "GitHub Repos",
                    "Stack Overflow"
                ]
            )
    
    if query_type == "Custom SQL":
        query = st.text_area(
            "SQL Query",
            value="SELECT * FROM `bigquery-public-data.samples.shakespeare` LIMIT 100",
            height=150,
            help="Nhập câu query SQL để lấy dữ liệu từ BigQuery"
        )
    elif query_type == "Sample Queries":
        sample_queries = {
            "Shakespeare Sample": "SELECT * FROM `bigquery-public-data.samples.shakespeare` LIMIT 100",
            "Weather Data": "SELECT * FROM `bigquery-public-data.noaa_gsod.gsod2020` LIMIT 100",
            "GitHub Repos": "SELECT * FROM `bigquery-public-data.github_repos.sample_repos` LIMIT 100",
            "Stack Overflow": "SELECT * FROM `bigquery-public-data.stackoverflow.posts_questions` LIMIT 100"
        }
        query = sample_queries.get(sample_query, "")
        st.code(query, language="sql")
    
    return query

def render_transfer_section():
    """Render transfer controls"""
    st.markdown("## 🚀 Đồng bộ dữ liệu")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        transfer_button = st.button(
            "📤 Chuyển dữ liệu sang Larkbase", 
            type="primary", 
            use_container_width=True
        )
    
    return transfer_button
