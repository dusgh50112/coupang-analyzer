import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from PIL import Image, ImageDraw, ImageFont
import requests
import os
import time

# --- 1. 구글 시트 연결 ---
def connect_gsheet():
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
        client = gspread.authorize(creds)
        return client.open("Coupang_Sales_DB").worksheet("시트1")
    except Exception as e:
        st.error(f"⚠️ 시트 연결 실패: {e}")
        return None

# --- 2. 앱 설정 ---
st.set_page_config(page_title="쿠팡 셀러 올인원", layout="wide")
tab1, tab2, tab3 = st.tabs(["📊 매출 분석/저장", "🎨 상세페이지", "🌟 아이템 추천"])

# Tab 1: 분석 및 저장
with tab1:
    st.title("📊 매출 수익 분석")
    up_file = st.file_uploader("엑셀 업로드", type=["xlsx"])
    if st.button("연습 데이터 생성"):
        df = pd.DataFrame({"날짜": [time.strftime("%Y-%m-%d")], "상품명": ["햇반"], "판매수량": [10], "판매가": [25000], "원가": [15000]})
        df["순이익"] = (df["판매가"] * 0.86) - df["원가"] # 수수료 대략 계산
        st.dataframe(df)
        if st.button("💾 구글 시트에 저장하기"):
            sheet = connect_gsheet()
            if sheet:
                sheet.append_rows(df.astype(str).values.tolist())
                st.success("✅ 구글 시트 저장 성공!")

# Tab 2: 상세페이지 (이전과 동일)
with tab2:
    st.title("🎨 상세페이지 제작")
    p_name = st.text_input("상품명", "상품")
    if st.file_uploader("이미지", type=["jpg", "png"]):
        st.write(f"{p_name} 상세페이지 미리보기 생성됨")

# Tab 3: 추천
with tab3:
    st.title("🌟 오늘의 추천 상품")
    st.info("현재 트렌드는 '난방 가전'입니다.")
