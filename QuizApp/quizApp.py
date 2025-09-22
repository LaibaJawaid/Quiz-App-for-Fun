import streamlit as st
import time
from io import BytesIO
import re
from docx import Document

# ------ PAKISTAN GK QUIZ(By dictionary) ------

quiz_data = {
    "1. What is the capital city of Pakistan?": {
        "options": ["Lahore", "Karachi", "Islamabad", "Quetta"],
        "answer": "Islamabad"
    },
    "2. What is the national language of Pakistan?": {
        "options": ["English", "Punjabi", "Sindhi", "Urdu"],
        "answer": "Urdu"
    },
    "3. Which is the national animal of Pakistan?": {
        "options": ["Tiger", "Markhor", "Lion", "Cheetah"],
        "answer": "Markhor"
    },
    "4. What is Pakistan's national flower?": {
        "options": ["Rose", "Jasmine", "Sunflower", "Tulip"],
        "answer": "Jasmine"
    },
    "5. What is the national sport of Pakistan?": {
        "options": ["Cricket", "Football", "Hockey", "Squash"],
        "answer": "Hockey"
    },
    "6. Which mountain range includes the tallest peak in Pakistan?": {
        "options": ["The Alps", "The Himalayas", "The Rockies", "The Andes"],
        "answer": "The Himalayas"
    },
    "7. Which famous river flows through Pakistan and is known as the 'Father of Rivers'?": {
        "options": ["The Ganges", "The Nile", "The Indus", "The Amazon"],
        "answer": "The Indus"
    },
    "8. What famous ancient civilization once flourished in the areas of Pakistan?": {
        "options": ["Roman", "Greek", "Indus Valley", "Egyptian"],
        "answer": "Indus Valley"
    },
    "9. What is the national motto of Pakistan?": {
        "options": [ "Peace, Love, Unity", "Unity, Faith, Discipline",
                     "Strength, Justice, Freedom", "Progress, Prosperity, Happiness"],
        "answer": "Unity, Faith, Discipline"
    },
    "10. What is the national fruit of Pakistan?":{
        "options":[ "Mango", "Apple", "Banana", "Orange" ],
        "answer": "Mango"
    }
}

# ------ HOME TITLE / PAGE CONFIGURATION ------

st.set_page_config(page_title="Pakistan Quiz", page_icon="🇵🇰", layout="centered")
st.title("Pakistan General Quiz~")

# ------ SESSION STATE ------

if "started" not in st.session_state:
    st.session_state.started = False
if "deadline" not in st.session_state:
    st.session_state.deadline = None
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# ------ Helper Functions ------ #

def reset_quiz():
    st.session_state.started = False
    st.session_state.submitted = False
    st.session_state.answers = {}
    st.session_state.deadline = None

# def start_quiz():
#     st.session_state.page = "quiz"

# def show_results():
#     st.session_state.page = "result"

# def restart_quiz():
#     st.session_state.page = "home"
#     st.session_state.responses = {}

if not st.session_state.started:
    st.info("You have **2 minutes** to complete the quiz.")
    if st.button("🚀 Start Quiz"):
        st.session_state.started = True
        st.session_state.deadline = time.time() + 120
        st.rerun()

elif not st.session_state.submitted:
    # live countdown
    remaining = max(0, int(st.session_state.deadline - time.time()))
    minutes, seconds = divmod(remaining, 60)
    st.warning(f"⏳ Time left: **{minutes}:{seconds:02d}**")

    if remaining == 0:
        st.error("Time is up! Please submit your answers.")
    # Questions
    for q, data in quiz_data.items():
        st.session_state.answers[q] = st.radio(
            q,
            data["options"],
            key=q,
            index=data["options"].index(st.session_state.answers.get(q))
            if st.session_state.answers.get(q) in data["options"]
            else 0,
        )

    if st.button("✅ Submit Quiz"):
        st.session_state.submitted = True
        st.rerun()

else:
# ------ RESULTS PAGE ------ #
 correct = sum(
        1
        for q, d in quiz_data.items()
        if st.session_state.answers.get(q) == d["answer"]
    )
total = len(quiz_data)
st.success(f"🎯 Your Score: {correct}/{total}  ({(correct/total)*100:.1f}%)")

with st.expander("Show Correct Answers"):
    for q, d in quiz_data.items():
        st.write(f"**{q}** — ✅ {d['answer']}")

    if st.button("🔄 Restart Quiz"):
        reset_quiz()
        st.rerun()