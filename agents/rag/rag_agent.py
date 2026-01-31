import os
from dotenv import load_dotenv
import google.generativeai as genai
from typing import List

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

class SimpleRAGAgent:
    """Simple Retrieval-Augmented Generation Agent"""
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.knowledge_base: List[str] = []
    
    def add_knowledge(self, text: str):
        """Add document to knowledge base"""
        self.knowledge_base.append(text)
    
    def retrieve_relevant_context(self, query: str, top_k: int = 3) -> str:
        """Simple keyword-based retrieval"""
        if not self.knowledge_base:
            return "No knowledge base available."
        
        # Simple scoring based on keyword overlap
        query_words = set(query.lower().split())
        scored_docs = []
        
        for doc in self.knowledge_base:
            doc_words = set(doc.lower().split())
            score = len(query_words & doc_words)
            scored_docs.append((score, doc))
        
        # Sort by score and get top_k
        scored_docs.sort(reverse=True, key=lambda x: x[0])
        relevant_docs = [doc for score, doc in scored_docs[:top_k] if score > 0]
        
        return "\n\n".join(relevant_docs) if relevant_docs else "No relevant information found."
    
    def answer_question(self, question: str) -> str:
        """Answer question using RAG"""
        # Retrieve relevant context
        context = self.retrieve_relevant_context(question)
        
        # Build prompt
        prompt = f"""Based on the following context, answer the question.

Context:
{context}

Question: {question}

Answer:"""
        
        # Generate response
        response = self.model.generate_content(prompt)
        return response.text

# Test
if __name__ == "__main__":
    agent = SimpleRAGAgent()
    
    # Add knowledge
    agent.add_knowledge("""
    Python is a high-level programming language known for its simplicity and readability.
    It was created by Guido van Rossum and first released in 1991.
    """)
    
    agent.add_knowledge("""
    AI agents are autonomous software programs that can perceive their environment,
    make decisions, and take actions to achieve specific goals.
    """)
    
    agent.add_knowledge("""
    Machine learning is a subset of AI that enables systems to learn from data
    and improve their performance without being explicitly programmed.
    """)
    
    # Test questions
    questions = [
        "Who created Python?",
        "What are AI agents?",
        "Tell me about machine learning"
    ]
    
    for q in questions:
        print(f"\nQuestion: {q}")
        print(f"Answer: {agent.answer_question(q)}")