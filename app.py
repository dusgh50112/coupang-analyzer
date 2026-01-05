import streamlit as st
import pandas as pd
from io import BytesIO

# 1. 페이지 설정 (웹사이트 탭 이름과 레이아웃)
st.set_page_config(page_title="쿠팡 주문 분석기", layout="wide")
st.title("📊 쿠팡 주문 엑셀 분석기")

# 2. 파일 업로드 섹션
# 이제 컴퓨터에 있는 파일을 직접 선택해서 올릴 수 있습니다.
uploaded_file = st.file_uploader("쿠팡 주문 엑셀 파일 선택 (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    try:
        # 3. 업로드된 엑셀 파일 읽기
        df = pd.read_excel(uploaded_file)

        # 4. 필요한 컬럼(제목)만 골라내기
        # 주의: 엑셀에 아래 이름들과 똑같은 컬럼이 있어야 합니다!
        cols = ["주문번호", "상품명", "판매수량", "판매가"]
        df = df[cols]

        # 5. 매출 계산 (수량 * 가격)
        df["매출"] = df["판매수량"] * df["판매가"]
        total_sales = df["매출"].sum()

        # 6. 상품별로 묶어서 합계 내기
        summary = df.groupby("상품명").agg(
            총판매수량=("판매수량", "sum"),
            총매출=("매출", "sum")
        ).reset_index()

        # 7. 화면에 결과 보여주기
        st.divider() # 구분선
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💰 총 매출")
            st.metric(label="전체 합계", value=f"{total_sales:,} 원")

        with col2:
            st.subheader("📦 상품별 요약")
            st.dataframe(summary, use_container_width=True)

        # 8. 분석 결과 엑셀로 내보내기 버튼
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            summary.to_excel(writer, index=False)
        
        st.download_button(
            label="✅ 분석 결과 엑셀 다운로드",
            data=output.getvalue(),
            file_name="쿠팡_판매량_분석결과.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except KeyError as e:
        st.error(f"⚠️ 엑셀 파일에 '{e}' 컬럼이 없습니다. 쿠팡 양식이 맞는지 확인해주세요.")
    except Exception as e:
        st.error(f"⚠️ 오류가 발생했습니다: {e}")

else:
    # 파일을 아직 안 올렸을 때 나오는 안내 문구
    st.info("⬆️ 위 버튼을 눌러 쿠팡 주문 엑셀 파일을 업로드해주세요.")