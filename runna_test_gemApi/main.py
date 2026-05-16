import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')


print('1. Test without API: Mock response')
mock_response = """
วันนี้คุณวิ่ง Tempo ได้ดีมาก! หัวใจ zone4 นานขึ้น 39% จากค่าเฉลี่ย 30 วัน 
เก่งมาก ครั้งหน้าลอง interval เพิ่มดูนะ 🔥
"""
print('Mock Gemini Response:')
print(mock_response)

if api_key:
    print('\\n2. Test with API...')
    genai.configure(api_key="YOUR_API_KEY")
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = 'วิเคราะห์ข้อมูลการวิ่งนี้เป็นไทย สนุก กระตุ้นใจ: Tempo 10.5km @4:45, HR zone4 25min. Easy 8km @5:20. Avg 30day 9.5km @4:60 zone4 18min.'
    try:
        response = model.generate_content(prompt)
        print('Real Gemini Response:')
        print(response.text)
    except Exception as e:
        print(f'API Error: {e}')
else:
    print('\\nNo API key - set GEMINI_API_KEY in .env for real response.')

