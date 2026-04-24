import streamlit as st
import time
from generator import generate_test

st.set_page_config(page_title="Processing Speed Test", layout="wide")

st.title("Processing Speed Test")

# --------------------------
# STICKY TIMER STYLE
# --------------------------

st.markdown("""
<style>
#timer-box {
    position: fixed;
    top: 10px;
    right: 20px;
    background-color: #000000;
    color: white;
    padding: 10px 20px;
    border-radius: 10px;
    font-size: 18px;
    z-index: 1000;
}
</style>
""", unsafe_allow_html=True)

# --------------------------
# SESSION STATE INIT
# --------------------------

if "started" not in st.session_state:
    st.session_state.started = False

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "test" not in st.session_state:
    st.session_state.test = None

if "submitted" not in st.session_state:
    st.session_state.submitted = False

# --------------------------
# START SCREEN
# --------------------------

if not st.session_state.started:
    st.write("### Instructions")
    st.write("""
    - You have **2 minutes** to complete the test  
    - Answer as many as you can accurately  
    - Test will auto-submit when time ends  
    """)

    if st.button("Start Test"):
        st.session_state.started = True
        st.session_state.start_time = time.time()
        st.session_state.test = generate_test()

    st.stop()

# --------------------------
# TIMER LOGIC
# --------------------------

TOTAL_TIME = 120  # seconds

elapsed = time.time() - st.session_state.start_time
remaining = int(TOTAL_TIME - elapsed)

# Sticky timer display
if remaining > 0:
    st.markdown(f"""
    <div id="timer-box">
    ⏳ {remaining} sec
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div id="timer-box">
    ⏰ Time's up!
    </div>
    """, unsafe_allow_html=True)

test = st.session_state.test

# --------------------------
# QUESTIONS
# --------------------------

disabled = remaining <= 0 or st.session_state.submitted

for i, q in enumerate(test):
    st.subheader(f"Q{i+1}. {q['question']}")

    st.radio(
        "Choose:",
        q["options"],
        index=None,
        key=f"q_{i}",
        disabled=disabled
    )

# --------------------------
# SUBMIT LOGIC
# --------------------------

submit_clicked = st.button("Submit")
time_up = remaining <= 0

# --------------------------
# CALCULATE SCORE (ONLY ONCE)
# --------------------------

if (submit_clicked or time_up) and not st.session_state.submitted:

    st.session_state.submitted = True

    score = 0
    total = len(test)

    for i, q in enumerate(test):
        selected = st.session_state.get(f"q_{i}")

        if selected is not None:
            idx = q["options"].index(selected)
            if chr(65 + idx) == q["answer"]:
                score += 1

    # ✅ store results
    st.session_state.score = score
    st.session_state.total = total
    st.session_state.percentage = (score / total) * 100

# --------------------------
# DISPLAY RESULT (PERSISTENT)
# --------------------------

if st.session_state.submitted:

    if remaining <= 0:
        st.warning("⏰ Time is up! Auto-submitting your test...")

    score = st.session_state.score
    total = st.session_state.total
    percentage = st.session_state.percentage

    st.success(f"Your Score: {score}/{total}")
    st.info(f"Percentage: {percentage:.1f}%")

    if percentage >= 85:
        st.success("Excellent processing speed")
    elif percentage >= 65:
        st.info("Good performance")
    else:
        st.warning("Needs improvement")

# --------------------------
# AUTO REFRESH TIMER
# --------------------------

if not st.session_state.submitted:
    time.sleep(1)
    st.rerun()