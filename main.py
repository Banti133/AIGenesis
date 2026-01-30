import os
from dotenv import load_dotenv
from simple_agent import SimpleAgent
from agent_with_guardrails import GuardrailAgent
from agent_builder import AgentBuilder, Tool, get_current_time
from rag_agent import SimpleRAGAgent

load_dotenv()

def main():
    print("=== AI Agents Demo ===\n")
    print("Choose an agent:")
    print("1. Simple Agent")
    print("2. Guardrail Agent")
    print("3. Custom Agent with Tools")
    print("4. RAG Agent")
    print("5. Exit")
    
    choice = input("\nEnter your choice (1-5): ")
    
    if choice == "1":
        agent = SimpleAgent()
        print("\n--- Simple Agent ---")
        while True:
            msg = input("You: ")
            if msg.lower() in ['exit', 'quit']:
                break
            print(f"Agent: {agent.send_message(msg)}")
    
    elif choice == "2":
        agent = GuardrailAgent()
        print("\n--- Guardrail Agent ---")
        while True:
            msg = input("You: ")
            if msg.lower() in ['exit', 'quit']:
                break
            print(f"Agent: {agent.process(msg)}")
    
    elif choice == "3":
        agent = AgentBuilder(
            role="Helpful Assistant",
            instructions="Be helpful and friendly"
        )
        agent.add_tool(Tool("get_time", "Get current time", get_current_time))
        
        print("\n--- Custom Agent ---")
        while True:
            msg = input("You: ")
            if msg.lower() in ['exit', 'quit']:
                break
            print(f"Agent: {agent.chat(msg)}")
    
    elif choice == "4":
        agent = SimpleRAGAgent()
        agent.add_knowledge("AI is artificial intelligence.")
        agent.add_knowledge("Python is a programming language.")
        
        print("\n--- RAG Agent ---")
        while True:
            msg = input("You: ")
            if msg.lower() in ['exit', 'quit']:
                break
            print(f"Agent: {agent.answer_question(msg)}")
    
    else:
        print("Goodbye!")

if __name__ == "__main__":
    main()