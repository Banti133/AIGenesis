import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')

print("=" * 70)
print("🔍 Direct API Test - Checking Available Models")
print("=" * 70)

if not api_key:
    print("\n❌ No API key found!")
    exit(1)

print(f"\n✅ API Key: {api_key[:10]}...{api_key[-5:]}")

# Try to list available models
print("\n📋 Attempting to list available models...")

try:
    # List models endpoint
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        if 'models' in data:
            print(f"\n✅ Found {len(data['models'])} available models:")
            print("\n" + "=" * 70)
            
            gemini_models = []
            for model in data['models']:
                name = model.get('name', '')
                display_name = model.get('displayName', '')
                description = model.get('description', '')[:50]
                
                # Extract just the model ID
                model_id = name.replace('models/', '')
                
                if 'gemini' in name.lower():
                    gemini_models.append(model_id)
                    print(f"\n🤖 {display_name}")
                    print(f"   ID: {model_id}")
                    print(f"   Description: {description}...")
            
            print("\n" + "=" * 70)
            print("\n💡 Models you can use:")
            for model in gemini_models:
                print(f"   - {model}")
            
            if gemini_models:
                print(f"\n⭐ RECOMMENDED: Use '{gemini_models[0]}'")
                
                # Create config file
                with open('model_config.py', 'w') as f:
                    f.write(f"# Auto-generated from API\n")
                    f.write(f"WORKING_MODEL = '{gemini_models[0]}'\n")
                    f.write(f"\n# All available models:\n")
                    for model in gemini_models:
                        f.write(f"# - {model}\n")
                
                print("✅ Created model_config.py")
        else:
            print("❌ No models found in response")
            print(f"Response: {data}")
    
    else:
        print(f"\n❌ API Error: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 403:
            print("\n🔧 This means:")
            print("   - API key might not be activated")
            print("   - Need to enable Gemini API in Google Cloud Console")
            print("\n📝 Steps to fix:")
            print("   1. Go to https://aistudio.google.com/app/apikey")
            print("   2. Create a NEW API key")
            print("   3. Make sure 'Generative Language API' is enabled")
        
        elif response.status_code == 429:
            print("\n🔧 Rate limited - wait a minute and try again")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)

# Now test a simple generation
print("\n🧪 Testing actual content generation...")

model_to_test = "gemini-2.5-flash"

try:
    import time
    time.sleep(2)  # Wait to avoid rate limit
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_to_test}:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": "Say 'Hello World'"
            }]
        }]
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        if 'candidates' in data:
            text = data['candidates'][0]['content']['parts'][0]['text']
            print(f"\n✅ SUCCESS! Model {model_to_test} works!")
            print(f"Response: {text}")
    else:
        print(f"\n❌ Error {response.status_code}: {response.text[:200]}")

except Exception as e:
    print(f"❌ Error testing generation: {e}")

print("\n" + "=" * 70)