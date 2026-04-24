import streamlit as st
import time
from generator import generate_test

st.set_page_config(page_title="Processing Speed Test", layout="wide")

# --------------------------
# STRONG FIXED TIMER CSS
# --------------------------

st.markdown("""
<style>

/* push content down slightly */
.block-container {
    padding-top: 4rem;
}

/* floating timer */
.floating-timer {
    position: fixed;
    top: 20px;
    right: 30px;
    background: #111;
    color: white;
    padding: 14px 24px;
    border-radius: 12px;
    font-size: 22px;
    font-weight: bold;
    z-index: 999999999 !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    border: 2px solid white;
}

/* make sure Streamlit doesn't cover it */
header {
    z-index: 0 !important;
}

</style>
""", unsafe_allow_html=True)

st.title("Processing Speed Test")

# --------------------------
# SESSION STATE
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
    - You have **2 minutes**
    - Test auto-submits when time ends
    - Timer stays visible while scrolling
    """)

    if st.button("Start Test"):
        st.session_state.started = True
        st.session_state.start_time = time.time()
        st.session_state.test = generate_test()

    st.stop()

# --------------------------
# TIMER
# --------------------------

TOTAL_TIME = 120

elapsed = time.time() - st.session_state.start_time
remaining = int(TOTAL_TIME - elapsed)

if remaining < 0:
    remaining = 0

minutes = remaining // 60
seconds = remaining % 60

if remaining > 0:
    timer_html = f"""
    <div class="floating-timer">
        ⏳ {minutes:02d}:{seconds:02d}
    </div>
    """
else:
    timer_html = """
    <div class="floating-timer">
        ⏰ Time's Up!
    </div>
    """

st.markdown(timer_html, unsafe_allow_html=True)

# --------------------------
# QUESTIONS
# --------------------------

test = st.session_state.test
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
# SUBMIT
# --------------------------

submit_clicked = st.button("Submit")
time_up = remaining <= 0

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

    st.session_state.score = score
    st.session_state.total = total
    st.session_state.percentage = (score / total) * 100

# --------------------------
# RESULT
# --------------------------

if st.session_state.submitted:
    st.success(
        f"Your Score: {st.session_state.score}/{st.session_state.total}"
    )
    st.info(
        f"Percentage: {st.session_state.percentage:.1f}%"
    )

# --------------------------
# AUTO REFRESH
# --------------------------

if not st.session_state.submitted:
    time.sleep(1)
    st.rerun()