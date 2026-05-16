# Athlete Intelligence API

## Setup
1. Copy `.env.example` to `.env` and add your free Gemini API key:
   ```
   GEMINI_API_KEY=your_key_here
   ```
   Get key: [Google AI Studio](https://aistudio.google.com/app/apikey)

2. Create & activate virtual env:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install deps:
   ```
   pip install -r requirements.txt
   ```

## Run
```
uvicorn main:app --reload
```
- Visit http://127.0.0.1:8000/docs for Swagger UI.
- Test `/analyze` with mock or real data.

## Test with Curl (uses mock data)
```
curl -X POST http://127.0.0.1:8000/analyze -H "Content-Type: application/json" -d "{\"user_id\": \"test123\"}"
```

## Flutter Test
Create simple Flutter app to POST data and show summary (optional, can use Postman/cURL).

## Errors
- Missing API key: Set in .env.
- Gemini quota: Use free tier limits.

