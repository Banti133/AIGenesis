import os
from dotenv import load_dotenv

load_dotenv()

print("🔍 Gemini Model Finder - 2026 Edition")
print("=" * 70)

# ✅ PRIORITIZED 2026 model list (from your directapitest.py success)
model_names = [
    # ⭐ TOP PRIORITY - Your confirmed working models
    'gemini-2.5-flash',           # ✅ Stable, recommended
    'gemini-2.5-pro',             # ✅ Stable reasoning
    'gemini-2.0-flash',           # ✅ Fast
    'gemini-2.0-flash-001',       # ✅ Stable version
    
    # Embedding models (for RAG)
    'text-embedding-004',         # ✅ Your RAG needs this
    
    # Latest variants
    'gemini-flash-latest',
    'gemini-pro-latest',
    'gemini-2.5-flash-latest',
    
    # Experimental (if available)
    'gemini-2.5-flash-preview-tts',
    'gemini-exp-1206',
    'gemini-3-flash-preview',
]

# Test with NEW SDK only (old one deprecated)
try:
    from google import genai
    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
    print("✅ Using: google-genai (2026 SDK)")
    USE_NEW_API = True
except ImportError:
    print("❌ Install: pip install google-genai")
    exit(1)

working_models = []
generation_models = []
embedding_models = []

print("\n🧪 Testing generation models...\n")

for model_name in model_names:
    try:
        # Test generation capability
        response = client.models.generate_content(
            model=model_name,
            contents=["Test: Reply with 'OK'"]
        )
        
        print(f"✅ {model_name:30} - WORKS! ({response.text[:20]}...)")
        working_models.append(model_name)
        generation_models.append(model_name)
        
    except Exception as e:
        error_msg = str(e).lower()
        if '404' in error_msg or 'not found' in error_msg:
            print(f"❌ {model_name:30} - Model not available")
        elif '429' in error_msg or 'quota' in error_msg:
            print(f"⚠️  {model_name:30} - Rate limited")
        elif '403' in error_msg:
            print(f"⚠️  {model_name:30} - Permission denied")
        else:
            print(f"❌ {model_name:30} - {str(e)[:40]}")

# Test embeddings separately
print(f"\n🧮 Testing embedding models...")
try:
    emb_response = client.models.embed_content(
        model='text-embedding-004',
        contents=["test"]
    )
    print("✅ text-embedding-004 - Embeddings WORK!")
    embedding_models.append('text-embedding-004')
except:
    print("❌ text-embedding-004 - Embeddings unavailable")

print("\n" + "=" * 70)
print("🎯 RECOMMENDATIONS")
print("=" * 70)

if working_models:
    print(f"\n✅ {len(working_models)} working models found!")
    print(f"\n📝 Copy this to your agents:")
    print(f"   MODEL_NAME = '{working_models[0]}'")
    print(f"   EMBEDDING_MODEL = 'text-embedding-004'")
    
    print(f"\n⭐ BEST CHOICES:")
    print(f"   Chat agents: {working_models[0]}")
    print(f"   RAG embeddings: text-embedding-004")
    
    # Auto-generate config
    config = f"""# Auto-generated config - {len(working_models)} models found
MODEL_NAME = '{working_models[0]}'
EMBEDDING_MODEL = 'text-embedding-004'
WORKING_MODELS = {working_models[:3]}
"""
    
    with open('model_config.py', 'w') as f:
        f.write(config)
    print(f"\n💾 Saved: model_config.py")

else:
    print("\n❌ No models working!")
    print("\n🔧 QUICK FIXES:")
    print("   1. pip install --upgrade google-genai")
    print("   2. Check .env: GEMINI_API_KEY=...")
    print("   3. https://aistudio.google.com/app/apikey")

api_key = os.getenv('GEMINI_API_KEY')
print(f"\n🔑 API Key: {'✅ Found' if api_key else '❌ Missing'} ({len(api_key or '')} chars)")
print("=" * 70)
