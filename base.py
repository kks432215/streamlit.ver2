import streamlit as st
import pandas as pd
import plotly.express as px

# ✅ 페이지 설정
st.set_page_config(page_title="CO₂ Emissions Dashboard", layout="wide")

# ✅ 제목
st.title("🌍 국가별 CO₂ 배출량 데이터 대시보드")
st.markdown("Kaggle에서 제공하는 국가별 CO₂ 배출 데이터를 시각화한 대시보드입니다.")

# -------------------------------
# 1. 데이터 업로드
# -------------------------------
uploaded_file = st.sidebar.file_uploader("CSV 파일 업로드", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # 📌 열 이름 출력해서 확인
    st.write("열 이름:", df.columns.tolist())

    # ✅ 실제 열 이름에 맞춰 결측값 제거
    df = df.dropna(subset=["Year", "Country", "CO2"])
else:
    st.warning("좌측 사이드바에서 co2_emissions.csv 파일을 업로드하세요.")
    st.stop()

# -------------------------------
# 2. 필터 설정 (사이드바)
# -------------------------------
st.sidebar.header("🔎 필터 옵션")
year_range = st.sidebar.s_
