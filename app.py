import streamlit as st
import pandas as pd
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import requests
import os

# 페이지 설정
st.set_page_config(page_title="셀러 올인원 마스터", layout="wide")

# --- 한글 폰트 설정 (이 코드가 있어야 한글이 안 깨집니다) ---
@st.cache_data
def get_font():
    font_url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Bold.ttf"
    font_path = "NanumGothic-Bold.ttf"
    if not os.path.exists(font_path):
        try:
            res = requests.get(font_url)
            with open(font_path, "wb") as f:
                f.write(res.content)
        except:
            return None
    return font_path

font_p = get_font()

# 상단 탭 구성
tab1, tab2, tab3 = st.tabs(["📊 매출 분석", "🎨 상세페이지 제작", "🌟 아이템 추천"])

# --- Tab 1: 매출 분석 ---
with tab1:
    st.title("📊 쿠팡 주문 엑셀 분석기")
    
    col_a, col_b = st.columns([2, 1])
    with col_a:
        uploaded_file = st.file_uploader("쿠팡 주문 엑셀 파일 선택 (.xlsx)", type=["xlsx"])
    with col_b:
        st.write("### 💡 테스트")
        use_sample = st.button("연습용 데이터로 실행하기") # 메인 화면으로 꺼냈습니다!

    df = None
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
    elif use_sample:
        df = pd.DataFrame({
            "주문번호": ["2024-01", "2024-02"],
            "상품명": ["햇반 210g x 24개", "스팸 200g x 10캔"],
            "판매수량": [5, 3],
            "판매가": [25000, 32000]
        })

    if df is not None:
        df["매출"] = df["판매수량"] * df["판매가"]
        st.success("데이터 분석 완료!")
        st.dataframe(df, use_container_width=True)
        st.metric("총 매출", f"{df['매출'].sum():,}")

# --- Tab 2: 상세페이지 제작 (한글 깨짐 수정 완료) ---
with tab2:
    st.title("🎨 심플 상세페이지 제작기")
    c1, c2 = st.columns([1, 1])
    with c1:
        prod_name = st.text_input("상품명", "햇반 210g")
        p1 = st.text_input("특징 1", "갓 지은 밥맛 그대로")
        p2 = st.text_input("특징 2", "전자레인지 2분 완성")
        price = st.text_input("가격", "25,000원")
        bg_color = st.color_picker("배경색", "#FFFFFF") # 흰색 추천
        txt_color = st.color_picker("글자색", "#333333")

    with c2:
        img = Image.new('RGB', (800, 1000), color=bg_color)
        draw = ImageDraw.Draw(img)
        
        try:
            # 폰트가 있으면 한글 적용, 없으면 기본 폰트
            f_main = ImageFont.truetype(font_p, 60) if font_p else ImageFont.load_default()
            f_sub = ImageFont.truetype(font_p, 40) if font_p else ImageFont.load_default()
            
            draw.text((400, 200), prod_name, fill=txt_color, font=f_main, anchor="mm")
            draw.line((200, 280, 600, 280), fill=txt_color, width=2)
            draw.text((400, 450), f"✓ {p1}", fill=txt_color, font=f_sub, anchor="mm")
            draw.text((400, 550), f"✓ {p2}", fill=txt_color, font=f_sub, anchor="mm")
            draw.text((400, 850), f"특별가: {price}", fill="#E44D26", font=f_main, anchor="mm")
        except:
            st.warning("폰트 로딩 중... 잠시만 기다려주세요.")
            
        st.image(img, use_container_width=True)

# --- Tab 3: 아이템 추천 ---
with tab3:
    st.title("🌟 카테고리별 추천 상품")
    st.info("여름 시즌: 휴대용 선풍기, 쿨매트가 뜨고 있습니다!")
    st.table(pd.DataFrame({"상품": ["캠핑용 의자", "단백질 쉐이크"], "이유": ["야외 활동 증가", "운동 시즌"], "난이도": ["중", "하"]}))
