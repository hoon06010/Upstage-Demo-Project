# core/formatter.py
import streamlit as st
import re

class ResponseFormatter:
    @staticmethod
    def extract_score(text):
        """텍스트 데이터에서 Score: [숫자] 패턴을 찾아 정수로 반환합니다."""
        match = re.search(r"Score:\s*(\d+)", text)
        if match:
            return int(match.group(1))
        return None

    @staticmethod
    def display_report(full_text):
        """텍스트를 파싱하여 점수는 게이지로, 본문은 마크다운으로 출력합니다."""
        # 1. 점수 추출 및 본문 분리
        score = ResponseFormatter.extract_score(full_text)
        clean_text = re.sub(r"---?\s*Score:\s*\d+", "", full_text).strip()

        # 2. 점수 시각화 (HCI적 요소: 상단 배치로 즉각적 피드백 제공)
        if score is not None:
            col1, col2 = st.columns([1, 3])
            with col1:
                color = "red" if score < 50 else "orange" if score < 80 else "green"
                st.metric(label="커뮤니케이션 온도", value=f"{score}점")
            with col2:
                st.progress(score / 100)
                if score < 60:
                    st.caption("⚠️ 현재 말투는 상대방에게 압박감을 줄 수 있습니다.")
                else:
                    st.caption("✅ 협력적인 소통 방식을 잘 유지하고 계시네요!")
            st.divider()

        # 3. 본문 출력
        st.markdown(clean_text)

#