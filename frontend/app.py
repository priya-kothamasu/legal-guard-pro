import streamlit as st
import os
from backend.analyzer import LegalAnalyzer
from backend.utils import scrape_url

st.set_page_config(page_title="LegalGuard AI Pro", page_icon="⚖️", layout="wide")

@st.cache_resource
def load_analyzer():
    return LegalAnalyzer()

analyzer = load_analyzer()

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .score-circle { border: 5px solid #238636; border-radius: 50%; width: 140px; height: 140px; display: flex; align-items: center; justify-content: center; margin: auto; background: #010409; }
    .evidence-card { border-left: 4px solid #f85149; background: #161b22; padding: 15px; margin-bottom: 12px; border-radius: 4px; border: 1px solid #30363d; }
    .quote { font-style: italic; color: #8b949e; font-size: 0.92rem; line-height: 1.4; display: block; margin-top: 5px; }
    .risk-tag { color: #f85149; font-size: 0.7rem; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ LegalGuard AI Pro")
st.caption("Neural Audit & Risk Quantification Dashboard")
st.divider()

col_l, col_r = st.columns([1, 1.4], gap="large")

with col_l:
    st.subheader("Input Audit Material")
    src = st.radio("Mode", ["Manual Text", "Web URL", "PDF Document"], horizontal=True)
    
    content = ""
    uploaded_file = None

    if src == "Manual Text":
        content = st.text_area("Paste Clauses", height=450, placeholder="Paste legal text here...")
    elif src == "Web URL":
        content = st.text_input("URL Link", placeholder="https://example.com/terms")
    else:
        uploaded_file = st.file_uploader("Upload Policy PDF", type=["pdf"])

    if st.button("Execute Neural Audit", use_container_width=True):
        text = ""
        if src == "PDF Document" and uploaded_file:
            with st.spinner("Extracting PDF content..."):
                text = analyzer.extract_pdf_text(uploaded_file.getvalue())
        elif src == "Web URL" and content:
            with st.spinner("Scraping URL..."):
                text = scrape_url(content)
        elif content:
            text = content
        
        if not text:
            st.error("Please provide valid input to audit.")
        else:
            with st.spinner("Analyzing risk linguistic patterns..."):
                findings = analyzer.analyze_text(text)
                evidence = analyzer.get_evidence(text)
                
                # Calculate Score
                score = 100
                for f in findings:
                    score -= 15 if f['risk'] == "High" else 7
                score -= (len(evidence) * 2)
                
                st.session_state.audit = {
                    "score": max(score, 12),
                    "findings": findings,
                    "evidence": evidence
                }

with col_r:
    if "audit" in st.session_state:
        data = st.session_state.audit
        