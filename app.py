import streamlit as st
import pandas as pd
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import requests
import os

# 페이지 설정
st.set_page_config(page_title="셀러 올인원 마스터", layout="wide")

# --- 한글 폰트 설정 (중요!) ---
def get_font():
    font_url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Bold.ttf"
    font_path = "NanumGothic-Bold.ttf"
    if not os.path.exists(font_path):
        res = requests.get(font_url)
        with open(font_path, "wb") as f:
            f.write(res.content)
    return font_path

font_p = get_font()

# 상단 탭 구성
tab1, tab2, tab3 = st.tabs(["📊 매출 분석", "🎨 상세페이지 제작", "🌟 아이템 추천"])

# --- Tab 2: 상세페이지 제작 ---
with tab2:
    st.title("🎨 심플 상세페이지 제작기")
    st.write("상품 정보만 입력하면 깔끔한 홍보 이미지를 만들어줍니다.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        prod_name = st.text_input("상품명 입력", "햇반")
        point1 = st.text_input("특징 1", "간편한 조리")
        point2 = st.text_input("특징 2", "간편한 뒤처리")
        point3 = st.text_input("특징 3", "휴대성")
        price = st.text_input("가격 표시", "25,000원")
        bg_color = st.color_picker("배경색 선택", "#FFFFFF") # 기본 흰색 권장
        text_color = st.color_picker("글자색 선택", "#333333")

    with col2:
        # 이미지 생성 (800x1200으로 조금 더 길게)
        img = Image.new('RGB', (800, 1200), color=bg_color)
        d = ImageDraw.Draw(img)
        
        # 폰트 적용 (크기 조절)
        title_font = ImageFont.truetype(font_p, 60)
        content_font = ImageFont.truetype(font_p, 40)
        small_font = ImageFont.truetype(font_p, 30)

        # 텍스트 배치
        d.text((400, 150), "[ SPECIAL ITEM ]", fill=text_color, font=small_font, anchor="mm")
        d.text((400, 300), prod_name, fill=text_color, font=title_font, anchor="mm")
        d.line((250, 380, 550, 380), fill=text_color, width=3)
        
        # 특징 리스트
        d.text((400, 550), f"✓ {point1}", fill=text_color, font=content_font, anchor="mm")
        d.text((400, 650), f"✓ {point2}", fill=text_color, font=content_font, anchor="mm")
        d.text((400, 750), f"✓ {point3}", fill=text_color, font=content_font, anchor="mm")
        
        # 가격 강조
        d.text((400, 1000), f"판매가: {price}", fill="#E44D26", font=title_font, anchor="mm")
        
        st.image(img, caption="상세페이지 미리보기", use_container_width=True)
        
        # 다운로드 버튼
        buf = BytesIO()
        img.save(buf, format="PNG")
        st.download_button("이미지 다운로드 받기", buf.getvalue(), f"{prod_name}_상세페이지.png", "image/png")

# --- 기존 탭 1, 3 기능은 그대로 유지 ---
with tab1:
    st.write("매출 분석 기능을 사용하려면 엑셀을 업로드하세요.")
with tab3:
    st.write("추천 아이템을 확인해보세요.")
