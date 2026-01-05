import streamlit as st
import pandas as pd
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# 페이지 설정
st.set_page_config(page_title="셀러 올인원 마스터", layout="wide")

# 상단 탭 구성
tab1, tab2, tab3 = st.tabs(["📊 매출 분석", "🎨 상세페이지 제작", "🌟 아이템 추천"])

# --- Tab 1: 매출 분석 (기존 기능) ---
with tab1:
    st.title("📊 쿠팡 주문 엑셀 분석기")
    
    def get_sample_data():
        data = {
            "주문번호": ["20240101-001", "20240101-002", "20240101-003", "20240101-004"],
            "상품명": ["맛있는 사과 1kg", "상큼한 오렌지 2kg", "맛있는 사과 1kg", "달콤한 포도 500g"],
            "판매수량": [2, 1, 3, 2],
            "판매가": [15000, 12000, 15000, 8000]
        }
        return pd.DataFrame(data)

    with st.sidebar:
        st.write("### 💡 테스트 모드")
        use_sample = st.button("연습용 데이터로 실행해보기")

    uploaded_file = st.file_uploader("쿠팡 주문 엑셀 파일 선택 (.xlsx)", type=["xlsx"], key="analysis_upload")

    df = None
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
    elif use_sample:
        df = get_sample_data()

    if df is not None:
        try:
            df = df[["주문번호", "상품명", "판매수량", "판매가"]]
            df["매출"] = df["판매수량"] * df["판매가"]
            total_sales = df["매출"].sum()
            summary = df.groupby("상품명").agg(총판매수량=("판매수량", "sum"), 총매출=("매출", "sum")).reset_index()
            
            st.divider()
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("💰 총 매출")
                st.metric("합계", f"{total_sales:,} 원")
            with col2:
                st.subheader("📦 상품별 분석")
                st.dataframe(summary, use_container_width=True)
        except:
            st.error("엑셀 형식이 맞지 않습니다. 제목을 확인해주세요.")

# --- Tab 2: 상세페이지 제작 ---
with tab2:
    st.title("🎨 심플 상세페이지 제작기")
    st.write("상품 정보만 입력하면 깔끔한 홍보 이미지를 만들어줍니다.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        prod_name = st.text_input("상품명 입력", "초강력 무선 핸디 청소기")
        point1 = st.text_input("특징 1", "동급 최강 흡입력")
        point2 = st.text_input("특징 2", "한 번 충전으로 30분 사용")
        point3 = st.text_input("특징 3", "0.5kg 초경량 설계")
        price = st.text_input("가격 표시", "29,900원")
        bg_color = st.color_picker("배경색 선택", "#FFFFFF")
        text_color = st.color_picker("글자색 선택", "#333333")

    with col2:
        # 이미지 생성 로직 (Pillow 사용)
        img = Image.new('RGB', (800, 1000), color=bg_color)
        d = ImageDraw.Draw(img)
        
        # 텍스트 배치 (간이 구현)
        d.text((400, 100), "[ SPECIAL ITEM ]", fill=text_color, anchor="mm")
        d.text((400, 200), prod_name, fill=text_color, anchor="mm")
        d.line((300, 250, 500, 250), fill=text_color, width=2)
        d.text((400, 400), f"✓ {point1}", fill=text_color, anchor="mm")
        d.text((400, 500), f"✓ {point2}", fill=text_color, anchor="mm")
        d.text((400, 600), f"✓ {point3}", fill=text_color, anchor="mm")
        d.text((400, 800), f"판매가: {price}", fill="#E44D26", anchor="mm")
        
        st.image(img, caption="상세페이지 미리보기", use_container_width=True)
        
        # 다운로드 버튼
        buf = BytesIO()
        img.save(buf, format="PNG")
        st.download_button("상세페이지 이미지 다운로드", buf.getvalue(), "detail_page.png", "image/png")

# --- Tab 3: 아이템 추천 ---
with tab3:
    st.title("🌟 요즘 뜨는 아이템 추천")
    st.write("키워드 분석을 통해 지금 팔기 좋은 블루오션 상품을 추천합니다.")
    
    category = st.selectbox("관심 카테고리", ["생활용품", "주방용품", "디지털/가전", "캠핑/레저"])
    
    # 추천 데이터 (예시 데이터 - 실제로는 알고리즘으로 확장 가능)
    recommendations = {
        "생활용품": [
            {"상품": "미니 제습함", "이유": "장마철 대비 검색량 급증, 경쟁 상품 적음", "난이도": "하"},
            {"상품": "자석 부착형 현관 모기장", "이유": "여름 시즌 아이템, 교체 수요 많음", "난이도": "중"}
        ],
        "주방용품": [
            {"상품": "실리콘 냄비 손잡이", "이유": "1인 가구 소품 수요 증가", "난이도": "하"},
            {"상품": "무전원 요거트 메이커", "이유": "건강식 트렌드, SNS 언급량 증가", "난이도": "중"}
        ],
        "디지털/가전": [
            {"상품": "노트북 쿨링 거치대", "이유": "재택근무자 증가로 꾸준한 수요", "난이도": "상"},
            {"상품": "C타입 관절 충전 케이블", "이유": "모바일 게임 유저 타겟팅", "난이도": "하"}
        ],
        "캠핑/레저": [
            {"상품": "접이식 캠핑 의자", "이유": "차박 트렌드 지속", "난이도": "중"},
            {"상품": "차량용 햇빛 가리개", "이유": "여름철 필수 아이템", "난이도": "하"}
        ]
    }
    
    st.write(f"### 🚀 {category} 추천 리스트")
    rec_df = pd.DataFrame(recommendations[category])
    st.table(rec_df)
    
    st.info("💡 위 아이템들을 도매 사이트(도매매 등)에서 검색해서 최저가를 확인해 보세요!")
