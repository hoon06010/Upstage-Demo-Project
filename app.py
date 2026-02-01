import streamlit as st
from core.coach_engine import coach_engine
from core.prompts import get_coaching_prompt
from core.formatter import ResponseFormatter
from utils.security import security_manager

# 1. 페이지 설정 및 커스텀 디자인
st.set_page_config(page_title="Solar Comm-Coach", page_icon="☀️", layout="wide")

# Upstage 스타일 커스텀 CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #6d28d9; color: white; }
    .stTextArea>div>div>textarea { background-color: #1f2937; color: #f3f4f6; }
    .security-badge { padding: 5px 10px; border-radius: 20px; background-color: #064e3b; color: #34d399; font-size: 0.8rem; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. 사이드바: 브랜드 및 상태 정보
with st.sidebar:
    st.title("Solar AI Coach")
    st.markdown('<p class="security-badge">🛡️ PII Masking Active</p>', unsafe_allow_html=True)
    st.divider()
    st.info("본 서비스는 Upstage Solar Pro 3 모델의 강력한 추론 능력을 바탕으로 조직 내 심리적 안전감을 구축합니다.")

# 3. 메인 레이아웃: 2컬럼 구성
col_input, col_result = st.columns([1, 1.2], gap="large")

with col_input:
    st.title("🤝 커뮤니케이션 코치")
    st.caption("AI 기반 말투 교정 및 관계 최적화 솔루션")
    
    user_input = st.text_area(
        "교정하고 싶은 대화 내용을 입력하세요:",
        placeholder="예: 홍길동 대리님, 지난번에도 데이터 틀리더니 이번에도 이러면 어떡해요?",
        height=250
    )
    
    # 관계 선택 옵션 (맥락 분석 강화)
    relation = st.selectbox("상대방과의 관계:", ["동료 (대등한 관계)", "직속 부하 (피드백 필요)", "상사 (정중한 제안)"])
    
    analyze_button = st.button("✨ Solar 분석 가동")

with col_result:
    # app.py의 실행 로직 부분 수정
    if analyze_button:
        if not user_input.strip():
            st.warning("분석할 텍스트를 입력해 주세요.")
        else:
            with st.spinner("Solar Pro 3가 실시간으로 분석 중입니다..."):
                system_prompt = get_coaching_prompt()
                masked_input = f"[관계: {relation}] {security_manager.mask_data(user_input)}" # 보안 적용
                
                # 1. 출력을 위한 빈 공간(Placeholder) 생성
                report_placeholder = st.empty()
                full_content = ""
                
                # 2. 스트리밍 호출 (stream=True)
                response_stream = coach_engine.get_response(system_prompt, masked_input, stream=True)
                
                if response_stream:
                    for chunk in response_stream:
                        # 스트리밍 데이터에서 텍스트 조각 추출
                        if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content:
                            token = chunk.choices[0].delta.content
                            full_content += token
                            # 실시간으로 화면에 출력 (가명화된 상태로 먼저 보여줌)
                            report_placeholder.markdown(full_content + "▌")
                    
                    # 3. [중요] 스트리밍 완료 후 보안 복원 및 최종 포맷팅
                    final_report = security_manager.unmask_data(full_content)
                    
                    # 4. 깔끔하게 정돈된 최종 리포트로 교체
                    report_placeholder.empty() # 이전 출력 삭제
                    ResponseFormatter.display_report(final_report) # 최종 디자인 적용
                    st.success("분석 완료! 업스테이지 솔라의 성능을 확인하세요. 🌙")
                else:
                    st.error("AI 엔진 호출 중 오류가 발생했습니다.")

st.markdown("---")
st.caption("© 2026 Half Moon AI Lab x Upstage Ambassador Project")