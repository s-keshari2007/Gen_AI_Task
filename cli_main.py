"""
India's Got Latent — Terminal CLI Stage Interface
Allows running the back-and-forth chatbot performance directly in the terminal without a browser.
"""

import sys
import os
from personas import PERSONAS, DEFAULT_PERSONA_KEY
from chatbot_engine import ChatbotEngine


def main():
    # UTF-8 stdout setup for Windows terminal emoji rendering
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    print("\n" + "=" * 60)
    print(" 🎙️  INDIA'S GOT LATENT — TERMINAL CHATBOT STAGE  🎙️")
    print("=" * 60)

    # 1. Select Persona
    print("\nSelect your Act (Persona):")
    persona_list = list(PERSONAS.keys())
    for idx, key in enumerate(persona_list, 1):
        p = PERSONAS[key]
        print(f" [{idx}] {p['name']} — {p['tagline']}")

    choice = input("\nEnter choice [1-6] (Default = 1 - RoastBot): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(persona_list):
        selected_key = persona_list[int(choice) - 1]
    else:
        selected_key = DEFAULT_PERSONA_KEY

    active_persona = PERSONAS[selected_key]
    print(f"\n🎭 Act Selected: {active_persona['name']}")
    print(f"💬 Tagline: \"{active_persona['sample_quote']}\"")

    # 2. Select Provider
    print("\nSelect AI Engine:")
    print(" [1] Demo Mode (Instant Offline - No API Key Needed)")
    print(" [2] Groq API")
    print(" [3] Google Gemini API")
    print(" [4] OpenAI API")
    prov_choice = input("Enter choice [1-4] (Default = 1): ").strip()

    provider_map = {"1": "demo", "2": "groq", "3": "gemini", "4": "openai"}
    provider = provider_map.get(prov_choice, "demo")

    api_key = None
    if provider != "demo":
        api_key = input(f"Enter your {provider.upper()} API Key: ").strip()

    # 3. Initialize Engine
    engine = ChatbotEngine(provider=provider, api_key=api_key)

    print("\n" + "-" * 60)
    print(f"STAGE IS LIVE! Talk to {active_persona['name']}.")
    print("Commands: Type 'reset' to clear memory, 'switch' to change persona, or 'exit' to quit.")
    print("-" * 60 + "\n")

    # 4. Interactive Back-and-Forth Chat Loop
    while True:
        try:
            user_input = input("👨‍⚖️ Judge: ").strip()
            if not user_input:
                continue

            lower_in = user_input.lower()
            if lower_in in ["exit", "quit", "q"]:
                print("\n🎭 Performance ended! The panel thanks you for watching India's Got Latent.\n")
                break

            if lower_in == "reset":
                engine.reset_memory()
                print("\n🧹 Memory cleared! Starting fresh performance on stage.\n")
                continue

            if lower_in == "switch":
                print("\nSelect new Persona:")
                for idx, key in enumerate(persona_list, 1):
                    print(f" [{idx}] {PERSONAS[key]['name']}")
                ch = input("Choice [1-6]: ").strip()
                if ch.isdigit() and 1 <= int(ch) <= len(persona_list):
                    selected_key = persona_list[int(ch) - 1]
                    active_persona = PERSONAS[selected_key]
                    print(f"🎭 Switched to: {active_persona['name']}\n")
                continue

            # Generate and print response
            response = engine.generate_response(user_input, persona_key=selected_key)
            print(f"\n🤖 {active_persona['name']}: {response}\n")

        except (KeyboardInterrupt, EOFError):
            print("\nExiting stage...")
            break


if __name__ == "__main__":
    main()
