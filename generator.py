import cv2
import numpy as np
import random

def generate_hbm_sample(defect_type="Normal"):
    """가상 HBM 기판 이미지 및 센서 데이터 생성"""
    # 기본 이미지 생성 (400x600)
    img = np.zeros((400, 600, 3), dtype=np.uint8) + 45
    for x in range(50, 600, 100):
        for y in range(50, 400, 100):
            cv2.circle(img, (x, y), 22, (180, 180, 180), -1)

    # 불량 합성 로직
    if defect_type == "Microbump Bridge":
        cv2.rectangle(img, (150, 42), (250, 58), (180, 180, 180), -1)
    elif defect_type == "TSV Void":
        cv2.circle(img, (250, 150), 7, (10, 10, 10), -1)

    # 가상 센서 데이터 (정상 범위를 기준으로 랜덤 생성)
    telemetry = {
        "temp": round(random.uniform(250, 275), 1),
        "pressure": round(random.uniform(100, 150), 1)
    }
    
    return img, telemetry