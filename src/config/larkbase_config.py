from typing import Dict, Optional
import streamlit as st

class LarkbaseConfig:
    """Cấu hình kết nối Larkbase"""
    
    def __init__(self, app_id: Optional[str] = None, 
                 app_secret: Optional[str] = None, 
                 api_endpoint: Optional[str] = None):
        self.app_id = app_id or st.secrets.get("larkbase", {}).get("default_app_id", "cli_a7fab27260385010")
        self.app_secret = app_secret or st.secrets.get("larkbase", {}).get("default_app_secret", "Zg4MVcFfiOu0g09voTcpfd4WGDpA0Ly5")
        self.api_endpoint = api_endpoint or 'https://open.larksuite.com/open-apis'
    
    def to_dict(self) -> Dict:
        """Chuyển đổi config thành dictionary"""
        return {
            'app_id': self.app_id,
            'app_secret': self.app_secret,
            'api_endpoint': self.api_endpoint
        }
    
    def is_valid(self) -> bool:
        """Kiểm tra tính hợp lệ của config"""
        return bool(self.app_id and self.app_secret and self.api_endpoint)
