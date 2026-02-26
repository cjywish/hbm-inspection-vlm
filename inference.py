# inference.py 수정본
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import PIL.Image
import cv2
import os

# 1. 로컬 환경일 경우 .env 파일을 로드함
load_dotenv()

class VLMInspector:
    def __init__(self):
        # 2. 우선 순위에 따라 키를 가져옴
        # (1) Streamlit Cloud Secrets (서버용)
        # (2) OS Environment / .env (로컬용)
        api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            st.error("⚠️ API Key를 찾을 수 없습니다. .env 파일이나 Streamlit Secrets를 확인하세요.")
            return

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        try:
            self.model = genai.GenerativeModel(self.model_name)
            # 간단한 연결 테스트
            print(f"✅ 모델 연결 시도 중: {self.model_name}")
        except Exception as e:
            print(f"❌ 모델 초기화 실패: {e}")

        self.system_prompt = """
        ### ROLE: HBM 패키징 수석 엔지니어
        입력된 이미지와 데이터를 분석하여 다음 형식을 준수하라:
        - <defect_status>: [정상/주의/불량]
        - <reasoning>: 상세 논리 근거
        - <process_suggestion>: 장비 설정 제언
        """

    def analyze(self, image_array, telemetry):
        rgb_img = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
        pil_img = PIL.Image.fromarray(rgb_img)

        user_content = f"현재 본딩 온도: {telemetry['temp']}C, 압력: {telemetry['pressure']}N. 분석 요청."
        
        try:
            # 404 에러가 지속될 경우를 대비한 예외 처리
            response = self.model.generate_content([self.system_prompt + user_content, pil_img])
            return response.text
        except Exception as e:
            return f"⚠️ 분석 중 오류 발생: {str(e)}\n사용 가능한 모델 리스트를 확인해 보세요."