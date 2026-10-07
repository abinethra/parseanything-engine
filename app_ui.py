import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="ParseAnything | Enterprise Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Persistent Session State
if "history" not in st.session_state:
    st.session_state.history = []

if "api_url" not in st.session_state:
    st.session_state.api_url = "http://127.0.0.1:8000"

if "api_key" not in st.session_state:
    st.session_state.api_key = "pa_live_8943f2a1e902bc"

# Global Universal CSS Override
st.markdown("""
<style>
    /* Force Light Mode Core Background */
    .stApp {
        background-color: #F8F6F0 !important;
    }
    
    /* Universal Text Blackout Override */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
    .stApp p, .stApp span, .stApp label, .stApp div, .stApp caption {
        color: #1E1E1E !important;
    }

    /* Dark Left Sidebar Structure */
    [data-testid="stSidebar"] {
        background-color: #888681 !important;
    }
    [data-testid="stSidebar"] * {
        color: #E0E0E0 !important;
    }

    /* Fixed High-Contrast Bento Cards */
    .bento-card {
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 16px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
    }
    
    .card-yellow { background-color: #F6E69F !important; }
    .card-yellow * { color: #3D3200 !important; }

    .card-pink { background-color: #F6CEDC !important; }
    .card-pink * { color: #52182B !important; }

    .card-green { background-color: #C9E2BD !important; }
    .card-green * { color: #1B3811 !important; }

    .card-blue { background-color: #CBDCEB !important; }
    .card-blue * { color: #12283A !important; }

    .card-white { background-color: #FFFFFF !important; border: 1px solid #E2DEC9; }
    .card-white * { color: #1E1E1E !important; }

    .metric-title {
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    .metric-value {
        font-size: 34px;
        font-weight: 800;
        margin-top: 6px;
        margin-bottom: 2px;
    }
    .metric-subtitle {
        font-size: 12px;
        font-weight: 500;
        opacity: 0.85;
    }

    /* Input Fields & Buttons */
    .stTextInput input, .stSelectbox div {
        background-color: #FFFFFF !important;
        color: #685656 !important;
        border: 1px solid #CCC !important;
    }
    
    .stButton>button {
        background-color: #161616 !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        width: 100%;
    }
    .stButton>button * {
        color: #FFFFFF !important;
    }
    .stButton>button:hover {
        background-color: #333333 !important;
    }
</style>
""", unsafe_allow_html=True)

# Navigation Sidebar
with st.sidebar:
    st.title("parseanything")
    st.caption("v1.0.0 Enterprise Engine")
    st.divider()
    
    menu = st.radio(
        "GENERAL",
        ["Dashboard", "Ingestion Hub", "Document Library", "API Keys & Settings"],
        index=0
    )
    
    st.divider()
    
    backend_status = "🔴 Offline"
    try:
        r = requests.get(f"{st.session_state.api_url}/health", timeout=2)
        if r.status_code == 200:
            backend_status = "🟢 API Service: Running"
    except:
        backend_status = "🔴 API Offline"

    st.info(f"{backend_status}\n`{st.session_state.api_url}`")

# 1. Dashboard View
if menu == "Dashboard":
    st.markdown("## Good morning, Team 👋")
    st.caption("Real-time document processing metrics and live extraction overview.")

    col_main, col_right = st.columns([2.5, 1])

    with col_main:
        total_ingested = len(st.session_state.history)
        avg_blocks = sum([item['blocks'] for item in st.session_state.history]) / max(total_ingested, 1)

        r1_col1, r1_col2 = st.columns(2)
        with r1_col1:
            st.markdown(f"""
            <div class="bento-card card-yellow">
                <div class="metric-title">Documents Ingested</div>
                <div class="metric-value">{total_ingested}</div>
                <div class="metric-subtitle">Active session uploads</div>
            </div>
            """, unsafe_allow_html=True)

        with r1_col2:
            st.markdown(f"""
            <div class="bento-card card-pink">
                <div class="metric-title">Avg Extracted Blocks</div>
                <div class="metric-value">{avg_blocks:.1f}</div>
                <div class="metric-subtitle">Blocks per document</div>
            </div>
            """, unsafe_allow_html=True)

        r2_col1, r2_col2 = st.columns(2)
        with r2_col1:
            st.markdown("""
            <div class="bento-card card-green">
                <div class="metric-title">Engine Speed</div>
                <div class="metric-value">< 0.25s</div>
                <div class="metric-subtitle">FastAPI native processing</div>
            </div>
            """, unsafe_allow_html=True)

        with r2_col2:
            st.markdown("""
            <div class="bento-card card-blue">
                <div class="metric-title">Supported Formats</div>
                <div class="metric-value">6 Types</div>
                <div class="metric-subtitle">PDF, DOCX, PPTX, XLSX, CSV, MSG</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("### Live Session Ingestion History")
        if len(st.session_state.history) > 0:
            df_hist = pd.DataFrame(st.session_state.history)[["timestamp", "file_name", "type", "blocks", "status"]]
            st.dataframe(df_hist, use_container_width=True, hide_index=True)
        else:
            st.info("No documents processed yet. Use the Quick Ingest panel on the right or go to Ingestion Hub.")

    with col_right:
        st.markdown("""
        <div class="bento-card card-white">
            <h4 style="margin-top:0;">Quick Ingest</h4>
            <p style="font-size:13px;">Upload a document to extract schema data instantly.</p>
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader("Choose file", type=["pdf", "docx", "pptx", "xlsx", "csv", "msg"], key="dash_upload")

        if uploaded_file is not None:
            if st.button("Parse Document", key="dash_btn"):
                with st.spinner("Ingesting through ParseAnything..."):
                    try:
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                        response = requests.post(f"{st.session_state.api_url}/parse", files=files)
                        if response.status_code == 200:
                            data = response.json()
                            
                            entry = {
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "file_name": uploaded_file.name,
                                "type": uploaded_file.name.split('.')[-1].upper(),
                                "blocks": data.get("total_blocks", 0),
                                "status": data.get("status", "success"),
                                "raw_json": data
                            }
                            st.session_state.history.insert(0, entry)
                            
                            st.success("Document parsed successfully!")
                            st.rerun()
                        else:
                            st.error(f"API Error ({response.status_code}): {response.text}")
                    except Exception as e:
                        st.error(f"Connection failed: {e}")

# 2. Ingestion Hub
elif menu == "Ingestion Hub":
    st.markdown("## Ingestion Hub")
    st.caption("Deep inspection tool for parsing documents and reviewing extracted JSON/Markdown.")

    file_to_parse = st.file_uploader("Upload file to inspect", type=["pdf", "docx", "pptx", "xlsx", "csv", "msg"], key="hub_uploader")
    
    if file_to_parse:
        if st.button("Run Full Engine Extraction", key="hub_btn"):
            with st.spinner("Processing..."):
                try:
                    files = {"file": (file_to_parse.name, file_to_parse.getvalue())}
                    res = requests.post(f"{st.session_state.api_url}/parse", files=files)
                    if res.status_code == 200:
                        parsed_data = res.json()
                        
                        entry = {
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "file_name": file_to_parse.name,
                            "type": file_to_parse.name.split('.')[-1].upper(),
                            "blocks": parsed_data.get("total_blocks", 0),
                            "status": parsed_data.get("status", "success"),
                            "raw_json": parsed_data
                        }
                        st.session_state.history.insert(0, entry)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("### Parsed Metadata")
                            st.write(f"**File Name:** {parsed_data.get('file_name')}")
                            st.write(f"**Total Blocks:** {parsed_data.get('total_blocks')}")
                            st.write(f"**Status:** {parsed_data.get('status')}")
                            
                            st.markdown("### Raw Structured JSON")
                            st.json(parsed_data)

                        with col2:
                            st.markdown("### Extracted Text Preview")
                            blocks = parsed_data.get("blocks", [])
                            for b in blocks:
                                st.markdown(f"> **Block {b.get('block_id')} (Page {b.get('page_number')}):** {b.get('text')}")
                    else:
                        st.error(f"Failed to parse document: {res.text}")
                except Exception as e:
                    st.error(f"Server error: {e}")

# 3. Document Library
elif menu == "Document Library":
    st.markdown("## Document Library")
    st.caption("Search, filter, and export data from all documents parsed in this session.")

    if len(st.session_state.history) == 0:
        st.info("No documents stored in library yet. Ingest documents via Dashboard or Ingestion Hub.")
    else:
        search_query = st.text_input("Search documents by file name...", "")
        
        filtered = [item for item in st.session_state.history if search_query.lower() in item["file_name"].lower()]
        
        st.markdown(f"**Found {len(filtered)} document(s)**")
        
        for idx, doc in enumerate(filtered):
            with st.expander(f"📄 {doc['file_name']} — Ingested at {doc['timestamp']}"):
                col_a, col_b = st.columns([1, 2])
                with col_a:
                    st.write(f"**Type:** {doc['type']}")
                    st.write(f"**Total Blocks:** {doc['blocks']}")
                    st.write(f"**Status:** {doc['status']}")
                    
                    json_str = json.dumps(doc['raw_json'], indent=2)
                    st.download_button(
                        label="Download JSON Data",
                        data=json_str,
                        file_name=f"{doc['file_name']}_parsed.json",
                        mime="application/json",
                        key=f"dl_{idx}"
                    )
                with col_b:
                    st.json(doc['raw_json'])

# 4. API Keys & Settings
elif menu == "API Keys & Settings":
    st.markdown("## API Keys & System Settings")
    st.caption("Configure environment parameters, FastAPI endpoint links, and authentication tokens.")

    with st.form("settings_form"):
        st.markdown("### Engine API Configuration")
        new_url = st.text_input("FastAPI Service Endpoint Base URL", value=st.session_state.api_url)
        new_key = st.text_input("API Key (Secret Token)", value=st.session_state.api_key, type="password")
        
        st.markdown("### Execution Settings")
        max_workers = st.slider("Max Concurrent Worker Threads", min_value=1, max_value=16, value=4)
        enable_ocr = st.checkbox("Enable OCR Fallback for Scanned PDF Pages", value=True)
        
        submitted = st.form_submit_button("Save Configuration")
        if submitted:
            st.session_state.api_url = new_url
            st.session_state.api_key = new_key
            st.success("Settings saved successfully!")
