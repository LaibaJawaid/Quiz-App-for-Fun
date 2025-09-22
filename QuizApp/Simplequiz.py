import streamlit as st
import time

# ---------------- QUIZ DATA ---------------- #
QUIZ = {
    "1. What is the capital city of Pakistan?": {
        "options": ["Lahore", "Karachi", "Islamabad", "Quetta"],
        "answer": "Islamabad",
    },
    "2. What is the national language of Pakistan?": {
        "options": ["English", "Punjabi", "Sindhi", "Urdu"],
        "answer": "Urdu",
    },
    "3. Which is the national animal of Pakistan?": {
        "options": ["Tiger", "Markhor", "Lion", "Cheetah"],
        "answer": "Markhor",
    },
    "4. What is Pakistan's national flower?": {
        "options": ["Rose", "Jasmine", "Sunflower", "Tulip"],
        "answer": "Jasmine",
    },
    "5. What is the national sport of Pakistan?": {
        "options": ["Cricket", "Football", "Hockey", "Squash"],
        "answer": "Hockey",
    },
    "6. Which mountain range includes the tallest peak in Pakistan?": {
        "options": ["The Alps", "The Himalayas", "The Rockies", "The Andes"],
        "answer": "The Himalayas",
    },
    "7. Which famous river flows through Pakistan and is known as the 'Father of Rivers'?": {
        "options": ["The Ganges", "The Nile", "The Indus", "The Amazon"],
        "answer": "The Indus",
    },
    "8. What famous ancient civilization once flourished in the areas of Pakistan?": {
        "options": ["Roman", "Greek", "Indus Valley", "Egyptian"],
        "answer": "Indus Valley",
    },
    "9. What is the national motto of Pakistan?": {
        "options": [
            "Peace, Love, Unity",
            "Unity, Faith, Discipline",
            "Strength, Justice, Freedom",
            "Progress, Prosperity, Happiness",
        ],
        "answer": "Unity, Faith, Discipline",
    },
    "10. What is the national fruit of Pakistan?": {
        "options": ["Mango", "Apple", "Banana", "Orange"],
        "answer": "Mango",
    },
}

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(page_title="QuizApp", page_icon="🎯", layout="centered")

# ---------------- STYLE-CSS ---------------- #
st.markdown(
    """
    <style>
    div.stButton > button {
        background-color: #808080 !important;
        color: white !important;
        border-radius: 6px;
        padding: 0.5em 1em;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- SESSION STATE ---------------- #
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "responses" not in st.session_state:
    st.session_state.responses = {}
if "deadline" not in st.session_state:
    st.session_state.deadline = None
if "finish_time" not in st.session_state:
    st.session_state.finish_time = None

# ---------------- RESET FUNCTION ---------------- #
def reset_quiz(next_page="Home"):
    """Clear everything and optionally start fresh Quiz."""
    st.session_state.responses = {}
    st.session_state.finish_time = None
    if next_page == "Quiz":
        st.session_state.deadline = time.time() + 60   # new 60-sec timer
    else:
        st.session_state.deadline = None
    st.session_state.page = next_page

# ---------------- HOME PAGE ---------------- #
if st.session_state.page == "Home":
    st.title("✨ Fun Quiz App ✨")
    st.markdown("Test your knowledge about Pakistan!")
    if st.button("🚀 Start Quiz", use_container_width=True):
        reset_quiz("Quiz")
        st.rerun()

# ---------------- QUIZ PAGE ---------------- #
elif st.session_state.page == "Quiz":
    # If user refreshed → go home
    if st.session_state.deadline is None:
        reset_quiz("Home")
        st.rerun()

    st.markdown("<h2 style='color:#9ACD32;'>Pakistan GK Quiz</h2>", unsafe_allow_html=True)

    remaining = max(0, int(st.session_state.deadline - time.time()))
    if remaining <= 0:
        st.session_state.finish_time = 60
        st.session_state.page = "Results"
        st.rerun()
    else:
        mins, secs = divmod(remaining, 60)
        st.subheader(f"⏳ Time left: {mins}:{secs:02d}")

        for q, d in QUIZ.items():
            st.session_state.responses[q] = st.radio(q, d["options"], key=q)

        if st.button("✅ Submit Quiz", use_container_width=True):
            st.session_state.finish_time = 60 - remaining
            st.session_state.page = "Results"
            st.rerun()

        time.sleep(1)
        st.rerun()

# ---------------- RESULTS PAGE ---------------- #
elif st.session_state.page == "Results":
    st.subheader("🎯 Your Results")
    total = len(QUIZ)
    correct = sum(
        1 for q, d in QUIZ.items()
        if st.session_state.responses.get(q) == d["answer"]
    )
    st.success(f"Score: {correct}/{total}  ({correct/total*100:.1f}%)")
    if st.session_state.finish_time is not None:
        st.info(f"Time used: {st.session_state.finish_time} seconds")

    st.write("### Answers")
    for q, d in QUIZ.items():
        user_ans = st.session_state.responses.get(q, "Not answered")
        if user_ans == d["answer"]:
            st.write(f"✅ {q} — Your answer: **{user_ans}**")
        else:
            st.write(f"❌ {q} — Your answer: **{user_ans}** | Correct: **{d['answer']}**")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔄 Restart Quiz", use_container_width=True):
            reset_quiz("Quiz")
            st.rerun()
    with c2:
        if st.button("🏠 Return Home", use_container_width=True):
            reset_quiz("Home")
            st.rerun()
