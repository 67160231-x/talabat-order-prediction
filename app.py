import streamlit as st
import pandas as pd
import pickle
import os

# --- 1. หน้าตาเว็บแบบมินิมอล ---
st.set_page_config(
    page_title="Order Predictor",
    page_icon="🥡",
    layout="centered"
)

# --- 2. Custom CSS ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Prompt', sans-serif; background-color: #ffffff; }
    .stMarkdown p, label { font-size: 1.25rem !important; font-weight: 500 !important; color: #333 !important; }
    input { font-size: 1.2rem !important; }
    .stButton>button {
        width: 100%; border-radius: 15px; border: none; height: 4em;
        background: linear-gradient(90deg, #FF4B2B 0%, #FF416C 100%);
        color: white; font-size: 1.5rem !important; font-weight: 600;
        box-shadow: 0 4px 15px rgba(255, 75, 43, 0.4); margin-top: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. โหลดโมเดล (แก้ไขเพื่อป้องกัน NameError) ---
@st.cache_resource
def load_model():
    # ลองหาไฟล์จากที่ต่างๆ
    possible_paths = [
        os.path.join(os.path.dirname(__file__), 'best_model.pkl'),
        os.path.join(os.path.dirname(__file__), 'models', 'best_model.pkl'),
        'best_model.pkl',
        'models/best_model.pkl'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, 'rb') as f:
                    return pickle.load(f)
            except:
                continue
    return None

# บรรทัดนี้สำคัญมาก: ต้องรันฟังก์ชันเพื่อเอาค่ามาใส่ตัวแปร model
model = load_model()

# --- 4. ส่วนหัวข้อ ---
st.markdown("<h1 style='text-align: center; color: #1E1E1E; font-size: 3rem; margin-bottom: 0;'>🥡 Order Analysis</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888; font-size: 1.4rem; margin-top: 0;'>วิเคราะห์ความเสี่ยงออเดอร์ด้วย AI</p>", unsafe_allow_html=True)
st.write("")

# --- 5. ส่วนกรอกข้อมูล ---
col1, col2 = st.columns(2)
with col1:
    dist = st.number_input("📍 ระยะทาง (km)", min_value=0.0, step=0.1, value=2.0)
    traffic = st.selectbox("🚦 สภาพการจราจร", ["Low", "Medium", "High"])
    quantity = st.number_input("🍱 จำนวนอาหาร (ชิ้น)", min_value=1, value=1)
with col2:
    price = st.number_input("💰 ราคารวม (AED)", min_value=0.0, step=1.0, value=45.0)
    hour = st.slider("⏰ เวลาที่สั่ง (24 ชม.)", 0, 23, 18)

st.write("")
predict_btn = st.button("วิเคราะห์ข้อมูลตอนนี้ ✨")

# --- 6. แสดงผลลัพธ์ ---
if predict_btn:
    if model is not None:
        try:
            traffic_map = {"Low": 0, "Medium": 1, "High": 2}
            input_df = pd.DataFrame([[quantity, price, hour, dist, traffic_map[traffic]]],
                                  columns=['Quantity', 'Total_Price', 'Order_Hour', 'Delivery_Distance_km', 'Traffic_Level'])
            
            proba = model.predict_proba(input_df)[0][1]
            risk_percent = proba * 100
            
            st.markdown("---")
            if proba < 0.5:
                st.markdown(f"<div style='background-color: #f0fdf4; padding: 40px; border-radius: 25px; text-align: center; border: 2px solid #bbf7d0;'><h1 style='color: #166534; margin: 0; font-size: 3rem;'>✅ ปลอดภัย</h1><p style='color: #16a34a; font-size: 1.6rem; margin-top: 10px;'>โอกาสสำเร็จสูง (ความเสี่ยง {risk_percent:.1f}%)</p></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='background-color: #fef2f2; padding: 40px; border-radius: 25px; text-align: center; border: 2px solid #fecaca;'><h1 style='color: #991b1b; margin: 0; font-size: 3rem;'>⚠️ เสี่ยงถูกยกเลิก</h1><p style='color: #dc2626; font-size: 1.6rem; margin-top: 10px;'>ความเสี่ยงสูง ({risk_percent:.1f}%)</p></div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาดในการทำนาย: {e}")
    else:
        st.error("Model Error: ระบบหาไฟล์โมเดลไม่เจอ โปรดตรวจสอบว่ามีไฟล์ best_model.pkl อยู่ใน GitHub")

st.markdown("<p style='text-align: center; color: #BBB; font-size: 1rem; margin-top: 60px;'>AI-Powered Prediction Platform</p>", unsafe_allow_html=True)