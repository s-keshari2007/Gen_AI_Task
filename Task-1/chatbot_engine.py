"""
Chatbot Engine using LangChain for memory management and multi-provider LLM support.
Supports Groq, Google Gemini, OpenAI, HuggingFace, and a smart local Demo Fallback Engine.
"""

import os
import random
from typing import Dict, List, Any, Optional

# LangChain Imports
try:
    from langchain.memory import ConversationBufferMemory
    from langchain.schema import SystemMessage, HumanMessage, AIMessage
except ImportError:
    ConversationBufferMemory = None

from personas import PERSONAS, DEFAULT_PERSONA_KEY


class ChatbotEngine:
    def __init__(self, provider: str = "demo", api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.provider = provider.lower()
        self.api_key = api_key or os.getenv("LLM_API_KEY", "")
        self.model_name = model_name
        self.memory_history: List[Dict[str, str]] = []  # List of {"role": "human"|"ai", "content": "..."}

    def reset_memory(self):
        """Clears the chat context memory."""
        self.memory_history = []

    def get_memory_context(self) -> List[Dict[str, str]]:
        """Returns the current conversation memory context."""
        return self.memory_history

    def generate_response(
        self, user_input: str, persona_key: str = DEFAULT_PERSONA_KEY, temperature: float = 0.7
    ) -> str:
        """
        Generates a response given user input, selected persona, and conversation memory context.
        """
        persona = PERSONAS.get(persona_key, PERSONAS[DEFAULT_PERSONA_KEY])
        system_prompt = persona["system_prompt"]

        # 1. Try real LLM providers if API key is provided
        if self.provider == "groq" and self.api_key:
            response = self._call_groq(user_input, system_prompt, temperature)
            if response:
                self._record_turn(user_input, response)
                return response

        elif self.provider == "gemini" and self.api_key:
            response = self._call_gemini(user_input, system_prompt, temperature)
            if response:
                self._record_turn(user_input, response)
                return response

        elif self.provider == "openai" and self.api_key:
            response = self._call_openai(user_input, system_prompt, temperature)
            if response:
                self._record_turn(user_input, response)
                return response

        elif self.provider == "huggingface" and self.api_key:
            response = self._call_huggingface(user_input, system_prompt, temperature)
            if response:
                self._record_turn(user_input, response)
                return response

        # 2. Fallback / Demo Engine (Smart offline generator with full context memory)
        response = self._generate_demo_response(user_input, persona)
        self._record_turn(user_input, response)
        return response

    def _record_turn(self, user_input: str, ai_response: str):
        """Appends human and AI turns to memory history."""
        self.memory_history.append({"role": "human", "content": user_input})
        self.memory_history.append({"role": "ai", "content": ai_response})

    def _call_groq(self, user_input: str, system_prompt: str, temperature: float) -> Optional[str]:
        try:
            from langchain_groq import ChatGroq
            model = self.model_name or "llama-3.3-70b-versatile"
            llm = ChatGroq(groq_api_key=self.api_key, model_name=model, temperature=temperature)
            
            messages = [SystemMessage(content=system_prompt)]
            for turn in self.memory_history:
                if turn["role"] == "human":
                    messages.append(HumanMessage(content=turn["content"]))
                else:
                    messages.append(AIMessage(content=turn["content"]))
            messages.append(HumanMessage(content=user_input))
            
            res = llm.invoke(messages)
            return res.content
        except Exception as e:
            print(f"Groq API Call failed: {e}")
            return None

    def _call_gemini(self, user_input: str, system_prompt: str, temperature: float) -> Optional[str]:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            model = self.model_name or "gemini-1.5-flash"
            llm = ChatGoogleGenerativeAI(google_api_key=self.api_key, model=model, temperature=temperature)
            
            messages = [SystemMessage(content=system_prompt)]
            for turn in self.memory_history:
                if turn["role"] == "human":
                    messages.append(HumanMessage(content=turn["content"]))
                else:
                    messages.append(AIMessage(content=turn["content"]))
            messages.append(HumanMessage(content=user_input))
            
            res = llm.invoke(messages)
            return res.content
        except Exception as e:
            print(f"Gemini API Call failed: {e}")
            return None

    def _call_openai(self, user_input: str, system_prompt: str, temperature: float) -> Optional[str]:
        try:
            from langchain_openai import ChatOpenAI
            model = self.model_name or "gpt-4o-mini"
            llm = ChatOpenAI(openai_api_key=self.api_key, model=model, temperature=temperature)
            
            messages = [SystemMessage(content=system_prompt)]
            for turn in self.memory_history:
                if turn["role"] == "human":
                    messages.append(HumanMessage(content=turn["content"]))
                else:
                    messages.append(AIMessage(content=turn["content"]))
            messages.append(HumanMessage(content=user_input))
            
            res = llm.invoke(messages)
            return res.content
        except Exception as e:
            print(f"OpenAI API Call failed: {e}")
            return None

    def _call_huggingface(self, user_input: str, system_prompt: str, temperature: float) -> Optional[str]:
        try:
            from langchain_community.llms import HuggingFaceHub
            model = self.model_name or "mistralai/Mistral-7B-Instruct-v0.2"
            llm = HuggingFaceHub(huggingfacehub_api_token=self.api_key, repo_id=model, model_kwargs={"temperature": temperature})
            
            full_prompt = f"{system_prompt}\n\n"
            for turn in self.memory_history:
                role = "User" if turn["role"] == "human" else "Bot"
                full_prompt += f"{role}: {turn['content']}\n"
            full_prompt += f"User: {user_input}\nBot:"
            
            res = llm.invoke(full_prompt)
            return res
        except Exception as e:
            print(f"HuggingFace API Call failed: {e}")
            return None

    def _generate_demo_response(self, user_input: str, persona: Dict[str, Any]) -> str:
        """
        Smart, context-aware demo response generator for offline / out-of-the-box testing.
        Incorporates dynamic memory callbacks across turns.
        """
        pid = persona["id"]
        turn_count = len(self.memory_history) // 2 + 1
        
        # Build dynamic memory callback referencing past turns dynamically
        memory_callback = ""
        if self.memory_history:
            prev_user_msgs = [m["content"] for m in self.memory_history if m["role"] == "human"]
            if prev_user_msgs:
                # Pick a relevant past turn or the latest turn
                if turn_count == 2:
                    memory_callback = f"\n\n*(🧠 Memory Callback: I remember in your first question you said '{prev_user_msgs[0]}')*"
                elif turn_count > 2:
                    last_msg = prev_user_msgs[-1]
                    memory_callback = f"\n\n*(🧠 Memory Callback: That's turn #{turn_count}! Right after you asked '{last_msg}', you bring this up?)*"

        lower_in = user_input.lower()

        if pid == "roastbot":
            roasts = [
                f"Oh wow, another classic question from the panel! *'{user_input}'*? I've seen better interrogation skills in a pre-school quiz.{memory_callback}",
                f"Judge, if I had a rupee for every time someone asked *'{user_input}'*, I'd buy this stage and fire the panel!{memory_callback}",
                f"Is asking *'{user_input}'* your secret strategy to buzz me off stage? The audience is checking their phones!{memory_callback}",
                f"Bold of you to ask *'{user_input}'*. Did you spend all night preparing that or did it just slip out by accident?{memory_callback}",
            ]
            return random.choice(roasts)

        elif pid == "shakespeare":
            speeches = [
                f"Hark, noble judge! Thou utterest words of grand curiosity: *'{user_input}'*!\n\nYet methinks thine inquiry doth echo through the halls of history like thunder upon the heath!{memory_callback}",
                f"Verily, I say unto thee, O sovereign panelist!\n\nTo answer or not to answer, that is the dilemma. Thou speakest: *'{user_input}'*, and my poet's heart doth tremble in theatrical dismay!{memory_callback}",
                f"Fair magistrate of the realm! By my troth, thy question *'{user_input}'* shall be written in the annals of comedic tragedy!{memory_callback}",
            ]
            return random.choice(speeches)

        elif pid == "emoji":
            emoji_combos = [
                f"🤯🎭 ➡️ 🎤💥 ➡️ 🤦‍♂️❌\n\n**Translation:** Your statement *'{user_input}'* left the entire auditorium in shock! Buzzers are glowing!{memory_callback}",
                f"🔥⚡ ➡️ 🌶️🤪 ➡️ 🏆✨\n\n**Translation:** Hot take detected on *'{user_input}'*! That question was spicier than a street samosa!{memory_callback}",
                f"🧐📜 ➡️ 🤡🎪 ➡️ 🏃‍♂️💨\n\n**Translation:** The judges are examining *'{user_input}'*, but it looks like a circus show!{memory_callback}",
            ]
            return random.choice(emoji_combos)

        elif pid == "bollywood_villain":
            dialogues = [
                f"*Muahaha!* Tumne pucha: *'{user_input}'*? Crime Master Gogo aaya hai, kuch toh lekar jaayega — aur tumhara calm posture le gaya!{memory_callback}",
                f"Mogambo khush hua... lekin tumhari iss baat *'{user_input}'* ne Mogambo ka dimaag kharab kar diya! Shakaal ko bulao!{memory_callback}",
                f"Kitne aadmi the, judge saab? Jo *'{user_input}'* jaise sawaal puchte hain? Yeh 'India's Got Latent' hai, Gabbar ka kila nahi!{memory_callback}",
            ]
            return random.choice(dialogues)

        elif pid == "astrologer":
            horoscopes = [
                f"🔮 **Cosmic Alert!** Mercury is currently doing a backflip in your 4th house!\n\nYour question *'{user_input}'* clearly shows Rahu interfering with your wifi and your karma today!{memory_callback}",
                f"✨ **Star Alignment:** The aura around the panel turned neon purple when you asked *'{user_input}'*. I predict 85% chance of emotional turbulence and 100% chance of comedy!{memory_callback}",
                f"🌌 **Tarot Reading:** The cards reveal that Saturn is frowning upon *'{user_input}'*. Wear yellow tomorrow to fix this energy!{memory_callback}",
            ]
            return random.choice(horoscopes)

        elif pid == "hostel_warden":
            rules = [
                f"🚨 **RULES VIOLATION!** It is past gate curfew and you are asking: *'{user_input}'*?\n\nWhere is your college ID card?! Fine imposed: Rs. 500!{memory_callback}",
                f"🗝️ **ATTENTION HOSTELITES:** No talking on stage without permission! Your statement *'{user_input}'* will be reported to the Chief Warden tomorrow morning!{memory_callback}",
                f"😠 **MESS COMMITTEE NOTICE:** First you complain about mess food, now you ask *'{user_input}'*? Hand over your hall ticket right now!{memory_callback}",
            ]
            return random.choice(rules)

        return f"The Bot listened carefully to *'{user_input}'* and holds the context in memory!{memory_callback}"
