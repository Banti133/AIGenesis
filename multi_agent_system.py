import os
from dotenv import load_dotenv
from google import genai  # ✅ NEW SDK (2026 standard)
from typing import Dict, List
import json

load_dotenv()

class SpecializedAgent:
    """A specialized agent with a specific role - 2026 Updated"""
    
    def __init__(self, name: str, role: str, expertise: str):
        self.name = name
        self.role = role
        self.expertise = expertise
        
        system_instruction = f"""You are {name}, a {role}.
Your expertise: {expertise}

Always respond according to your role and expertise.
Be helpful, accurate, and professional."""
        
        # ✅ NEW SDK: client.models.generate_content()
        self.client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
        self.model_name = 'gemini-2.5-flash'  # Your confirmed working model
        self.system_instruction = system_instruction
    
    def respond(self, query: str) -> str:
        """Generate a response to a query - Updated API"""
        try:
            # ✅ CORRECT 2026 API pattern
            full_prompt = f"{self.system_instruction}\n\nUser Query: {query}\n\nResponse:"
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[full_prompt]
            )
            return response.text.strip()
            
        except Exception as e:
            return f"Error: {str(e)}"

class MultiAgentSystem:
    """System that manages multiple specialized agents - 2026 Updated"""
    
    def __init__(self):
        self.agents: Dict[str, SpecializedAgent] = {}
        # ✅ NEW SDK router
        self.client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
        self.router_model = 'gemini-2.5-flash'
    
    def add_agent(self, agent: SpecializedAgent):
        """Add a specialized agent to the system"""
        self.agents[agent.name] = agent
        print(f"✓ Added agent: {agent.name} ({agent.role})")
    
    def route_query(self, query: str) -> str:
        """AI-powered query routing - Updated API"""
        if not self.agents:
            return "No agents available"
        
        # Create agent descriptions
        agent_descriptions = "\n".join([
            f"- {name}: {agent.role} - {agent.expertise}"
            for name, agent in self.agents.items()
        ])
        
        routing_prompt = f"""Given this query and available agents, select EXACTLY ONE agent name.

Query: {query}

Available agents:
{agent_descriptions}

Respond with ONLY the agent NAME (e.g. "CodeMaster", "DataWizard"). No explanations."""

        try:
            response = self.client.models.generate_content(
                model=self.router_model,
                contents=[routing_prompt]
            )
            
            selected_agent_name = response.text.strip()
            
            # Exact match first, then fuzzy
            for agent_name in self.agents.keys():
                if agent_name.lower() == selected_agent_name.lower():
                    return agent_name
            
            # Fuzzy match fallback
            for agent_name in self.agents.keys():
                if agent_name.lower() in selected_agent_name.lower():
                    return agent_name
            
            # Default fallback
            return list(self.agents.keys())[0]
            
        except Exception as e:
            print(f"Routing error: {e}")
            return list(self.agents.keys())[0]
    
    def process_query(self, query: str) -> Dict:
        """Process query through intelligent routing"""
        agent_name = self.route_query(query)
        agent = self.agents[agent_name]
        response = agent.respond(query)
        
        return {
            "query": query,
            "agent": agent_name,
            "role": agent.role,
            "expertise": agent.expertise,
            "response": response
        }
    
    def list_agents(self):
        """Display all available agents"""
        print("\n📋 Available Agents (2026 Multi-Agent System):")
        print("=" * 70)
        for name, agent in self.agents.items():
            print(f"\n🤖 {name}")
            print(f"   🎭 Role: {agent.role}")
            print(f"   🧠 Expertise: {agent.expertise}")
        print("\n" + "=" * 70)

# Same great default agents
def create_default_agents() -> List[SpecializedAgent]:
    return [
        SpecializedAgent(
            name="CodeMaster",
            role="Senior Software Engineer",
            expertise="Python, JavaScript, C#, .NET, algorithms, debugging, best practices, code review, system design"
        ),
        SpecializedAgent(
            name="DataWizard", 
            role="Data Scientist",
            expertise="Machine learning, statistics, data analysis, pandas, PyTorch, scikit-learn, visualization, RAG systems"
        ),
        SpecializedAgent(
            name="SecurityGuard",
            role="Cybersecurity Expert",
            expertise="Security best practices, OWASP Top 10, encryption, JWT auth, secure coding, penetration testing"
        ),
        SpecializedAgent(
            name="WriterPro",
            role="Technical Writer",
            expertise="API documentation, technical writing, READMEs, tutorials, developer guides, clear communication"
        ),
        SpecializedAgent(
            name="DesignGuru",
            role="UX/UI & System Architect", 
            expertise="User experience, microservices, system design, scalability, cloud architecture, design patterns"
        )
    ]

def interactive_multi_agent():
    """🚀 Main interactive interface"""
    print("=" * 70)
    print("🌟 Multi-Agent AI System - 2026 Edition")
    print("✅ Using gemini-2.5-flash (your confirmed working model)")
    print("=" * 70)
    
    system = MultiAgentSystem()
    
    print("\n🔄 Initializing specialized agents...")
    for agent in create_default_agents():
        system.add_agent(agent)
    
    print("\n🎮 Commands:")
    print("   'agents' - List agents")
    print("   'exit' - Quit")
    print("\n" + "=" * 70 + "\n")
    
    while True:
        try:
            query = input("💬 Your Query: ").strip()
            
            if not query:
                continue
                
            if query.lower() in ['exit', 'quit']:
                print("\n👋 Thanks for using Multi-Agent System!")
                break
                
            if query.lower() == 'agents':
                system.list_agents()
                continue
            
            print("\n🔍 AI Routing your query...")
            result = system.process_query(query)
            
            print(f"\n🎯 Routed to: {result['agent']} ({result['role']})")
            print(f"\n💡 Response:\n{result['response']}\n")
            print("-" * 70 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")

if __name__ == "__main__":
    interactive_multi_agent()
