import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("No GEMINI_API_KEY in .env")
    exit(1)

genai.configure(api_key=api_key)

print("Available models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)

model = genai.GenerativeModel('gemini-1.5-flash-latest')
response = model.generate_content("Hello")
print("\nResponse:", response.text)
