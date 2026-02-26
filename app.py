import streamlit as st
from generator import generate_hbm_sample
from inference import VLMInspector
from database import InspectionDB
from hbm_utils import extract_status, format_for_finetune

# 객체 초기화
db = InspectionDB()
inspector = VLMInspector()

st.set_page_config(page_title="HBM AI Inspector", layout="wide")
st.title("🔬 HBM Intelligent Inspection System")

tab1, tab2 = st.tabs(["Inference", "Active Learning"])

with tab1:
    col_l, col_r = st.columns(2)
    with col_l:
        defect_type = st.selectbox("Target Defect", ["Normal", "Microbump Bridge", "TSV Void"])
        img, tele = generate_hbm_sample(defect_type)
        st.image(img, caption="Real-time Input")
        
    with col_r:
        if st.button("Run AI Analysis"):
            res = inspector.analyze(img, tele)
            status = extract_status(res)
            db.log_result(status, tele['temp'], tele['pressure'], res)
            st.markdown(res)

with tab2:
    st.subheader("User Feedback Loop")
    df = db.get_all_logs()
    st.dataframe(df)
    # ... (데이터 교정 및 JSONL 다운로드 UI)