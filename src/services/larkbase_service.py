import requests
import streamlit as st
import time
from typing import Dict, List, Optional
from ..config.larkbase_config import LarkbaseConfig

class LarkbaseAuthenticator:
    """Service xác thực với Larkbase API"""
    
    def __init__(self, config: LarkbaseConfig):
        self.config = config
    
    def authenticate(self) -> Optional[str]:
        """Xác thực với API Larkbase để lấy access token"""
        try:
            url = f"{self.config.api_endpoint}/auth/v3/tenant_access_token/internal"
            response = requests.post(url, json={
                'app_id': self.config.app_id, 
                'app_secret': self.config.app_secret
            })
            response.raise_for_status()
            data = response.json()
            
            if data.get('code') == 0:
                return data.get('tenant_access_token')
            else:
                st.error(f"❌ Lỗi API Larkbase: {data.get('msg', 'Không xác định')}")
                return None
        except Exception as e:
            st.error(f"❌ Lỗi xác thực Larkbase: {str(e)}")
            return None

class LarkbaseDataWriter:
    """Service ghi dữ liệu vào Larkbase"""
    
    def __init__(self, access_token: str, config: LarkbaseConfig):
        self.access_token = access_token
        self.config = config
    
    def write_records(self, app_token: str, table_id: str, records: List[Dict]) -> bool:
        """Ghi nhiều bản ghi vào Larkbase với batch processing"""
        try:
            url = f"{self.config.api_endpoint}/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create"
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            batch_size = 500
            total_written = 0
            progress_bar = st.progress(0)
            
            for i in range(0, len(records), batch_size):
                batch = records[i:i + batch_size]
                payload = {"records": [{"fields": record} for record in batch]}
                
                response = requests.post(url, headers=headers, json=payload)
                response.raise_for_status()
                response_data = response.json()
                
                if response_data.get('code') != 0:
                    st.error(f"❌ Lỗi ghi batch {i//batch_size + 1}: {response_data.get('msg')}")
                    return False
                
                total_written += len(batch)
                progress = total_written / len(records)
                progress_bar.progress(progress)
                
                st.info(f"📝 Đã ghi {total_written}/{len(records)} bản ghi")
                time.sleep(0.1)
            
            progress_bar.empty()
            return True
            
        except Exception as e:
            st.error(f"❌ Lỗi ghi dữ liệu: {str(e)}")
            return False

class LarkbaseDataFetcher:
    """Service lấy dữ liệu từ Larkbase"""
    
    def __init__(self, access_token: str, config: LarkbaseConfig):
        self.access_token = access_token
        self.config = config
    
    def fetch_data(self, app_token: str, table_id: str) -> List[Dict]:
        """Lấy tất cả dữ liệu từ Larkbase API với phân trang"""
        all_records = []
        page_token = None
        has_more = True
        
        while has_more:
            try:
                url = f"{self.config.api_endpoint}/bitable/v1/apps/{app_token}/tables/{table_id}/records"
                headers = {'Authorization': f'Bearer {self.access_token}'}
                params = {
                    'page_size': 100,
                    'page_token': page_token
                }

                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()
                response_data = response.json()

                if response_data.get('code') != 0:
                    st.error(f"❌ Lỗi API: {response_data.get('msg', 'Không xác định')}")
                    break

                records = response_data.get('data', {}).get('items', [])
                all_records.extend(records)
                
                has_more = response_data.get('data', {}).get('has_more', False)
                page_token = response_data.get('data', {}).get('page_token')

            except Exception as e:
                st.error(f"❌ Lỗi khi lấy dữ liệu: {str(e)}")
                break
        
        return all_records
