import os
from dotenv import load_dotenv
from google import genai
from datetime import datetime

load_dotenv()


class EnhancedSimpleAgent:
    """Enhanced conversational agent with memory and context"""

    def __init__(self, model_name="gemini-2.5-flash", system_instruction=None):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_name = model_name
        self.system_instruction = system_instruction or "You are a helpful AI assistant. Be concise and friendly."

        self.history = []
        self.conversation_count = 0
        self.start_time = datetime.now()

    # ================= CHAT =================
    def send_message(self, message: str) -> str:
        try:
            self.history.append({"role": "user", "parts": [{"text": message}]})

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=self.history,
                config={
                    "system_instruction": self.system_instruction
                }
            )

            reply = response.text
            self.history.append({"role": "model", "parts": [{"text": reply}]})

            self.conversation_count += 1
            return reply

        except Exception as e:
            return f"Error: {str(e)}"

    # ================= UTILITIES =================
    def get_history(self):
        return self.history

    def get_stats(self):
        duration = datetime.now() - self.start_time
        return {
            "messages": self.conversation_count,
            "duration": str(duration).split('.')[0],
            "model": self.model_name
        }

    def clear_history(self):
        self.history = []
        self.conversation_count = 0
        print("✓ Conversation history cleared!")

    def save_conversation(self, filename="conversation.txt"):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"=== Conversation Log ===\n")
            f.write(f"Model: {self.model_name}\n")
            f.write(f"Started: {self.start_time}\n\n")

            for msg in self.history:
                role = "You" if msg["role"] == "user" else "Agent"
                f.write(f"{role}: {msg['parts'][0]['text']}\n\n")

        print(f"✓ Conversation saved to {filename}")


# ================= INTERACTIVE CLI =================
def run_interactive_agent():
    print("=" * 60)
    print("🤖 Enhanced AI Agent - Powered by Gemini")
    print("=" * 60)
    print("\nCommands:")
    print("  exit / quit - Exit")
    print("  clear - Clear memory")
    print("  stats - Show session stats")
    print("  save - Save conversation")
    print("  help - Show commands\n")

    agent = EnhancedSimpleAgent()

    print("Agent: Hello! I'm your AI assistant.\n")

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit", "bye"]:
                stats = agent.get_stats()
                print("\n👋 Goodbye!")
                print(f"Session: {stats['messages']} messages in {stats['duration']}")
                break

            if user_input.lower() == "clear":
                agent.clear_history()
                continue

            if user_input.lower() == "stats":
                stats = agent.get_stats()
                print(stats)
                continue

            if user_input.lower() == "save":
                agent.save_conversation()
                continue

            if user_input.lower() == "help":
                print("exit | clear | stats | save")
                continue

            response = agent.send_message(user_input)
            print(f"\nAgent: {response}\n")

        except KeyboardInterrupt:
            print("\n👋 Interrupted!")
            break


# ================= PERSONALITY TEST =================
def test_personalities():
    personalities = [
        ("Professional", "You are a professional business assistant."),
        ("Tutor", "You are a friendly teacher explaining concepts simply."),
        ("Creative", "You are a creative storyteller.")
    ]

    for name, instruction in personalities:
        print(f"\n--- {name} ---")
        agent = EnhancedSimpleAgent(system_instruction=instruction)
        print(agent.send_message("Explain AI briefly."))


if __name__ == "__main__":
    run_interactive_agent()
