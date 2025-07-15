import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="CO₂ Emissions Dashboard", layout="wide")

# 제목
st.title("🌍 국가별 CO₂ 배출량 데이터 대시보드")
st.markdown("Kaggle에서 제공하는 국가별 CO₂ 배출 데이터를 시각화한 대시보드입니다.")

# 데이터 업로드
uploaded_file = st.sidebar.file_uploader("CSV 파일 업로드", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # 원본 열 이름 출력 (확인용)
    st.write("원본 열 이름:", df.columns.tolist())

    # 열 이름 좌우 공백 제거
    df.columns = df.columns.str.strip()

    # 공백 제거 후 열 이름 출력 (확인용)
    st.write("공백 제거 후 열 이름:", df.columns.tolist())

    # 필요한 열 목록
    required_cols = ["Year", "Entity", "Annual CO₂ emissions (tonnes )"]

    # 필수 열 존재 확인
    if not all(col in df.columns for col in required_cols):
        st.error(f"❗ CSV에 필요한 열이 없습니다. 필요한 열: {required_cols}")
        st.stop()

    # 결측값 제거
    df = df.dropna(subset=required_cols)

    # 필터 설정
    st.sidebar.header("🔎 필터 옵션")
    year_range = st.sidebar.slider("연도 범위", 1950, 2020, (2000, 2020))
    selected_countries = st.sidebar.multiselect(
        "국가 선택", options=sorted(df["Entity"].unique()),
        default=["South Korea", "United States", "China"]
    )

    filtered_df = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]
    if selected_countries:
        filtered_df = filtered_df[filtered_df["Entity"].isin(selected_countries)]

    # 연도별 CO₂ 배출량 라인 차트
    st.subheader("📈 연도별 CO₂ 배출량 추이")
    fig_line = px.line(
        filtered_df,
        x="Year",
        y="Annual CO₂ emissions (tonnes )",
        color="Entity",
        labels={
            "Annual CO₂ emissions (tonnes )": "CO₂ 배출량 (톤)",
            "Year": "연도",
            "Entity": "국가"
        },
        title="국가별 CO₂ 배출량 변화 추이"
    )
    st.plotly_chart(fig_line, use_container_width=True)

    # 특정 연도의 상위 배출국 바 차트
    st.subheader("🏆 특정 연도의 상위 배출국")
    rank_year = st.selectbox("연도 선택", sorted(filtered_df["Year"].unique(), reverse=True))
    rank_df = (
        filtered_df[filtered_df["Year"] == rank_year]
        .groupby("Entity")["Annual CO₂ emissions (tonnes )"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    st.bar_chart(rank_df)

    # 요약 통계 카드
    st.subheader("📊 요약 통계 지표")
    total = filtered_df["Annual CO₂ emissions (tonnes )"].sum()
    average = filtered_df.groupby("Entity")["Annual CO₂ emissions (tonnes )"].mean().mean()

    col1, col2 = st.columns(2)
    col1.metric("총 CO₂ 배출량 (톤)", f"{total:,.0f}")
    col2.metric("국가별 평균 배출량", f"{average:,.2f}")

else:
    st.warning("좌측 사이드바에서 co2_emissions.csv 파일을 업로드하세요.")
