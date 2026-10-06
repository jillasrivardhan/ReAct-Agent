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

    .main {
        padding-top: 2rem;
    }

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

    .info-card {
        padding: 18px;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.25);
        margin-bottom: 25px;
    }

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
    '<div class="title">'
    '🤖 ReAct AI Assistant'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'LangGraph ReAct Agent • '
    'OpenAI • DuckDuckGo'
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

    🔹 <b>Direct Question</b>
    → OpenAI GPT-4.1 Mini

    <br>

    🔎 <b>Current / External Information</b>
    → LangGraph ReAct Agent
    → DuckDuckGo Search

    <br><br>

    You provide your own OpenAI API key.
    Your key is used for your current session.

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

        <b>OpenAI</b><br>

        GPT-4.1 Mini

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
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title(
        "⚙️ Settings"
    )

    # ========================================================
    # API KEY INPUT
    # ========================================================

    st.subheader(
        "🔑 OpenAI API Key"
    )

    user_api_key = st.text_input(
        "Enter your OpenAI API key",
        type="password",
        placeholder="sk-...",
        help=(
            "Your API key is used only "
            "for your current session."
        ),
    )

    # --------------------------------------------------------
    # API KEY STATUS
    # --------------------------------------------------------

    if user_api_key:

        st.success(
            "API key provided."
        )

    else:

        st.warning(
            "API key required."
        )

    st.caption(
        "🔒 The application does not save "
        "your API key to the project database."
    )

    st.markdown("---")

    # ========================================================
    # ABOUT
    # ========================================================

    st.markdown(
        """
        ### About

        This application uses:

        - 🧠 **OpenAI GPT-4.1 Mini**
        - 🔄 **LangGraph ReAct Agent**
        - 🔀 **RunnableBranch**
        - 🔎 **DuckDuckGo Search**
        - 💬 **Streamlit**

        ### Routing

        **DIRECT**

        General questions are answered
        directly by OpenAI.

        **TOOL**

        Questions requiring external
        information are routed to
        the ReAct agent.

        The ReAct agent can call the
        DuckDuckGo search tool when
        necessary.

        ---
        """
    )

    # ========================================================
    # CLEAR CHAT
    # ========================================================

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True,
    ):

        st.session_state.messages = []

        st.rerun()


# ============================================================
# CHAT HISTORY
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


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

    # --------------------------------------------------------
    # API KEY CHECK
    # --------------------------------------------------------

    if not user_api_key:

        st.warning(
            "Please enter your OpenAI API key "
            "in the sidebar first."
        )

        st.stop()


    # --------------------------------------------------------
    # SAVE USER MESSAGE
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )


    # --------------------------------------------------------
    # DISPLAY USER MESSAGE
    # --------------------------------------------------------

    with st.chat_message(
        "user"
    ):

        st.markdown(
            user_input
        )


    # --------------------------------------------------------
    # GENERATE RESPONSE
    # --------------------------------------------------------

    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "Thinking..."
        ):

            try:

                # IMPORTANT:
                #
                # Pass the visitor's API key.
                #
                # NOT your API key.
                #
                response = ask(
                    user_input,
                    user_api_key,
                )

                st.markdown(
                    response
                )

                # ------------------------------------------------
                # SAVE ASSISTANT MESSAGE
                # ------------------------------------------------

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response,
                    }
                )

            except Exception as error:

                error_message = (
                    f"Something went wrong: "
                    f"{error}"
                )

                st.error(
                    error_message
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                    }
                )