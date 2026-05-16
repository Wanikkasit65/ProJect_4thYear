import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("No GEMINI_API_KEY in .env")
    exit(1)

genai.configure(api_key=api_key)

# List models
print("Available models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)

# Use working model
model = genai.GenerativeModel('models/gemini-2.5-flash')
response = model.generate_content("Hello")
print("\nResponse:", response.text)
