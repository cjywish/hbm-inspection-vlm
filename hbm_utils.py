import re
import json

def extract_status(text):
    """
    VLM 응답 텍스트에서 <defect_status>: [값] 패턴을 찾아 반환합니다.
    """
    if not text:
        return "Unknown"
        
    # 정규표현식 설명: <defect_status> 태그 뒤의 대괄호([]) 안의 내용을 추출
    pattern = r"<defect_status>:\s*\[?(.*?)\]?(\n|$)"
    match = re.search(pattern, text, re.IGNORECASE)
    
    if match:
        status = match.group(1).strip()
        # 대괄호가 남아있을 경우 제거
        status = status.replace("[", "").replace("]", "")
        return status
    
    return "Unknown"

def format_for_finetune(df):
    """
    DB에서 불러온 DataFrame을 LoRA 파인튜닝용 JSONL 포맷으로 변환합니다.
    """
    jsonl_list = []
    for _, row in df.iterrows():
        entry = {
            "instruction": "HBM 패키징 공정 이미지를 분석하고 상태를 판정하라.",
            "input": f"온도: {row['temp']}C, 압력: {row['pressure']}N",
            "output": f"판정: {row['user_label']}\n분석: {row['analysis']}"
        }
        jsonl_list.append(json.dumps(entry, ensure_ascii=False))
    
    return "\n".join(jsonl_list)