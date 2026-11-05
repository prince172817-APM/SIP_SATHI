import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
import json

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="SIP Saathi",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------
# FILE STORAGE
# --------------------------------

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

FEEDBACK_FILE = DATA_DIR / "user_feedback.csv"
CHECKIN_FILE = DATA_DIR / "sip_checkins.csv"

# --------------------------------
# CUSTOM CSS
# --------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #f7faf8;
}

section[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #e5eee8;
}

.main-title {
    color: #087c45;
    font-size: 38px;
    font-weight: 800;
}

.subtitle {
    color: #64748b;
    font-size: 16px;
}

.metric-card {
    background: white;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #e4eee7;
    margin-bottom: 12px;
}

.metric-title {
    color: #64748b;
    font-size: 14px;
}

.metric-value {
    color: #087c45;
    font-size: 27px;
    font-weight: bold;
}

.info-card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #e4eee7;
    min-height: 145px;
}

.stButton > button {
    background-color: #087c45;
    color: white;
    border-radius: 8px;
    border: none;
    min-height: 42px;
}

.stButton > button:hover {
    background-color: #056536;
    color: white;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------
# KNOWLEDGE BASE
# --------------------------------

KNOWLEDGE = {

    "Failed SIP payment": {
        "description": "Understanding a failed SIP payment",
        "steps": [
            "Check whether your bank account has sufficient balance.",
            "Review any SMS or notification from your bank.",
            "Check whether your bank mandate is active.",
            "Review the SIP transaction status in your investment app.",
            "Contact your bank or Groww support if the issue continues."
        ]
    },

    "Missed SIP instalment": {
        "description": "Understanding a missed instalment",
        "steps": [
            "Check your transaction history.",
            "Confirm whether money was debited from your bank account.",
            "Review the notification received from your bank.",
            "Check your next scheduled SIP date.",
            "Contact platform support if the transaction status is unclear."
        ]
    },

    "Thinking about pausing": {
        "description": "Things to understand before pausing an SIP",
        "steps": [
            "Identify why you are considering pausing your SIP.",
            "Review your current financial commitments.",
            "Check the scheme and platform rules for pausing an SIP.",
            "Understand the consequences of missed instalments.",
            "Seek qualified financial advice if you need investment guidance."
        ]
    },

    "Understanding SIP": {
        "description": "Understanding how SIPs work",
        "steps": [
            "SIP stands for Systematic Investment Plan.",
            "It allows periodic investments into a mutual fund.",
            "The frequency depends on the selected SIP instructions.",
            "Mutual fund investments are subject to market risks.",
            "Read the relevant scheme documents before investing."
        ]
    },

    "Cancelling SIP": {
        "description": "Understanding SIP cancellation",
        "steps": [
            "Review your SIP details in the investment application.",
            "Check the official cancellation process.",
            "Review the next instalment date and applicable cut-off time.",
            "Check whether an instalment is already being processed.",
            "Contact platform support if you need account-specific help."
        ]
    }
}


# --------------------------------
# SIMPLE INTENT DETECTION
# --------------------------------

# --------------------------------
# KNOWLEDGE BASE RETRIEVAL
# --------------------------------

KNOWLEDGE_PATH = Path(__file__).parent / "knowledge" / "sip_knowledge.json"


def load_knowledge_base():
    with open(KNOWLEDGE_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


KNOWLEDGE_BASE = load_knowledge_base()


def detect_problem(question):
    text = question.lower()

    best_match = None
    highest_score = 0

    for item in KNOWLEDGE_BASE:
        score = sum(
            1 for keyword in item["keywords"]
            if keyword.lower() in text
        )

        if score > highest_score:
            highest_score = score
            best_match = item["topic"]

    return best_match


def get_knowledge_item(category):
    for item in KNOWLEDGE_BASE:
        if item["topic"] == category:
            return item

    return None


# --------------------------------
# SAVE FEEDBACK
# --------------------------------

def save_feedback(problem, rating, comment):

    row = pd.DataFrame([{
        "date": datetime.now().isoformat(),
        "problem": problem,
        "rating": rating,
        "comment": comment
    }])

    if FEEDBACK_FILE.exists():
        row.to_csv(
            FEEDBACK_FILE,
            mode="a",
            header=False,
            index=False
        )
    else:
        row.to_csv(FEEDBACK_FILE, index=False)


# --------------------------------
# SIDEBAR
# --------------------------------

with st.sidebar:

    st.markdown(
        '<h1 style="color:#087c45;">🌱 SIP Saathi</h1>',
        unsafe_allow_html=True
    )

    st.caption("Your SIP continuity companion")

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Dashboard",
            "SIP Help Centre",
            "Monthly Check-in",
            "Product Insights",
            "About"
        ]
    )

    st.divider()

    st.caption("Independent product concept")
    st.caption("Groww case study | 2026")


# =================================
# DASHBOARD
# =================================

if page == "Dashboard":

    st.markdown(
        '<div class="main-title">Welcome to SIP Saathi 👋</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Understand your SIP journey with simple, '
        'helpful guidance.</div>',
        unsafe_allow_html=True
    )

    st.write("")

    st.success(
        "Your SIP support centre is ready. "
        "Choose a service below to get started."
    )

    st.subheader("Your support centre")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="info-card">
        <h3>💳 Payment Support</h3>
        <p>Understand failed payments and bank mandate issues.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-card">
        <h3>📅 SIP Check-in</h3>
        <p>Record your SIP experience and recurring difficulties.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="info-card">
        <h3>🤖 SIP Assistant</h3>
        <p>Get simple explanations and troubleshooting guidance.</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    st.subheader("What would you like help with?")

    selected = st.selectbox(
        "Select your concern",
        [
            "Choose a concern",
            "Failed SIP payment",
            "Missed SIP instalment",
            "Thinking about pausing",
            "Understanding SIP",
            "Cancelling SIP"
        ]
    )

    if st.button("Explore support"):

        if selected == "Choose a concern":
            st.warning("Please select a concern.")

        else:
            st.session_state.selected_problem = selected
            st.session_state.navigate_to_help = True
            st.rerun()


# =================================
# SIP HELP CENTRE
# =================================

elif page == "SIP Help Centre":

    st.markdown(
        '<div class="main-title">SIP Help Centre</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Describe your SIP problem and receive "
        "simple educational guidance."
    )

   # Keep the answer available after Streamlit refreshes
    # Keep the answer available after Streamlit refreshes
    if "current_answer" not in st.session_state:
        st.session_state.current_answer = None

    if "current_category" not in st.session_state:
        st.session_state.current_category = None

    question = st.text_area(
        "Describe your problem",
        placeholder="Example: My SIP payment failed this month..."
    )

    if st.button("Get AI-assisted guidance"):

        if not question.strip():
            st.session_state.current_answer = None
            st.warning("Please describe your problem.")

        else:
            category = detect_problem(question)

            if category is None:
                st.session_state.current_answer = None
                st.info(
                    "We couldn't confidently identify your concern. "
                    "Try words such as payment failed, missed instalment, "
                    "pause or cancellation."
                )

            else:
                item = get_knowledge_item(category)

                if item is None:
                    st.session_state.current_answer = None
                    st.error("We couldn't find guidance for this topic.")

                else:
                    st.session_state.current_category = category

                    steps = (
                        item.get("steps")
                        or KNOWLEDGE.get(category, {}).get("steps")
                        or [
                            "Review the guidance provided above.",
                            "Check the official source for the latest instructions."
                        ]
                    )

                    st.session_state.current_answer = {
                        "description": item["answer"],
                        "steps": steps,
                        "source": item["source"],
                        "topic": item["topic"]
                    }

    # Display the saved answer OUTSIDE the button condition
    if st.session_state.current_answer is not None:

        answer = st.session_state.current_answer

        st.divider()

        st.subheader("🌱 SIP Saathi Assistant")

        st.success(answer["description"])

        st.write("Suggested troubleshooting steps:")

        for index, step in enumerate(answer["steps"], 1):
            st.markdown(f"**{index}.** {step}")

        st.caption(
            "This is general educational information, not financial "
            "or investment advice. It does not access your Groww account."
        )

        st.write("Source:", answer["source"])

        st.divider()

        st.subheader("Was this answer helpful?")

        rating = st.radio(
            "Your feedback",
            ["Helpful", "Partially helpful", "Not helpful"],
            key="help_rating"
        )

        comment = st.text_area(
            "Additional feedback (optional)",
            key="help_comment"
        )

        if st.button("Submit response feedback"):
            save_feedback(
                st.session_state.current_category,
                rating,
                comment
            )
            st.success("Thank you! Your feedback has been saved.")

# =================================
# MONTHLY CHECK-IN
# =================================

elif page == "Monthly Check-in":

    st.markdown(
        '<div class="main-title">Monthly SIP Check-in</div>',
        unsafe_allow_html=True
    )

    st.write(
        "A quick check-in to understand your SIP experience."
    )

    with st.form("checkin_form"):

        experience = st.selectbox(
            "How has your SIP experience been?",
            [
                "Smooth",
                "Experienced payment problems",
                "Missed an instalment",
                "Considering pausing",
                "Need more information"
            ]
        )

        confidence = st.slider(
            "How confident do you feel managing your SIP?",
            1, 5, 3
        )

        difficulty = st.text_area(
            "What was your biggest difficulty this month?"
        )

        submitted = st.form_submit_button("Save check-in")

        if submitted:

            row = pd.DataFrame([{
                "date": datetime.now().isoformat(),
                "experience": experience,
                "confidence": confidence,
                "difficulty": difficulty
            }])

            if CHECKIN_FILE.exists():

                row.to_csv(
                    CHECKIN_FILE,
                    mode="a",
                    header=False,
                    index=False
                )

            else:

                row.to_csv(CHECKIN_FILE, index=False)

            st.success("Your check-in has been saved!")


# =================================
# PRODUCT INSIGHTS
# =================================

elif page == "Product Insights":

    st.markdown(
        '<div class="main-title">Product Insights</div>',
        unsafe_allow_html=True
    )

    st.write(
        "An overview of feedback collected through the SIP Saathi prototype."
    )

    if FEEDBACK_FILE.exists():

        feedback = pd.read_csv(FEEDBACK_FILE)

        st.metric("Feedback submissions", len(feedback))

        if not feedback.empty:

            st.subheader("User feedback")

            st.dataframe(
                feedback,
                use_container_width=True
            )

            st.subheader("Feedback distribution")

            st.bar_chart(
                feedback["rating"].value_counts()
            )

    else:

        st.info(
            "No feedback collected yet. "
            "User feedback will appear here after testing."
        )

    if CHECKIN_FILE.exists():

        checkins = pd.read_csv(CHECKIN_FILE)

        st.subheader("Monthly check-ins")

        st.metric("Total check-ins", len(checkins))

        st.dataframe(
            checkins,
            use_container_width=True
        )


# =================================
# ABOUT
# =================================

elif page == "About":

    st.markdown(
        '<div class="main-title">About SIP Saathi</div>',
        unsafe_allow_html=True
    )

    st.write("""
    SIP Saathi is an independent product concept developed as part
    of a Product Management graduation project using Groww as the
    selected case-study company.

    ### Product vision

    Help first-time mutual fund investors better understand and
    manage common SIP-related difficulties.

    ### Product principles

    - Simple educational guidance.
    - Clear and understandable explanations.
    - Responsible AI-assisted support.
    - No investment recommendations.
    - No access to personal financial accounts.

    ### Current technology

    - Python
    - Streamlit
    - Pandas
    - Rule-based intent detection
    - Curated knowledge retrieval

    ### Product status

    Working MVP prototype under development.
    """)

st.divider()

st.caption(
    "SIP Saathi | Independent Groww case-study prototype | "
    "Not an official Groww product"
)
# CUSTOM CSS
st.markdown("""
<style>

/* Main application */
.stApp {
    background-color: #f7faf8;
    color: #1f2937;
}

/* Main content */
section.main {
    background-color: #f7faf8;
}

h1, h2, h3, h4, p, label {
    color: #1f2937;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #ffffff;
}

section[data-testid="stSidebar"] * {
    color: #26352d;
}

/* Dashboard cards */
.info-card {
    background-color: #ffffff;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #e4eee7;
    min-height: 145px;
    color: #26352d;
}

.info-card h3 {
    color: #087c45 !important;
}

.info-card p {
    color: #64748b !important;
}

/* Main title */
.main-title {
    color: #087c45 !important;
    font-size: 38px;
    font-weight: 800;
}

/* Subtitle */
.subtitle {
    color: #64748b !important;
    font-size: 16px;
}

/* Buttons */
.stButton > button {
    background-color: #087c45;
    color: white !important;
    border-radius: 8px;
    border: none;
    min-height: 42px;
}

.stButton > button:hover {
    background-color: #056536;
    color: white !important;
}

/* Input fields */
input, textarea {
    color: #1f2937 !important;
}

/* Metrics */
[data-testid="stMetricValue"] {
    color: #087c45;
}

</style>
""", unsafe_allow_html=True)