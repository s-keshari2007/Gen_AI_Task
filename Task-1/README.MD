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

3. **Dual Execution Mode (Web UI & Terminal CLI):**
   * Can be launched as a rich **Streamlit Web Stage UI** OR run directly in the **Terminal CLI**.

4. **Multi-LLM Engine & Instant Out-of-the-Box Demo:**
   * Works out-of-the-box in **Demo Mode** without needing any API keys.
   * Supports **Groq API** (`llama-3.3-70b`), **Google Gemini**, **OpenAI** (`gpt-4o-mini`), and **HuggingFace**.

---

## 🛠️ How to Run the Act

### Prerequisites
Make sure you have Python 3.9+ installed.

### 1. Clone & Install Dependencies
```bash
cd Gen_AI
pip install -r requirements.txt
```

### 2. Option A: Run via Web UI (Streamlit)
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

### 3. Option B: Run via Terminal CLI (No Browser Needed!)
```bash
python cli_main.py
```
Talk to the bot directly in your command line window!

---

## 📂 Codebase Structure

* `app.py` — Main Streamlit web application & India's Got Latent stage UI.
* `cli_main.py` — Terminal CLI interface for running the chatbot directly in command line.
* `chatbot_engine.py` — LangChain memory buffer manager and multi-provider LLM connector.
* `personas.py` — Definitions, system prompts, avatars, and character traits for all 6 personas.
* `requirements.txt` — Required Python packages.
* `README.md` — Contestant Profile documentation.

---

*Submitted for ACM BPHC GenAI Inductions 2026.*

