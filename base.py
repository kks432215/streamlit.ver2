
import pandas as pd
import plotly as px

# -------------------------------
# 1. 페이지 설정 및 제목
# -------------------------------
st.set_page_config(page_title="CO₂ Emissions Dashboard", layout="wide")
st.title("🌍 국가별 CO₂ 배출량 데이터 대시보드")
st.markdown("Kaggle에서 제공하는 국가별 CO₂ 배출 데이터를 시각화한 대시보드입니다.")

# -------------------------------
# 2. 데이터 불러오기
# (GitHub의 RAW CSV 링크 사용)
# -------------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/your-username/your-repo/main/co2_emissions.csv"  # ← 여기 수정!
    df = pd.read_csv(url)
    df = df.dropna(subset=["year", "country", "co2"])
    return df

df = load_data()

# -------------------------------
# 3. 필터 설정 (사이드바)
# -------------------------------
st.sidebar.header("🔎 필터 옵션")
year_range = st.sidebar.slider("연도 범위", 1950, 2020, (2000, 2020))
selected_countries = st.sidebar.multiselect(
    "국가 선택", options=sorted(df["country"].unique()), default=["South Korea", "United States", "China"]
)

filtered_df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]
if selected_countries:
    filtered_df = filtered_df[filtered_df["country"].isin(selected_countries)]

# -------------------------------
# 4. 연도별 CO₂ 배출량 라인 차트
# -------------------------------
st.subheader("📈 연도별 CO₂ 배출량 추이")
fig_line = px.line(
    filtered_df, x="year", y="co2", color="country",
    labels={"co2": "CO₂ 배출량 (백만 톤)", "year": "연도"},
    title="국가별 CO₂ 배출량 변화 추이"
)
st.plotly_chart(fig_line, use_container_width=True)

# -------------------------------
# 5. 특정 연도의 상위 배출국 바 차트
# -------------------------------
st.subheader("🏆 특정 연도의 상위 배출국")
rank_year = st.selectbox("연도 선택", sorted(filtered_df["year"].unique(), reverse=True))
rank_df = filtered_df[filtered_df["year"] == rank_year].groupby("country")["co2"].sum().sort_values(ascending=False).head(10)

st.bar_chart(rank_df)

# -------------------------------
# 6. 요약 통계 카드
# -------------------------------
st.subheader("📊 요약 통계 지표")
total = filtered_df["co2"].sum()
average = filtered_df.groupby("country")["co2"].mean().mean()

col1, col2 = st.columns(2)
col1.metric("총 CO₂ 배출량 (백만 톤)", f"{total:,.0f}")
col2.metric("국가별 평균 배출량", f"{average:,.2f}")
