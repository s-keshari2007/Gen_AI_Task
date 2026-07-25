"""
India's Got Latent — Chatbot Challenge
Streamlit Web Application & Stage Interface
"""

import streamlit as st
import time
from personas import PERSONAS, DEFAULT_PERSONA_KEY
from chatbot_engine import ChatbotEngine

# Set Page Config
st.set_page_config(
    page_title="India's Got Latent — Chatbot Stage",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Stage CSS
STAGE_CSS = """
<style>
/* Main Background & Theme */
.stApp {
    background: linear-gradient(135deg, #0a0a12 0%, #121225 50%, #1a0f2b 100%);
    color: #e0e0e0;
    font-family: 'Inter', sans-serif;
}

/* Stage Header Banner */
.stage-header {
    background: linear-gradient(90deg, #ff0055 0%, #7928ca 50%, #4338ca 100%);
    padding: 24px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(255, 0, 85, 0.3);
    margin-bottom: 25px;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.stage-title {
    font-size: 2.8rem;
    font-weight: 900;
    color: #ffffff;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin: 0;
    text-shadow: 0 2px 10px rgba(0,0,0,0.5);
}

.stage-subtitle {
    font-size: 1.1rem;
    color: #ffd700;
    margin-top: 6px;
    font-weight: 600;
}

/* Persona Card Widget */
.persona-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-radius: 12px;
    padding: 16px;
    border-left: 6px solid #ff0055;
    margin-bottom: 20px;
}

.persona-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: #ffffff;
    display: flex;
    align-items: center;
    gap: 10px;
}

.persona-quote {
    font-style: italic;
    color: #ffca28;
    margin-top: 8px;
    font-size: 0.95rem;
}

/* Judge Impression Meter */
.judge-meter-box {
    background: rgba(18, 18, 37, 0.8);
    border-radius: 12px;
    padding: 14px 20px;
    border: 1px solid rgba(255, 215, 0, 0.3);
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

/* Chat Message Customizations */
.stChatMessage {
    background-color: rgba(255, 255, 255, 0.04) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    padding: 12px !important;
    margin-bottom: 12px !important;
}

/* Sidebar Customization */
[data-testid="stSidebar"] {
    background-color: #0b0b14 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #ff0055 0%, #7928ca 100%);
    color: white;
    font-weight: 700;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(255, 0, 85, 0.4);
}
</style>
"""

st.markdown(STAGE_CSS, unsafe_allow_html=True)


# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_persona" not in st.session_state:
    st.session_state.selected_persona = DEFAULT_PERSONA_KEY

if "engine" not in st.session_state:
    st.session_state.engine = ChatbotEngine(provider="demo")

if "judge_score" not in st.session_state:
    st.session_state.judge_score = 85


# Sidebar Configuration Panel
with st.sidebar:
    st.image("https://img.icons8.com/emoji/96/000000/performing-arts.png", width=64)
    st.title("🎙️ Contestant Control Panel")
    st.caption("India's Got Latent — Backstage Setup")

    st.markdown("---")
    st.subheader("1. Select LLM Provider")
    provider = st.selectbox(
        "Choose AI Engine",
        options=["Demo (Instant Offline)", "Groq API", "Google Gemini", "OpenAI", "HuggingFace"],
        index=0,
        help="Select 'Demo' to test out-of-the-box, or plug in your API key for real LLM models.",
    )

    provider_key_map = {
        "Demo (Instant Offline)": "demo",
        "Groq API": "groq",
        "Google Gemini": "gemini",
        "OpenAI": "openai",
        "HuggingFace": "huggingface",
    }
    selected_provider = provider_key_map[provider]

    api_key = ""
    model_name = ""
    if selected_provider != "demo":
        api_key = st.text_input(
            f"Enter {provider} Key",
            type="password",
            help=f"Required to run {provider}. Left blank, fallback demo mode is used.",
        )
        if selected_provider == "groq":
            model_name = st.selectbox("Groq Model", ["llama-3.3-70b-versatile", "llama3-8b-8192", "mixtral-8x7b-32768"])
        elif selected_provider == "gemini":
            model_name = st.selectbox("Gemini Model", ["gemini-1.5-flash", "gemini-1.5-pro"])
        elif selected_provider == "openai":
            model_name = st.selectbox("OpenAI Model", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"])
        elif selected_provider == "huggingface":
            model_name = st.text_input("HF Model Repo", value="mistralai/Mistral-7B-Instruct-v0.2")

    temperature = st.slider("Comedy / Creativity Temp", min_value=0.1, max_value=1.2, value=0.8, step=0.1)

    st.markdown("---")
    st.subheader("2. Pick Your Act (Persona)")

    persona_keys = list(PERSONAS.keys())
    persona_names = [PERSONAS[k]["name"] for k in persona_keys]
    
    current_idx = persona_keys.index(st.session_state.selected_persona) if st.session_state.selected_persona in persona_keys else 0
    selected_name = st.radio(
        "Choose Persona",
        options=persona_names,
        index=current_idx,
    )

    # Update active persona
    new_persona_key = [k for k, v in PERSONAS.items() if v["name"] == selected_name][0]
    if new_persona_key != st.session_state.selected_persona:
        st.session_state.selected_persona = new_persona_key
        st.toast(f"🎭 Act Switched to: {PERSONAS[new_persona_key]['name']}", icon="✨")

    # Update Engine Instance
    st.session_state.engine.provider = selected_provider
    st.session_state.engine.api_key = api_key
    st.session_state.engine.model_name = model_name

    st.markdown("---")
    st.subheader("3. Stage Actions")
    if st.button("🗑️ Reset Memory & Stage", use_container_width=True):
        st.session_state.messages = []
        st.session_state.engine.reset_memory()
        st.session_state.judge_score = 85
        st.success("Memory cleared! Ready for a new performance.")
        st.rerun()


# Main Stage Interface
st.markdown(
    """
    <div class="stage-header">
        <h1 class="stage-title">India's Got Latent</h1>
        <div class="stage-subtitle">🌟 Chatbot Challenge Stage — Live Performance Mode 🌟</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Active Persona Banner
active_persona = PERSONAS[st.session_state.selected_persona]
badge_col = active_persona.get("badge_color", "#ff0055")

st.markdown(
    f"""
    <div class="persona-card" style="border-left-color: {badge_col};">
        <div class="persona-title">
            <span>{active_persona['avatar']}</span>
            <span>{active_persona['name']}</span>
        </div>
        <div style="color: #bbb; margin-top: 4px;">{active_persona['tagline']}</div>
        <div class="persona-quote">"{active_persona['sample_quote']}"</div>
        <div style="margin-top: 10px; font-size: 0.85rem; color: #888;">
            <b>Roast Intensity:</b> {active_persona['roast_level']} &nbsp;|&nbsp; 
            <b>Drama Index:</b> {active_persona['drama_level']}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Judge Panel Status & Scorecard
cols = st.columns([2, 1, 1])
with cols[0]:
    st.markdown(f"**Panel Impression Score:** `{'⭐' * (st.session_state.judge_score // 20)} ({st.session_state.judge_score}/100)`")
with cols[1]:
    st.markdown("**Buzzer Status:** `🟢 SAFE`")
with cols[2]:
    st.markdown(f"**Context Turns Retained:** `{len(st.session_state.messages) // 2}`")

# Context Inspector Drawer
with st.expander("🧠 LangChain Memory Context Inspector (Click to see what the bot remembers!)"):
    mem_turns = st.session_state.engine.get_memory_context()
    if not mem_turns:
        st.info("Memory buffer is currently empty. Ask a question to begin building context!")
    else:
        for idx, turn in enumerate(mem_turns):
            role_icon = "👨‍⚖️ Judge" if turn["role"] == "human" else f"🤖 {active_persona['name']}"
            st.markdown(f"**[{idx+1}] {role_icon}:** {turn['content']}")

st.markdown("---")

# Quick Curveball Buttons for Testing
st.markdown("##### ⚡ Quick Panel Curveballs (Click to ask instantly):")
curveball_cols = st.columns(4)
curveball_msg = ""
if curveball_cols[0].button("👋 'Introduce yourself!'"):
    curveball_msg = "Walk us through your act! Who are you and why are you on this stage?"
elif curveball_cols[1].button("💥 'Do you remember my name?'"):
    curveball_msg = "Call back to what I said 2 questions ago! Do you remember my name or details?"
elif curveball_cols[2].button("🌶️ 'Roast the panel!'"):
    curveball_msg = "Give Samay Raina and the judge panel your honest, unfiltered review!"
elif curveball_cols[3].button("🔮 'What is your secret weapon?'"):
    curveball_msg = "What makes your chatbot act better than the 100 generic bots before you?"

# Display Chat Messages
for msg in st.session_state.messages:
    avatar = "👨‍⚖️" if msg["role"] == "user" else active_persona["avatar"]
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# User Input Box
user_input = st.chat_input("Ask a question or throw a curveball at the bot on stage...")

# Process Input (either from curveball buttons or chat_input)
final_input = curveball_msg if curveball_msg else user_input

if final_input:
    # Display User message
    st.session_state.messages.append({"role": "user", "content": final_input})
    with st.chat_message("user", avatar="👨‍⚖️"):
        st.markdown(final_input)

    # Generate Bot Response
    with st.chat_message("assistant", avatar=active_persona["avatar"]):
        with st.spinner(f"{active_persona['name']} is thinking of a comeback..."):
            time.sleep(0.3)  # Smooth UX delay
            response = st.session_state.engine.generate_response(
                user_input=final_input,
                persona_key=st.session_state.selected_persona,
                temperature=temperature,
            )
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Adjust Judge Score based on engagement
    st.session_state.judge_score = min(100, st.session_state.judge_score + 2)
    st.rerun()
