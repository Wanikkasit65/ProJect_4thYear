import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print("No GEMINI_API_KEY found in .env")
    exit(1)

genai.configure(api_key=api_key)

# เลือก model (แนะนำตัวนี้)
model = genai.GenerativeModel("gemini-2.5-flash")

# ตัวอย่างข้อมูลการวิ่ง
pace = 6.2          # นาทีต่อกิโลเมตร
distance = 5        # กิโลเมตร
duration = 31       # นาที
steps = 6200        # จำนวนก้าว

# prompt สำหรับ AI
prompt = f"""
You are a professional running coach.

Analyze the following running session:

Distance: {distance} km
Duration: {duration} minutes
Average Pace: {pace} min/km
Steps: {steps}

Provide:
1. Performance summary
2. Strengths
3. Weaknesses
4. Suggestions for improvement

Keep it concise and easy to understand.
"""

# เรียกใช้ API
response = model.generate_content(prompt)

# แสดงผลลัพธ์
print("=== AI ANALYSIS ===")
print(response.text)
