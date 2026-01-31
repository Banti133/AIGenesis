import os
from dotenv import load_dotenv
import google.generativeai as genai
from typing import Optional

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

class GuardrailAgent:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.blocked_topics = ['violence', 'harmful', 'illegal']
        self.max_tokens = 1000
        
    def validate_input(self, user_input: str) -> tuple[bool, Optional[str]]:
        """Validate user input before processing"""
        # Length check
        if len(user_input) > 5000:
            return False, "Input too long. Please keep it under 5000 characters."
        
        # Empty check
        if not user_input.strip():
            return False, "Input cannot be empty."
        
        # Blocked topics check
        user_input_lower = user_input.lower()
        for topic in self.blocked_topics:
            if topic in user_input_lower:
                return False, f"Sorry, I cannot discuss topics related to {topic}."
        
        return True, None
    
    def validate_output(self, output: str) -> tuple[bool, Optional[str]]:
        """Validate model output before returning"""
        # Length check
        if len(output) > self.max_tokens * 4:  # Rough character estimate
            return False, "Response too long. Please refine your question."
        
        return True, None
    
    def process(self, user_input: str) -> str:
        """Process user input with guardrails"""
        # Input validation
        is_valid, error_msg = self.validate_input(user_input)
        if not is_valid:
            return f"⚠️ Guardrail Alert: {error_msg}"
        
        try:
            # Generate response
            response = self.model.generate_content(user_input)
            output = response.text
            
            # Output validation
            is_valid, error_msg = self.validate_output(output)
            if not is_valid:
                return f"⚠️ Output Guardrail: {error_msg}"
            
            return output
            
        except Exception as e:
            return f"❌ Error: {str(e)}"

# Test
if __name__ == "__main__":
    agent = GuardrailAgent()
    
    # Test cases
    test_inputs = [
        "What is Python?",
        "Tell me about violence",  # Should be blocked
        "",  # Empty input
        "Explain machine learning in simple terms"
    ]
    
    for test_input in test_inputs:
        print(f"\n--- Testing: '{test_input}' ---")
        response = agent.process(test_input)
        print(f"Response: {response}")