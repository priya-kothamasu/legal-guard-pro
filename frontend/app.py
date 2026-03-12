import streamlit as st
import requests

st.set_page_config(page_title="LegalGuard AI Pro", page_icon="⚖️", layout="wide")

# Modern Enterprise Styling
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
    
    # FIX: Initialize variables at the top to avoid NameError
    content = ""
    uploaded_file = None
    data_payload = {"source_type": src.lower()}
    files_payload = None

    if src == "Manual Text":
        content = st.text_area("Paste Clauses", height=450, placeholder="Paste legal text here...")
        data_payload["content"] = content
    elif src == "Web URL":
        content = st.text_input("URL Link", placeholder="https://example.com/terms")
        data_payload["content"] = content
    else:
        uploaded_file = st.file_uploader("Upload Policy PDF", type=["pdf"])
        if uploaded_file:
            files_payload = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}

    if st.button("Execute Neural Audit", use_container_width=True):
        # FIX: Correct check for all input types
        if src == "PDF Document" and not uploaded_file:
            st.error("Please upload a PDF file first.")
        elif src != "PDF Document" and not content:
            st.error("Please provide text or a URL to audit.")
        else:
            with st.spinner("Analyzing risk linguistic patterns..."):
                try:
                    res = requests.post("http://127.0.0.1:8000/analyze", data=data_payload, files=files_payload)
                    if res.status_code == 200:
                        st.session_state.audit = res.json()
                    else:
                        st.error(f"Engine Error: {res.status_code}")
                except Exception as e:
                    st.error("Engine Offline. Ensure backend/main.py is running in Terminal 1.")

with col_r:
    if "audit" in st.session_state:
        data = st.session_state.audit
        if "error" in data:
            st.error(data["error"])
        else:
            c1, c2 = st.columns([1, 2.5])
            with c1:
                score = data.get('score', 100)
                color = "#f85149" if score < 50 else "#d29922" if score < 75 else "#238636"
                st.markdown(f"<div class='score-circle' style='border-color:{color}; text-align:center;'><div style='font-size:2.8rem; font-weight:bold; color:{color};'>{score}</div></div>", unsafe_allow_html=True)
                st.markdown("<p style='text-align:center; color:#8b949e; margin-top:10px; font-size:0.8rem;'>SAFETY RATING</p>", unsafe_allow_html=True)
            
            with c2:
                st.markdown("### Risk Evidence")
                evidence = data.get('evidence', [])
                if evidence:
                    for ev in evidence:
                        st.markdown(f"""
                            <div class='evidence-card'>
                                <span class='risk-tag'>{ev['type']} IDENTIFIED</span>
                                <span class='quote'>"{ev['quote']}"</span>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.success("No high-risk clauses extracted from this section.")
            
            st.divider()
            st.subheader("Neural Risk Matrix")
            findings = data.get('findings', [])
            for f in findings:
                with st.expander(f"{f['category']} Audit"):
                    risk_color = "#f85149" if f['risk'] == "High" else "#d29922"
                    st.markdown(f"**Threat Level:** <span style='color:{risk_color}'>{f['risk']}</span>", unsafe_allow_html=True)
                    st.write(f['text'])
                    st.progress(f['confidence']/100)
                    st.caption(f"Machine Confidence: {f['confidence']}%")
    else:
        st.markdown("""
            <div style='text-align:center; padding-top:120px; color:#484f58;'>
                <h3>System Ready</h3>
                <p>Upload a document or paste text to generate risk intelligence.</p>
            </div>
        """, unsafe_allow_html=True)