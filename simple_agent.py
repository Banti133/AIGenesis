import os
from dotenv import load_dotenv
from google import genai
from typing import List, Dict

load_dotenv()

class SimpleAgent:
    """🚀 2026 SimpleAgent - PRODUCTION READY"""
    
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        """Initialize with your confirmed working model"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("❌ GEMINI_API_KEY missing from .env file")
        
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self.chat = self.client.chats.create(model=model_name)
        print(f"✅ Agent ready: {model_name}")
    
    def send_message(self, message: str) -> str:
        """Send message and get response (native chat session)"""
        try:
            response = self.chat.send_message(message)
            return response.text.strip()
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def get_history(self) -> List[Dict]:
        """Get chat history using correct 2026 API"""
        try:
            return self.chat.get_history()
        except Exception as e:
            return [{"role": "error", "content": f"History error: {e}"}]
    
    def clear_history(self) -> str:
        """Start fresh conversation"""
        self.chat = self.client.chats.create(model=self.model_name)
        return "✅ Chat history cleared!"
    
    def get_stats(self) -> Dict:
        """Conversation statistics"""
        history = self.get_history()
        messages = len(history)
        human_msgs = len([m for m in history if hasattr(m, 'role') and m.role == "user"])
        ai_msgs = len([m for m in history if hasattr(m, 'role') and m.role == "model"])
        
        return {
            "total_messages": messages,
            "human_messages": human_msgs,
            "ai_messages": ai_msgs,
            "session_active": True
        }

def main():
    """🚀 Enhanced interactive interface"""
    print("=" * 65)
    print("🤖 SIMPLE AGENT v2.0 - 2026 PRODUCTION EDITION")
    print("✅ gemini-2.5-flash | Native Chat | Full Stats")
    print("=" * 65)
    print("💬 Commands: 'help' | 'stats' | 'clear' | 'exit'")
    print("=" * 65)
    
    agent = SimpleAgent()
    print("\n🤖 Agent: Hello! I'm your 2026 AI assistant.")
    print("💡 Ask anything technical or type 'help' for commands!\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                print("💭 (type 'help' for commands)")
                continue
                
            # 🚀 Commands
            if user_input.lower() == "exit":
                print("\n🤖 Agent: Goodbye! 👋")
                stats = agent.get_stats()
                print(f"📊 Session complete: {stats['human_messages']} questions, {stats['ai_messages']} responses")
                break
                
            elif user_input.lower() == "help":
                print("\n📋 Available Commands:")
                print("  • 'stats'     - Show conversation statistics")
                print("  • 'clear'     - Reset chat history")  
                print("  • 'exit'      - End session")
                print("  • Anything    - Ask your AI assistant!\n")
                continue
                
            elif user_input.lower() == "stats":
                stats = agent.get_stats()
                print(f"\n📊 Live Chat Statistics:")
                print(f"  ├─ Total exchanges: {stats['total_messages']}")
                print(f"  ├─ Your questions:  {stats['human_messages']}")
                print(f"  └─ AI responses:   {stats['ai_messages']}")
                print(f"     {'🟢 Session Active' if stats['session_active'] else '🔴 Inactive'}\n")
                continue
                
            elif user_input.lower() == "clear":
                response = agent.clear_history()
                print(f"\n🤖 Agent: {response}")
                continue
            
            # 💬 Normal conversation
            print("🤖 Agent: ", end="", flush=True)
            response = agent.send_message(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\n\n🤖 Agent: Chat interrupted. Goodbye! 👋")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
