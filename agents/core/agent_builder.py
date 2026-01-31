import os
from dotenv import load_dotenv
import google.generativeai as genai
from typing import List, Dict, Callable
from datetime import datetime

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

class Tool:
    """Represents a tool that an agent can use"""
    def __init__(self, name: str, description: str, function: Callable):
        self.name = name
        self.description = description
        self.function = function
    
    def execute(self, *args, **kwargs):
        return self.function(*args, **kwargs)

class AgentBuilder:
    """Build custom AI agents with tools and specific roles"""
    
    def __init__(self, role: str, instructions: str):
        self.role = role
        self.instructions = instructions
        self.tools: List[Tool] = []
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.conversation_history = []
        
    def add_tool(self, tool: Tool):
        """Add a tool to the agent"""
        self.tools.append(tool)
        return self
    
    def get_system_prompt(self) -> str:
        """Generate system prompt with role and available tools"""
        tools_description = "\n".join([
            f"- {tool.name}: {tool.description}" 
            for tool in self.tools
        ])
        
        return f"""You are a {self.role}.

Instructions: {self.instructions}

Available tools:
{tools_description}

When you need to use a tool, respond with: USE_TOOL: tool_name(arguments)
"""
    
    def process_message(self, user_message: str) -> str:
        """Process a message and handle tool usage"""
        # Build full prompt
        full_prompt = f"{self.get_system_prompt()}\n\nUser: {user_message}"
        
        # Get response
        response = self.model.generate_content(full_prompt)
        response_text = response.text
        
        # Check if agent wants to use a tool
        if "USE_TOOL:" in response_text:
            tool_call = response_text.split("USE_TOOL:")[1].strip()
            tool_name = tool_call.split("(")[0].strip()
            
            # Find and execute tool
            for tool in self.tools:
                if tool.name == tool_name:
                    try:
                        result = tool.execute()
                        return f"Tool Result: {result}\n\nAgent: Based on this, {response_text.split('USE_TOOL:')[0]}"
                    except Exception as e:
                        return f"Error executing tool: {str(e)}"
        
        return response_text
    
    def chat(self, message: str) -> str:
        """Have a conversation with the agent"""
        self.conversation_history.append({"role": "user", "content": message})
        response = self.process_message(message)
        self.conversation_history.append({"role": "assistant", "content": response})
        return response

# Example tools
def get_current_time():
    """Get the current time"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def calculate(expression: str):
    """Safely calculate a mathematical expression"""
    try:
        # Only allow safe operations
        allowed_chars = set("0123456789+-*/(). ")
        if all(c in allowed_chars for c in expression):
            return eval(expression)
        return "Invalid expression"
    except:
        return "Calculation error"

# Test the Agent Builder
if __name__ == "__main__":
    # Create a research assistant agent
    agent = AgentBuilder(
        role="Research Assistant",
        instructions="Help users with research tasks, provide accurate information, and use tools when necessary."
    )
    
    # Add tools
    agent.add_tool(Tool(
        name="get_time",
        description="Get the current date and time",
        function=get_current_time
    ))
    
    agent.add_tool(Tool(
        name="calculate",
        description="Perform mathematical calculations",
        function=lambda: calculate("2 + 2")
    ))
    
    # Test conversation
    print("=== Research Assistant Agent ===\n")
    
    questions = [
        "What time is it?",
        "Explain what AI agents are",
        "Calculate 25 * 4"
    ]
    
    for question in questions:
        print(f"User: {question}")
        response = agent.chat(question)
        print(f"Agent: {response}\n")