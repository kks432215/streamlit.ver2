import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# 1. 타이틀 및 소개
# -----------------------------
st.set_page_config(layout="wide")
st.title("🌍 국가별 CO₂ 배출량 대시보드")
st.markdown("""
이 대시보드는 Kaggle의 **CO₂ 배출량 데이터셋**을 바탕으로  
국가별, 산업별, 연도별 탄소 배출 트렌드를 분석하고 시각화합니다.
""")

# -----------------------------
# 2. 데이터 로딩
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("co2_emissions.csv")  # 파일명을 실제 이름으로 바꿔주세요
    df = df.dropna(subset=["year", "country", "co2"])
    return df

df = load_data()

# -----------------------------
# 3. 사이드바 필터
# -----------------------------
year_range = st.sidebar.slider("연도 범위 선택", 1950, 2020, (2000, 2020))
selected_countries = st.sidebar.multiselect("국가 선택", options=df['country'].unique(), default=["South Korea", "United States", "China"])

filtered_df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]
if selected_countries:
    filtered_df = filtered_df[filtered_df["country"].isin(selected_countries)]

# -----------------------------
# 4. 시계열 그래프
# -----------------------------
st.subheader("📈 연도별 CO₂ 배출량 변화")
fig = px.line(filtered_df, x="year", y="co2", color="country", title="국가별 연도별 CO₂ 배출량 (단위: 백만 톤)")
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# 5. 상위 국가 랭킹
# -----------------------------
st.subheader("🏆 특정 연도의 상위 CO₂ 배출국")
rank_year = st.selectbox("연도 선택", sorted(filtered_df['year'].unique(), reverse=True))
rank_data = filtered_df[filtered_df["year"] == rank_year].groupby("country")["co2"].sum().sort_values(ascending=False).head(10)
st.bar_chart(rank_data)

# -----------------------------
# 6. 지도 시각화
# -----------------------------
st.subheader("🗺️ 세계 지도 기반 CO₂ 배출량")
map_data = filtered_df[filtered_df["year"] == rank_year][["country", "co2", "latitude", "longitude"]].dropna()

if not map_data.empty:
    fig_map = px.scatter_geo(
        map_data,
        lat='latitude',
        lon='longitude',
        hover_name='country',
        size='co2',
        color='co2',
        projection="natural earth",
        title=f"{rank_year}년 국가별 CO₂ 배출량"
    )
    st.plotly_chart(fig_map, use_container_width=True)
else:
    st.warning("지도 시각화를 위한 좌표 데이터가 없습니다.")

# -----------------------------
# 7. 요약 지표
# -----------------------------
st.subheader("📌 요약 통계")
total_emissions = filtered_df["co2"].sum()
avg_emission = filtered_df.groupby("country")["co2"].mean().mean()

col1, col2 = st.columns(2)
col1.metric("총 배출량 (Mton)", f"{total_emissions:,.0f}")
col2.metric("국가별 평균 배출량", f"{avg_emission:,.2f}")
