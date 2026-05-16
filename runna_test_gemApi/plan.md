# Athlete Intelligence API Plan

## Understanding of the Task
- **Project Goal**: Build a FastAPI-based API for testing integration with free Gemini AI (Google Generative AI) and Samsung Health Connect APIs. The core feature is "Athlete Intelligence," which uses AI to analyze running/workout data and generate user-friendly summaries (in Thai or mixed language).
- **Key Requirements**:
  - Analyze running data (e.g., distance, pace, heart rate zones like Tempo run, Zone 4).
  - Generate summaries comparing to past data (e.g., "วันนี้คุณวิ่ง Tempo ได้ดีมาก หัวใจอยู่ในโซน 4 นานขึ้น 10% เมื่อเทียบกับ 30 วันที่ผ่านมา").
  - Use mock data for testing (no real Samsung Health integration initially; simulate data).
  - Dependencies: `fastapi`, `uvicorn`, `google-generativeai`.
  - Test with Flutter (likely a mobile app consuming the API).
  - Show result at the end (e.g., run the API and demo endpoint).
- **Constraints**: Free Gemini API (requires API key). Mock Samsung Health data acceptable. Project starts empty.

## What It Will Look Like at the End
```
g:/runna_test_gemApi/
├── requirements.txt          # Dependencies: fastapi, uvicorn, google-generativeai
├── main.py                   # FastAPI app with /analyze endpoint
├── prompts.py                # Pre-defined prompts for Gemini (Thai summaries)
├── mock_data.py              # Sample running data (JSON-like: runs with date, distance, pace, HR zones)
├── .env                      # GEMINI_API_KEY (user to add)
├── README.md                 # Setup/run instructions
├── tests/                    # Optional pytest for unit tests
│   └── test_analyze.py
└── plan.md                   # This file
```
- **API Endpoints**:
  - `POST /analyze`: Input running data JSON → Gemini analysis → Summary text response.
- **Flutter Test**: Simple Flutter app to call API (or use curl/Postman for demo).
- **Final Demo**: Run `uvicorn main:app --reload`, hit endpoint with mock data, get AI summary.

## How It Will Work
1. **Setup**:
   - Create virtual env, install deps.
   - User adds `GEMINI_API_KEY` to `.env`.

2. **Data Flow**:
   - Client (Flutter) sends POST to `/analyze` with JSON: `{ "user_id": "123", "recent_runs": [...] }` (mock Samsung Health data: list of runs with fields like `date`, `distance_km`, `pace_min_per_km`, `hr_zone_time: {zone4: 20min}`, etc.).
   - FastAPI loads Gemini client with API key.
   - Construct prompt: "Analyze this running data: [data]. Summarize in Thai, highlight improvements vs 30-day avg."
   - Call `genai.generate_content(prompt)` → Get AI summary.
   - Return JSON: `{ "summary": "วันนี้คุณวิ่ง Tempo ได้ดีมาก...", "analysis": {...} }`.

3. **Mock Data Example**:
   ```json
   {
     "recent_runs": [
       {"date": "2024-10-01", "type": "Tempo", "distance_km": 10, "hr_zone4_min": 30},
       {"date": "2024-09-30", "type": "Easy", "distance_km": 8, "hr_zone4_min": 10}
     ],
     "avg_30day": {"hr_zone4_min": 25}
   }
   ```

4. **Prompt Example**:
   ```
   สรุปผลการวิ่งของผู้ใช้จากข้อมูลนี้: [JSON data]. ใช้ภาษาไทยที่เข้าใจง่าย เน้นจุดเด่น เช่น หัวใจโซน 4 นานขึ้นเท่าไหร่เมื่อเทียบ 30 วัน.
   ```

## How to Test
1. **Backend**:
   - `pip install -r requirements.txt`
   - `uvicorn main:app --reload`
   - Curl test:
     ```bash
     curl -X POST http://127.0.0.1:8000/analyze \
     -H "Content-Type: application/json" \
     -d '{"recent_runs": [...]}'
     ```
   - Expected: AI-generated summary in response.

2. **Flutter** (separate folder, quick create):
   - Simple app with button to POST data → Display summary.
   - Run `flutter run`.

3. **End Result Demo**:
   - Run API, execute curl → Show console output with summary.
   - Confirm Gemini integration works with mock data.

## Next Steps After Approval
1. Create requirements.txt, main.py, etc.
2. Setup virtual env and install deps.
3. Test API locally.
4. Create Flutter test app if needed.
5. attempt_completion with run command.

Approve this plan or suggest changes?

