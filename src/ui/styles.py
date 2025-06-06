import streamlit as st

def load_css():
    """Load CSS styles cho Material UI design"""
    st.markdown("""
    <style>
        .main-header {
            background: linear-gradient(90deg, #1976d2 0%, #42a5f5 100%);
            padding: 2rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 4px 20px rgba(25, 118, 210, 0.3);
        }
        
        .metric-card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-left: 4px solid #1976d2;
            margin: 1rem 0;
        }
        
        .status-success {
            background-color: #e8f5e8;
            border-left: 4px solid #4caf50;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        .status-error {
            background-color: #ffebee;
            border-left: 4px solid #f44336;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        .status-warning {
            background-color: #fff3e0;
            border-left: 4px solid #ff9800;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        .stButton > button {
            background: linear-gradient(45deg, #1976d2, #42a5f5);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.5rem 2rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 2px 10px rgba(25, 118, 210, 0.2);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(25, 118, 210, 0.4);
        }
        
        .sidebar .stSelectbox > div > div {
            background-color: #f8f9fa;
            border-radius: 8px;
        }
        
        .stDataFrame {
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """Render header với Material UI styling"""
    st.markdown("""
    <div class="main-header">
        <h1>🔄 BigQuery to Larkbase Data Pipeline</h1>
        <p>Kết nối và đồng bộ dữ liệu từ Google BigQuery sang Larkbase</p>
    </div>
    """, unsafe_allow_html=True)

def render_footer():
    """Render footer"""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>🔄 BigQuery to Larkbase Pipeline | Được xây dựng với ❤️ bằng Streamlit</p>
    </div>
    """, unsafe_allow_html=True)
