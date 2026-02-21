import streamlit as st
import random
import pandas as pd
import time
import os

st.set_page_config(page_title="도파민 보상 선택 실험")

st.title("🧠 도파민 보상 선택 실험")
st.write("총 30번 선택하면 실험이 종료됩니다.")
st.write("1초 간격으로만 선택할 수 있습니다.")

MAX_CLICKS = 30
DATA_FILE = "results.csv"

# 참가자 이름 입력
participant = st.text_input("참가자 이름 또는 번호를 입력하세요")

# 세션 초기화
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.total_score = 0
    st.session_state.total_clicks = 0
    st.session_state.safe_count = 0
    st.session_state.risk8_count = 0
    st.session_state.risk12_count = 0
    st.session_state.last_click_time = 0
    st.session_state.finished = False

def can_click():
    return time.time() - st.session_state.last_click_time >= 1

def register_click():
    st.session_state.total_clicks += 1
    st.session_state.last_click_time = time.time()
    if st.session_state.total_clicks >= MAX_CLICKS:
        st.session_state.finished = True

# 버튼 영역
if participant and not st.session_state.finished:

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("✔ 확정 보상 (4점)"):
            if can_click():
                st.session_state.safe_count += 1
                st.session_state.total_score += 4
                register_click()

    with col2:
        if st.button("🎲 50% 확률로 8점"):
            if can_click():
                st.session_state.risk8_count += 1
                if random.random() < 0.5:
                    st.session_state.total_score += 8
                register_click()

    with col3:
        if st.button("🎯 33% 확률로 12점"):
            if can_click():
                st.session_state.risk12_count += 1
                if random.random() < 0.33:
                    st.session_state.total_score += 12
                register_click()

st.subheader(f"현재 점수: {st.session_state.total_score}")
st.subheader(f"선택 횟수: {st.session_state.total_clicks} / 30")

# 실험 종료 시 저장
if st.session_state.finished and participant:

    st.header("📊 실험 종료")

    new_data = pd.DataFrame([{
        "참가자": participant,
        "Safe(4점)": st.session_state.safe_count,
        "Risk8(50%)": st.session_state.risk8_count,
        "Risk12(33%)": st.session_state.risk12_count,
        "총 점수": st.session_state.total_score
    }])

    if os.path.exists(DATA_FILE):
        existing = pd.read_csv(DATA_FILE)
        combined = pd.concat([existing, new_data], ignore_index=True)
    else:
        combined = new_data

    combined.to_csv(DATA_FILE, index=False)

    st.success("결과가 저장되었습니다.")

    st.dataframe(combined)

    if st.button("🔄 다시 시작"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()