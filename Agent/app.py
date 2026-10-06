import streamlit as st

from ReAct import ask


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ReAct AI Assistant",
    page_icon="🤖",
    layout="centered",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main container */
    .main {
        padding-top: 2rem;
    }

    /* Header */
    .title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 17px;
        color: #777;
        margin-bottom: 30px;
    }

    /* Info card */
    .info-card {
        padding: 18px;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.25);
        margin-bottom: 25px;
    }

    /* Feature cards */
    .feature {
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(128, 128, 128, 0.2);
        text-align: center;
        min-height: 100px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="title">🤖 ReAct AI Assistant</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'LangGraph ReAct Agent • Ollama • DuckDuckGo'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# INFORMATION CARD
# ============================================================

st.markdown(
    """
    <div class="info-card">

    <b>How it works</b>

    <br><br>

    Your question is first analyzed by a router.

    <br><br>

    🔹 <b>Direct Question</b> → Ollama LLM

    <br>

    🔎 <b>Current / External Information</b> → LangGraph ReAct Agent → DuckDuckGo

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FEATURE SECTION
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="feature">
        🧠<br>
        <b>Local LLM</b><br>
        Ollama
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="feature">
        🔄<br>
        <b>ReAct Agent</b><br>
        LangGraph
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="feature">
        🔎<br>
        <b>Web Search</b><br>
        DuckDuckGo
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown("---")


# ============================================================
# CHAT HISTORY
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# DISPLAY PREVIOUS MESSAGES
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ============================================================
# USER INPUT
# ============================================================

user_input = st.chat_input(
    "Ask me anything..."
)


# ============================================================
# PROCESS USER QUESTION
# ============================================================

if user_input:

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response
    with st.chat_message("assistant"):

        with st.spinner(
            "Thinking..."
        ):

            try:

                response = ask(user_input)

                st.markdown(response)

                # Save assistant response
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response,
                    }
                )

            except Exception as error:

                error_message = (
                    f"Something went wrong: {error}"
                )

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                    }
                )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("⚙️ Settings")

    st.markdown(
        """
        ### About

        This application uses:

        - 🧠 **Gemini models**
        - 🔄 **LangGraph ReAct Agent**
        - 🔀 **RunnableBranch**
        - 🔎 **DuckDuckGo Search**
        - 💬 **Streamlit**

        ### Routing

        **DIRECT**

        General questions are answered directly by the local LLM.

        **TOOL**

        Questions requiring external information are routed to
        the ReAct agent.

        ---
        """
    )

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True,
    ):

        st.session_state.messages = []

        st.rerun()