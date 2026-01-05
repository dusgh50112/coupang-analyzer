import streamlit as st
import pandas as pd

st.set_page_config(page_title="쿠팡 주문 분석기", layout="wide")
st.title("📊 쿠팡 주문 엑셀 분석기")

# 1️⃣ 파일 업로드
uploaded_file = st.file_uploader("쿠팡 주문 엑셀 파일 선택 (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    try:
        # 2️⃣ 엑셀 불러오기
        df = pd.read_excel(uploaded_file)

        # 3️⃣ 필요한 컬럼만 선택
        df = df[["주문번호", "상품명", "판매수량", "판매가"]]

        # 4️⃣ 총 매출 계산
        df["매출"] = df["판매수량"] * df["판매가"]
        total_sales = df["매출"].sum()

        # 5️⃣ 상품별 판매량 집계
        summary = df.groupby("상품명").agg(
            총판매수량=("판매수량", "sum"),
            총매출=("매출", "sum")
        ).reset_index()

        # 6️⃣ 웹 화면에 결과 보여주기
        st.subheader("총 매출")
        st.write(f"💰 {total_sales:,} 원")

        st.subheader("상품별 판매량")
        st.dataframe(summary)

        # 7️⃣ 다운로드 버튼
        summary.to_excel("상품별_판매량.xlsx", index=False)
        st.download_button(
            label="상품별 판매량 다운로드",
            data=open("상품별_판매량.xlsx", "rb"),
            file_name="상품별_판매량.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"⚠️ 엑셀 파일을 읽는 중 오류가 발생했습니다: {e}")
else:
    st.info("⬆️ 먼저 쿠팡 주문 엑셀 파일을 업로드해주세요.")
