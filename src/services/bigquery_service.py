import streamlit as st
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from typing import Optional

class BigQueryService:
    """Service xử lý kết nối và truy vấn BigQuery"""
    
    def __init__(self):
        self.client = self._init_client()
    
    def _init_client(self) -> Optional[bigquery.Client]:
        """Khởi tạo BigQuery client từ secrets - KHÔNG dùng cache"""
        try:
            credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"]
            )
            return bigquery.Client(credentials=credentials)
        except Exception as e:
            st.error(f"❌ Lỗi kết nối BigQuery: {str(e)}")
            return None
    
    @st.cache_data(ttl=300)
    def execute_query(_self, query: str) -> Optional[pd.DataFrame]:
        """Thực thi query BigQuery với cache"""
        if not _self.client:
            return None
        
        try:
            query_job = _self.client.query(query)
            results = query_job.result()
            df = results.to_dataframe()
            return df
        except Exception as e:
            st.error(f"❌ Lỗi thực thi query: {str(e)}")
            return None
