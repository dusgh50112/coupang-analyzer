import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import requests
import os

# --- 1. 구글 시트 연결 설정 ---
def connect_gsheet():
    # Streamlit Secrets에 저장한 정보를 불러옵니다.
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    client = gspread.authorize(creds)
    # 반드시 구글 시트 제목이 'Coupang_Sales_DB' 여야 합니다.
    return client.open("Coupang_Sales_DB").sheet1

# --- 2. 폰트 설정 ---
@st.cache_data
def get_font():
    font_url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Bold.ttf"
    font_path = "NanumGothic-Bold.ttf"
    if not os.path.exists(font_path):
        res = requests.get(font_url)
        with open(font_path, "wb") as f: f.write(res.content)
    return font_path

font_p = get_font()

# --- 3. 메인 화면 구성 ---
st.set_page_config(page_title="셀러 올인원 마스터", layout="wide")
tab1, tab2, tab3 = st.tabs(["📊 정밀 매출 분석(DB저장)", "🎨 상세페이지 제작", "🌟 아이템 추천"])

# --- Tab 1: 매출 분석 및 구글 시트 저장 ---
with tab1:
    st.title("📊 쿠팡 정밀 수익 분석기")
    
    uploaded_file = st.file_uploader("쿠팡 주문 엑셀 파일 업로드", type=["xlsx"])
    use_sample = st.button("연습용 데이터로 실행하기")

    df = None
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
    elif use_sample:
        df = pd.DataFrame({
            "주문번호": ["2026-01-05-01"],
            "상품명": ["햇반 210g x 24개"],
            "판매수량": [10],
            "판매가": [25000],
            "원가": [15000]
        })

    if df is not None:
        # 간단 수익 계산 (수수료 13.9% 가정)
        df["총매출"] = df["판매가"] * df["판매수량"]
        df["예상수수료"] = (df["총매출"] * 0.139).astype(int)
        df["순이익"] = df["총매출"] - (df["판매수량"] * df.get("원가", 15000)) - df["예상수수료"]
        
        st.subheader("✅ 분석 결과 미리보기")
        st.dataframe(df, use_container_width=True)
        
        # 구글 시트 저장 버튼
        if st.button("💾 구글 스프레드시트에 영구 저장하기"):
            try:
                sheet = connect_gsheet()
                # 데이터를 문자열로 변환하여 구글 시트에 추가
                sheet.append_rows(df.astype(str).values.tolist())
                st.success("✅ 구글 시트(Coupang_Sales_DB)에 데이터가 안전하게 저장되었습니다!")
            except Exception as e:
                st.error(f"❌ 저장 실패: {e}\n(Secrets 설정이나 시트 공유를 확인하세요)")

# --- Tab 2: 상세페이지 제작 (이미지 업로드 포함) ---
with tab2:
    st.title("🎨 상세페이지 제작기")
    col1, col2 = st.columns([1, 1])
    with col1:
        name = st.text_input("상품명", "햇반")
        price_txt = st.text_input("가격", "25,000원")
        uploaded_img = st.file_uploader("상품 이미지 업로드", type=["jpg", "png"])
    
    with col2:
        # 간단 미리보기 이미지 생성 로직
        canvas = Image.new('RGB', (500, 700), color='white')
        draw = ImageDraw.Draw(canvas)
        if uploaded_img:
            product_img = Image.open(uploaded_img).resize((300, 300))
            canvas.paste(product_img, (100, 50))
        
        # 텍스트 넣기 (폰트가 있을 경우)
        try:
            f = ImageFont.truetype(font_p, 40)
            draw.text((250, 400), name, fill="black", font=f, anchor="mm")
            draw.text((250, 500), price_txt, fill="red", font=f, anchor="mm")
        except:
            st.write(f"상품명: {name} / 가격: {price_txt}")
            
        st.image(canvas)

# --- Tab 3: 아이템 추천 ---
with tab3:
    st.title("🌟 오늘의 추천 아이템")
    st.write("현재 시즌에는 '보온 보냉백'의 수요가 급증하고 있습니다!")
