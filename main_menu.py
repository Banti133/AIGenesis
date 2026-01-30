import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if API key is set
if not os.getenv('GEMINI_API_KEY'):
    print("❌ Error: GEMINI_API_KEY not found in .env file")
    print("\nPlease create a .env file with your Gemini API key:")
    print("GEMINI_API_KEY=your_key_here")
    sys.exit(1)

def print_header():
    """Print application header"""
    print("\n" + "=" * 70)
    print("🤖 AI AGENTS SYSTEM - Powered by Google Gemini")
    print("=" * 70)

def print_menu():
    """Print main menu"""
    print("\n📋 Available Agents:\n")
    print("  1. 💬 Simple Conversational Agent")
    print("     → Basic chat with conversation memory and commands")
    print()
    print("  2. 🛡️  Guardrail Agent")
    print("     → Agent with input/output validation and safety checks")
    print()
    print("  3. 🔧 Custom Agent Builder")
    print("     → Build agents with custom tools and capabilities")
    print()
    print("  4. 📚 RAG Agent (Basic)")
    print("     → Simple retrieval-augmented generation")
    print()
    print("  5. 📖 Advanced RAG Agent")
    print("     → Enhanced RAG with document processing and search")
    print()
    print("  6. 🌟 Multi-Agent System")
    print("     → Multiple specialized agents with intelligent routing")
    print()
    print("  7. 🧪 Test All Agents")
    print("     → Quick demo of all agent capabilities")
    print()
    print("  0. ❌ Exit")
    print("\n" + "=" * 70)

def run_simple_agent():
    """Run simple conversational agent"""
    try:
        from enhanced_simple_agent import run_interactive_agent
        run_interactive_agent()
    except ImportError:
        from simple_agent import SimpleAgent
        print("\n--- Simple Agent ---")
        print("Commands: 'exit' to quit\n")
        agent = SimpleAgent()
        print("Agent: Hello! How can I help you today?")
        while True:
            msg = input("\nYou: ").strip()
            if msg.lower() in ['exit', 'quit']:
                print("\nAgent: Goodbye! 👋\n")
                break
            if msg:
                response = agent.send_message(msg)
                print(f"Agent: {response}")

def run_guardrail_agent():
    """Run guardrail agent"""
    from agent_with_guardrails import GuardrailAgent
    print("\n--- Guardrail Agent (with Safety Checks) ---")
    print("Commands: 'exit' to quit\n")
    agent = GuardrailAgent()
    print("Agent: Hello! I have safety checks enabled. Try me!")
    while True:
        msg = input("\nYou: ").strip()
        if msg.lower() in ['exit', 'quit']:
            print("\nAgent: Goodbye! 👋\n")
            break
        if msg:
            response = agent.process(msg)
            print(f"Agent: {response}")

def run_agent_builder():
    """Run custom agent builder"""
    from agent_builder import AgentBuilder, Tool, get_current_time
    print("\n--- Custom Agent Builder ---")
    print("Commands: 'exit' to quit\n")
    
    agent = AgentBuilder(
        role="Helpful Assistant",
        instructions="Be helpful, friendly, and use tools when appropriate."
    )
    agent.add_tool(Tool("get_time", "Get current time", get_current_time))
    
    print("Agent: Hello! I'm a custom agent with tools. Ask me anything!")
    while True:
        msg = input("\nYou: ").strip()
        if msg.lower() in ['exit', 'quit']:
            print("\nAgent: Goodbye! 👋\n")
            break
        if msg:
            response = agent.chat(msg)
            print(f"Agent: {response}")

def run_basic_rag():
    """Run basic RAG agent"""
    from rag_agent import SimpleRAGAgent
    print("\n--- Basic RAG Agent ---")
    print("Commands: 'exit' to quit\n")
    
    agent = SimpleRAGAgent()
    
    # Add sample knowledge
    print("📥 Loading sample knowledge base...")
    agent.add_knowledge("Python is a high-level programming language created by Guido van Rossum in 1991.")
    agent.add_knowledge("AI agents are autonomous programs that can perceive and act on their environment.")
    agent.add_knowledge("Machine learning is a subset of AI that learns from data without explicit programming.")
    print("✓ Knowledge base loaded!\n")
    
    print("Agent: Ask me questions about Python, AI, or Machine Learning!")
    while True:
        msg = input("\nYou: ").strip()
        if msg.lower() in ['exit', 'quit']:
            print("\nAgent: Goodbye! 👋\n")
            break
        if msg:
            response = agent.answer_question(msg)
            print(f"Agent: {response}")

def run_advanced_rag():
    """Run advanced RAG agent"""
    try:
        from advanced_rag_agent import interactive_rag
        interactive_rag()
    except Exception as e:
        print(f"\n❌ Error loading Advanced RAG: {e}")
        print("Falling back to basic RAG...\n")
        run_basic_rag()

def run_multi_agent():
    """Run multi-agent system"""
    try:
        from multi_agent_system import interactive_multi_agent
        interactive_multi_agent()
    except Exception as e:
        print(f"\n❌ Error loading Multi-Agent System: {e}\n")

def test_all_agents():
    """Quick test of all agents"""
    print("\n" + "=" * 70)
    print("🧪 Testing All Agents")
    print("=" * 70)
    
    test_query = "What is artificial intelligence?"
    
    # Test 1: Simple Agent
    print("\n1️⃣  Testing Simple Agent...")
    try:
        from simple_agent import SimpleAgent
        agent = SimpleAgent()
        response = agent.send_message(test_query)
        print(f"✓ Response: {response[:100]}...")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Guardrail Agent
    print("\n2️⃣  Testing Guardrail Agent...")
    try:
        from agent_with_guardrails import GuardrailAgent
        agent = GuardrailAgent()
        response = agent.process(test_query)
        print(f"✓ Response: {response[:100]}...")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: RAG Agent
    print("\n3️⃣  Testing RAG Agent...")
    try:
        from rag_agent import SimpleRAGAgent
        agent = SimpleRAGAgent()
        agent.add_knowledge("AI is artificial intelligence, simulating human intelligence in machines.")
        response = agent.answer_question(test_query)
        print(f"✓ Response: {response[:100]}...")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print("✅ Testing complete!")
    print("=" * 70 + "\n")
    input("Press Enter to return to main menu...")

def main():
    """Main application loop"""
    while True:
        print_header()
        print_menu()
        
        try:
            choice = input("Select an option (0-7): ").strip()
            
            if choice == '1':
                run_simple_agent()
            elif choice == '2':
                run_guardrail_agent()
            elif choice == '3':
                run_agent_builder()
            elif choice == '4':
                run_basic_rag()
            elif choice == '5':
                run_advanced_rag()
            elif choice == '6':
                run_multi_agent()
            elif choice == '7':
                test_all_agents()
            elif choice == '0':
                print("\n" + "=" * 70)
                print("👋 Thank you for using AI Agents System!")
                print("=" * 70 + "\n")
                break
            else:
                print("\n❌ Invalid choice. Please select 0-7.")
                input("Press Enter to continue...")
        
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted! Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()