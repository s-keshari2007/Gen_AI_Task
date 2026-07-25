# 🎭 Contestant Profile: The India's Got Latent Chatbot Challenge

> **Task 1 Submission — ACM BPHC GenAI Team Induction 2026**

---

## 🌟 Contestant Brief & Act Overview

* **Contestant Name:** Multi-Persona AI Act (`India's Got Latent Chatbot`)
* **Act Category:** Interactive Persona-Driven AI Comedy & Roast Bot
* **Stage Tagline:** *"Forget generic 'Hi, how can I help you?' bots. This bot roast-battles the panel, speaks Shakespeare, translates to emojis, and remembers every insult thrown at it!"*

---

## 🚀 Why This Act Will Impress Samay & The Panel

1. **Unmistakable Persona Toggles (6 Unique Acts in 1):**
   * 🔥 **RoastBot**: Fires back witty, sarcastic roasts no matter what curveballs the judges throw.
   * 🎭 **ShakespeareBot**: Answers every question in Early Modern Elizabethan dramatic verse.
   * 😂 **Emoji Translator Bot**: Converts thoughts into emoji storytelling with hilarious subtitles.
   * 🦹‍♂️ **Bollywood Villain Bot**: Channeling Mogambo, Crime Master Gogo, and Shakaal.
   * 🔮 **Overly-Dramatic Astrologer**: Blames judges' questions on Rahu-Ketu doshas & planetary retrogrades.
   * 🗝️ **Strict Hostel Warden**: Demands ID cards, enforces 8 PM curfew, and slaps Rs 500 fines.

2. **Long-Term Memory Across Turns:**
   * Powered by **LangChain's Stateful Memory Context**.
   * The bot doesn't forget — if a judge mentions their name or an insult in Question 1, the bot will call them out on it 3 questions later!
   * Built-in **Memory Context Inspector** UI accordion lets judges see the exact context window stored in real-time.

3. **Live Interactive Stage UI (Streamlit):**
   * Dark mode stage aesthetic with neon highlights, judge impression meters, and curveball trigger buttons.

4. **Multi-LLM Engine & Instant Out-of-the-Box Demo:**
   * Works out-of-the-box in **Demo Mode** without needing any API keys.
   * Supports **Groq API** (`llama-3.3-70b`), **Google Gemini**, **OpenAI** (`gpt-4o-mini`), and **HuggingFace**.

---

## 🛠️ How to Run the Act Locally

### Prerequisites
Make sure you have Python 3.9+ installed.

### 1. Clone & Install Dependencies
```bash
cd Gen_AI
pip install -r requirements.txt
```

### 2. Launch the Stage (Streamlit)
```bash
streamlit run app.py
```

### 3. (Optional) Set API Key for Real LLM Models
You can either enter your API key in the **Sidebar Panel** of the web UI or export it in your environment:
```bash
# Example for Groq
export GROQ_API_KEY="your_groq_api_key"

# Example for Gemini
export GOOGLE_API_KEY="your_gemini_api_key"
```

---

## 📂 Codebase Structure

* `app.py` — Main Streamlit web application & India's Got Latent stage UI.
* `chatbot_engine.py` — LangChain memory buffer manager and multi-provider LLM connector.
* `personas.py` — Definitions, system prompts, avatars, and character traits for all 6 personas.
* `requirements.txt` — Required Python packages.
* `README.md` — Contestant Profile documentation.

---

*Submitted for ACM BPHC GenAI Inductions 2026.*
