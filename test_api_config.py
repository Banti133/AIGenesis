import os
import time
from dotenv import load_dotenv

load_dotenv()

print("=" * 70)
print("🔧 Gemini API Configuration Tester")
print("=" * 70)

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("❌ No API key found in .env file!")
    exit(1)

print(f"\n✅ API Key: {api_key[:10]}...{api_key[-5:]}")

# Test with the new google-genai package using correct configuration
print("\n📦 Testing with google-genai package...")

try:
    from google import genai
    from google.genai import types
    
    # Create client
    client = genai.Client(api_key=api_key)
    
    print("✅ Client created successfully")
    
    # Models to try with waiting
    test_models = [
        'gemini-2.0-flash',
        'gemini-2.5-flash',
        'gemini-2.5-pro',
    ]
    
    working_model = None
    
    for model_name in test_models:
        print(f"\n🧪 Testing: {model_name}")
        print("   Waiting 3 seconds to avoid rate limit...")
        time.sleep(3)
        
        try:
            # Try to generate content
            response = client.models.generate_content(
                model=model_name,
                contents="Say 'Hello'"
            )
            
            print(f"   ✅ SUCCESS! Response: {response.text}")
            working_model = model_name
            break
            
        except Exception as e:
            error_str = str(e)
            if '429' in error_str:
                print(f"   ⚠️  Rate limited - waiting 10 seconds...")
                time.sleep(10)
                # Try once more
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents="Say 'Hello'"
                    )
                    print(f"   ✅ SUCCESS on retry! Response: {response.text}")
                    working_model = model_name
                    break
                except Exception as e2:
                    print(f"   ❌ Still failed: {str(e2)[:100]}")
            else:
                print(f"   ❌ Error: {error_str[:100]}")
    
    print("\n" + "=" * 70)
    
    if working_model:
        print(f"\n🎉 SUCCESS! Working model found: {working_model}")
        print(f"\n💡 Use this in your code:")
        print(f"   MODEL_NAME = '{working_model}'")
        
        # Create a config file
        with open('model_config.py', 'w') as f:
            f.write(f"# Auto-generated working model configuration\n")
            f.write(f"WORKING_MODEL = '{working_model}'\n")
        print("\n✅ Created model_config.py with working model name")
        
    else:
        print("\n❌ No working model found")
        print("\n🔍 Possible issues:")
        print("   1. API key might not have access to these models")
        print("   2. Account might not be activated properly")
        print("   3. Region restrictions")
        print("\n📝 Next steps:")
        print("   1. Go to https://aistudio.google.com/")
        print("   2. Click 'Get API Key'")
        print("   3. Make sure you see a list of available models")
        print("   4. Try generating content in the web UI first")
        print("   5. Generate a NEW API key")
        
except ImportError:
    print("\n❌ google-genai package not installed!")
    print("\nRun: pip install google-genai")
except Exception as e:
    print(f"\n❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)