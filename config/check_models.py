import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

try:
    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
    
    print("=" * 60)
    print("🔍 Checking Available Gemini Models")
    print("=" * 60)
    
    # Try common model names
    test_models = [
        'gemini-2.5-flash',
        'gemini-2.5-pro',
        'gemini-2.0-flash-exp',
        'gemini-2.5-pro',
        'gemini-flash',
    ]
    
    print("\n✅ Testing models...\n")
    
    working_models = []
    
    for model_name in test_models:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents="Say 'OK'"
            )
            print(f"✅ {model_name} - WORKS")
            working_models.append(model_name)
        except Exception as e:
            print(f"❌ {model_name} - Error: {str(e)[:80]}...")
    
    print("\n" + "=" * 60)
    if working_models:
        print(f"\n✅ Working Models Found: {len(working_models)}")
        print(f"Recommended: {working_models[0]}")
    else:
        print("\n❌ No working models found. Please check your API key.")
    print("\n" + "=" * 60)
    
except Exception as e:
    print(f"\n❌ Error initializing client: {e}")
    print("\nMake sure you have:")
    print("1. Installed google-genai: pip install google-genai")
    print("2. Valid API key in .env file")