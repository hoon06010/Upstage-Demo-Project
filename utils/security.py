# utils/security.py 수정본
import re

class DataSecurityManager:
    def __init__(self):
        self.mask_map = {}
        
    def mask_data(self, text):
        masked_text = text
        
        # 1. 이메일 패턴 (기존 유지)
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', masked_text)
        for i, email in enumerate(emails):
            token = f"[EMAIL_{i+1}]"
            self.mask_map[token] = email
            masked_text = masked_text.replace(email, token)
            
        # 2. 실명 + 직함/호칭 통합 패턴 개선
        # 이름 뒤에 붙는 모든 직급과 '님'을 한꺼번에 묶어서 마스킹합니다.
        # 예: '홍길동 대리님', '이영희 팀장', '박철수님' 모두 하나의 토큰으로 변환
        titles = r"(?:대리|과장|팀장|차장|부장|교수|연구원|책임|선임|님|\s)+"
        name_pattern = r'[가-힣]{2,4}' + titles
        
        found_names = re.findall(name_pattern, masked_text)
        for i, name_block in enumerate(found_names):
            token = f"[PERSON_{i+1}]"
            # 중복 마스킹 방지를 위해 strip() 처리된 원본을 저장
            self.mask_map[token] = name_block.strip()
            masked_text = masked_text.replace(name_block, token)
            
        return masked_text

    def unmask_data(self, text):
        unmasked_text = text
        for token, original in self.mask_map.items():
            unmasked_text = unmasked_text.replace(token, original)
        return unmasked_text

security_manager = DataSecurityManager()