import os
from openai import OpenAI
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

class SolarCoachEngine:
    def __init__(self):
        self.api_key = os.getenv("UPSTAGE_API_KEY")
        self.base_url = os.getenv("UPSTAGE_BASE_URL")
        self.model_name = os.getenv("UPSTAGE_MODEL_NAME")
        
        # 클라이언트 초기화
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

    def get_response(self, system_prompt, user_input, stream=True):
        """
        Solar Pro 3 모델에 메시지를 보내고 응답을 받아오는 핵심 함수
        """
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                stream=stream,
                # Solar Pro 3의 핵심 기능: 논리적 추론 강도 설정
                # 'high'로 설정 시 복잡한 커뮤니케이션 분석 능력이 극대화됩니다.
                extra_body={"reasoning_effort": "high"} 
            )
            return response
            
        except Exception as e:
            print(f"[Error] AI 엔진 호출 중 오류 발생: {e}")
            return None

# 싱글톤 패턴으로 엔진 인스턴스 생성 (어디서든 동일한 엔진 사용 가능)
coach_engine = SolarCoachEngine()