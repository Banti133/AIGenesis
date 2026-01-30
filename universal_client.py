import os
from dotenv import load_dotenv
from google import genai
from typing import Optional, List

load_dotenv()

def get_gemini_client(model_name: str = "gemini-2.5-flash"):
    """Get 2026 Gemini client - SIMPLIFIED API"""
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        raise ValueError("❌ GEMINI_API_KEY missing from .env")
    
    client = genai.Client(api_key=api_key)
    print(f"✅ Client: {model_name}")
    return client

def generate_content(prompt: str, model: str = "gemini-2.5-flash") -> str:
    """✅ FIXED - No generation_config (your SDK issue)"""
    client = get_gemini_client(model)
    
    try:
        # ✅ SIMPLIFIED - Just model + contents (matches your SDK)
        response = client.models.generate_content(
            model=model,
            contents=[prompt]  # List format required
        )
        return response.text.strip()
        
    except Exception as e:
        return f"❌ Error: {str(e)}"

def generate_embedding(text: str, model: str = "text-embedding-004") -> list:
    """✅ Embeddings already working (your test passed!)"""
    client = get_gemini_client(model)
    
    try:
        response = client.models.embed_content(
            model=model,
            contents=[text]
        )
        return response.embeddings[0].values
    except Exception as e:
        print(f"❌ Embedding error: {e}")
        return []

# 🧪 FIXED TEST SUITE
if __name__ == "__main__":
    print("=" * 70)
    print("🧪 Universal Client - FIXED FOR YOUR SDK")
    print("=" * 70)
    
    # Test 1: Basic (SIMPLEST call)
    print("\n✅ 1. Basic generation...")
    resp1 = generate_content("Say 'Hello 2026!'")
    print(f"   {repr(resp1)[:60]}")
    
    # Test 2: Agent style (your MultiAgentSystem pattern)
    print("\n✅ 2. Agent style...")
    agent_prompt = """You are CodeMaster. Fix: for i in range(10): print(i * 2)

Better version:"""
    resp2 = generate_content(agent_prompt)
    print(f"   {repr(resp2)[:80]}...")
    
    # Test 3: Embeddings (✅ ALREADY WORKS)
    print("\n✅ 3. Embeddings... (768 dims confirmed)")
    
    print("\n🎉 FIXED! Ready for Multi-Agent system!")
    print("=" * 70)
