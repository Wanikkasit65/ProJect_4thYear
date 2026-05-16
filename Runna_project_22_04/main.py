from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

import datetime

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI(title="Runna AI Coach")

# Mock data
MOCK_LOCATIONS = {
    "18.7883,98.9853": "ประตูท่าแพ",
    "18.7970,98.9817": "อ่างแก้ว มช.",
    "18.8036,98.9712": "ดอยสุเทพ",
    "18.7769,98.9937": "นิมมานเหมินทร์"
}

class RunData(BaseModel):
    lat: float
    lng: float
    distance: float
    pace: str
    steps: int

@app.get("/")
async def root():
    return {"message": "Runna AI Coach - FastAPI! Test POST /ai-summary"}

@app.post("/manual")
async def record_run(run: RunData):
    location = MOCK_LOCATIONS.get(f"{run.lat},{run.lng}", "เชียงใหม่")
    return {"locationName": location, "message": "Run recorded!"}

@app.post("/ai-summary")
async def ai_summary(run: RunData):
    location = MOCK_LOCATIONS.get(f"{run.lat},{run.lng}", "เชียงใหม่")
    
    # Mock history
    stats = {
        "today": {"distance": run.distance, "pace": run.pace, "steps": run.steps},
        "history30Days": {"avgPace": "6:15", "totalRuns": 12}
    }
    
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    
prompt = f'''
คุณคือ Athlete Intelligence AI ที่วิเคราะห์การวิ่งอย่างมืออาชีพ
ข้อมูลวันนี้: Distance {run.distance}km, Pace {run.pace}, Steps {run.steps}
Samsung Health: HR zone 4: 20min (vs 30d avg 18min +10%)
Mock Samsung Health connect data loaded.

สรุปผลเข้าใจง่าย: "วันนี้คุณวิ่ง Tempo ได้ดีมาก หัวใจอยู่ในโซน 4 นานขึ้น 10% เมื่อเทียบกับ 30 วันที่ผ่านมา."
ภาษาไทย 3-4ประโยค, ชมเชย+แนะนำ
'''

    
    try:
        response = model.generate_content(prompt)
        summary = response.text
    except:
        summary = f"สวัสดีเจ้า! วิ่งดีที่{location} Pace {run.pace}เร็วกว่าavg วินัย12ครั้ง ปิ๊กบ้าน!"
    
    return {"location": location, "stats": stats, "aiSummary": summary}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)

