import streamlit as st
import pandas as pd
from io import BytesIO

# 페이지 설정
st.set_page_config(page_title="쿠팡 주문 분석기", layout="wide")
st.title("📊 쿠팡 주문 엑셀 분석기")

# --- 연습용 샘플 데이터 만들기 기능 ---
def get_sample_data():
    data = {
        "주문번호": ["20240101-001", "20240101-002", "20240101-003", "20240101-004"],
        "상품명": ["맛있는 사과 1kg", "상큼한 오렌지 2kg", "맛있는 사과 1kg", "달콤한 포도 500g"],
        "판매수량": [2, 1, 3, 2],
        "판매가": [15000, 12000, 15000, 8000]
    }
    return pd.DataFrame(data)

# 사이드바에 샘플 데이터 버튼 추가
with st.sidebar:
    st.write("### 💡 테스트 모드")
    use_sample = st.button("연습용 데이터로 실행해보기")

# 1️⃣ 파일 업로드
uploaded_file = st.file_uploader("쿠팡 주문 엑셀 파일 선택 (.xlsx)", type=["xlsx"])

# 파일이 업로드되었거나, 샘플 버튼을 눌렀을 때 작동
df = None
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
elif use_sample:
    df = get_sample_data()
    st.success("✅ 연습용 데이터가 불러와졌습니다!")

if df is not None:
    try:
        # 2️⃣ 필요한 컬럼만 선택
        df = df[["주문번호", "상품명", "판매수량", "판매가"]]

        # 3️⃣ 매출 계산
        df["매출"] = df["판매수량"] * df["판매가"]
        total_sales = df["매출"].sum()

        # 4️⃣ 요약 정보
        summary = df.groupby("상품명").agg(
            총판매수량=("판매수량", "sum"),
            총매출=("매출", "sum")
        ).reset_index()

        # 5️⃣ 화면 표시
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("💰 총 매출")
            st.metric("합계", f"{total_sales:,} 원")
        with col2:
            st.subheader("📦 상품별 분석")
            st.dataframe(summary, use_container_width=True)

        # 다운로드 버튼
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            summary.to_excel(writer, index=False)
        st.download_button(
            label="분석 결과 다운로드",
            data=output.getvalue(),
            file_name="분석결과.xlsx"
        )

    except Exception as e:
        st.error(f"⚠️ 오류 발생: {e}. 엑셀의 제목(컬럼명)을 확인해주세요.")
else:
    st.info("⬆️ 파일을 업로드하거나 왼쪽의 '연습용 데이터' 버튼을 눌러보세요.")
