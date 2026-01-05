import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import requests
import os

# --- 1. 구글 시트 연결 함수 ---
def connect_gsheet():
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds_dict = st.secrets["gcp_service_account"]
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        client = gspread.authorize(creds)
        spreadsheet = client.open("Coupang_Sales_DB")
        return spreadsheet.worksheet("시트1") 
    except Exception as e:
        st.error(f"⚠️ 구글 시트 연결 실패: {e}")
        return None

# --- 2. 폰트 설정 ---
@st.cache_data
def get_font():
    font_url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Bold.ttf"
    font_path = "NanumGothic-Bold.ttf"
    if not os.path.exists(font_path):
        try:
            res = requests.get(font_url)
            with open(font_path, "wb") as f: f.write(res.content)
        except: return None
    return font_path

font_p = get_font()

# --- 3. 앱 화면 구성 ---
st.set_page_config(page_title="셀러 올인원 마스터", layout="wide")
tab1, tab2, tab3 = st.tabs(["📊 매출 분석 및 저장", "🎨 상세페이지 제작", "🌟 아이템 추천"])

# --- Tab 1: 매출 분석 및 구글 시트 저장 ---
with tab1:
    st.title("📊 쿠팡 매출 분석 및 DB 저장")
    uploaded_file = st.file_uploader("쿠팡 정산 엑셀 업로드", type=["xlsx"])
    use_sample = st.button("연습용 데이터 불러오기")

    df = None
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
    elif use_sample:
        df = pd.DataFrame({
            "날짜": ["2026-01-05"],
            "상품명": ["햇반 210g x 24개"],
            "판매수량": [10],
            "판매가": [25000],
            "원가": [15000]
        })

    if df is not None:
        df["총매출"] = df["판매가"] * df["판매수량"]
        df["수수료"] = (df["총매출"] * 0.139).astype(int)
        df["순이익"] = df["총매출"] - (df["판매수량"] * df.get("원가", 15000)) - df["수수료"]
        
        st.subheader("✅ 데이터 확인")
        st.dataframe(df, use_container_width=True)
        
        if st.button("💾 구글 스프레드시트에 영구 저장하기"):
            sheet = connect_gsheet()
            if sheet:
                try:
                    data_to_save = df.astype(str).values.tolist()
                    sheet.append_rows(data_to_save)
                    
                    # 데이터가 어디에 저장됐는지 확인용 코드 추가
                    rows = sheet.get_all_values()
                    st.success(f"🎉 저장 성공! 현재 구글 시트에 총 {len(rows)}개의 데이터가 있습니다.")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ 저장 중 에러 발생: {e}")

# --- Tab 2: 상세페이지 제작 ---
with tab2:
    st.title("🎨 상세페이지 제작기")
    col1, col2 = st.columns([1, 1])
    with col1:
        p_name = st.text_input("상품 이름", "상품명을 입력하세요")
        p_price = st.text_input("표시 가격", "25,000원")
        p_img = st.file_uploader("상품 사진 업로드", type=["jpg", "png"])
    
    with col2:
        canvas = Image.new('RGB', (500, 700), color='white')
        draw = ImageDraw.Draw(canvas)
        if p_img:
            img = Image.open(p_img).resize((300, 300))
            canvas.paste(img, (100, 50))
        if font_p:
            try:
                f = ImageFont.truetype(font_p, 35)
                draw.text((250, 450), p_name, fill="black", font=f, anchor="mm")
                draw.text((250, 550), p_price, fill="red", font=f, anchor="mm")
            except: pass
        st.image(canvas, caption="미리보기 화면")

# --- Tab 3: 아이템 추천 ---
with tab3:
    st.title("🌟 오늘의 추천 아이템")
    st.info("실시간 트렌드 분석 결과: 현재 '방한용품'의 클릭률이 가장 높습니다.")
