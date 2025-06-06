import streamlit as st
import pandas as pd
from src.services.bigquery_service import BigQueryService
from src.services.larkbase_service import LarkbaseAuthenticator, LarkbaseDataWriter
from src.config.larkbase_config import LarkbaseConfig
from src.ui.styles import load_css, render_header, render_footer
from src.ui.components import (
    render_status_card, 
    render_data_preview, 
    render_query_builder,
    render_transfer_section
)

# Cấu hình trang
st.set_page_config(
    page_title="BigQuery to Larkbase",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Load CSS và render header
    load_css()
    render_header()
    
    # Khởi tạo services
    bigquery_service = BigQueryService()
    
    # Sidebar cấu hình
    with st.sidebar:
        st.markdown("## ⚙️ Cấu hình")
        
        # BigQuery Configuration
        st.markdown("### 🔵 BigQuery")
        query = render_query_builder()
        
        # Larkbase Configuration
        st.markdown("### 🟡 Larkbase")
        app_token = st.text_input("App Token", help="Token ứng dụng Larkbase")
        table_id = st.text_input("Table ID", help="ID bảng trong Larkbase")
        
        # Advanced settings
        with st.expander("🔧 Cấu hình nâng cao"):
            custom_app_id = st.text_input("App ID")
            custom_app_secret = st.text_input("App Secret", type="password")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## 📊 Dữ liệu từ BigQuery")
        
        if st.button("🔍 Xem trước dữ liệu", type="primary"):
            with st.spinner("Đang truy vấn BigQuery..."):
                df = bigquery_service.execute_query(query)
                
                if render_data_preview(df):
                    st.session_state['bigquery_data'] = df
                    st.markdown('<div class="status-success">✅ Truy vấn thành công!</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("## 🎯 Trạng thái hệ thống")
        
        # BigQuery status
        bigquery_connected = bigquery_service.client is not None
        render_status_card("BigQuery", "Kết nối" if bigquery_connected else "Lỗi", bigquery_connected)
        
        # Larkbase test
        if st.button("🧪 Test Larkbase"):
            config = LarkbaseConfig(
                app_id=custom_app_id if custom_app_id else None,
                app_secret=custom_app_secret if custom_app_secret else None
            )
            authenticator = LarkbaseAuthenticator(config)
            token = authenticator.authenticate()
            
            if token:
                st.session_state['larkbase_token'] = token
                st.session_state['larkbase_config'] = config
                st.markdown('<div class="status-success">✅ Larkbase kết nối thành công!</div>', unsafe_allow_html=True)
    
    # Transfer section
    if render_transfer_section():
        # Validation
        if 'bigquery_data' not in st.session_state:
            st.error("⚠️ Vui lòng truy vấn dữ liệu BigQuery trước!")
            return
        
        if not app_token or not table_id:
            st.error("⚠️ Vui lòng nhập App Token và Table ID!")
            return
        
        if 'larkbase_token' not in st.session_state:
            st.error("⚠️ Vui lòng test kết nối Larkbase trước!")
            return
        
        # Execute transfer
        df = st.session_state['bigquery_data']
        
        with st.spinner("Đang chuyển dữ liệu..."):
            # Convert DataFrame to Larkbase format
            records = []
            for _, row in df.iterrows():
                record = {}
                for col in df.columns:
                    value = row[col]
                    if pd.isna(value):
                        record[col] = ""
                    else:
                        record[col] = str(value)
                records.append(record)
            
            # Write to Larkbase
            writer = LarkbaseDataWriter(
                st.session_state['larkbase_token'],
                st.session_state['larkbase_config']
            )
            
            success = writer.write_records(app_token, table_id, records)
            
            if success:
                st.success(f"✅ Đã chuyển thành công {len(records)} bản ghi sang Larkbase!")
                st.balloons()
                
                # Statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📊 Tổng bản ghi", len(records))
                with col2:
                    st.metric("⏱️ Thời gian ước tính", f"{len(records)/100:.1f}s")
                with col3:
                    st.metric("✅ Trạng thái", "Thành công")
    
    render_footer()

if __name__ == "__main__":
    main()
