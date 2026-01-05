import streamlit as st
import pandas as pd
from io import BytesIO

# 페이지 설정
st.set_page_config(page_title="쿠팡 주문 분석기", layout="wide")
st.title("📊 쿠팡 주문 엑셀 분석기")

# 1️⃣ 파일 업로드
uploaded_file = st.file_uploader("쿠팡 주문 엑셀 파일 선택 (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    try:
        # 2️⃣ 업로드된 파일 읽기
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

        # 6️⃣ 결과 화면에 표시
        st.subheader("총 매출")
        st.write(f"💰 {total_sales:,} 원")

        st.subheader("상품별 판매량")
        st.dataframe(summary)

        # 7️⃣ 다운로드 버튼 (BytesIO 사용)
        output = BytesIO()
        summary.to_excel(output, index=False)
        output.seek(0)
        st.download_button(
            label="상품별 판매량 다운로드",
            data=output,
            file_name="상품별_판매량.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"⚠️ 엑셀 읽기 중 오류: {e}")

else:
    st.info("⬆️ 먼저 쿠팡 주문 엑셀 파일을 업로드해주세요.")
