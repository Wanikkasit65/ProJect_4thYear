# Runna AI Coach - Testing Guide

## 1. Test Mock AI (No API Key needed)
```
node test-mock.js
```
Output example:
```
=== Test AI Summary ===
Location: ประตูท่าแพ
Stats: { today: { distance: 5, pace: '5:45', steps: 5200 }, history30Days: { avgPace: '6:15', totalRuns: 12 } }

AI Coach: Mock summary (set GEMINI_API_KEY): สวัสดีเจ้า! วิ่งดีมากที่ประตูท่าแพ Pace เร็วกว่าค่าเฉลี่ย ปิ๊กบ้านไปพักเถิด!

Test complete! Set GEMINI_API_KEY for real AI.
```

## 2. Get Gemini API Key (Optional for real AI)
- Go to https://aistudio.google.com/app/apikey
- Create free API key for gemini-1.5-flash
- Copy key

## 3. Setup .env (Optional)
Copy `.env.example` to `.env` and add key:
```
cp .env.example .env
```
Edit `.env`:
```
GEMINI_API_KEY=AIza...your_key_here
PORT=3000
DB_PATH=./runna.db
```

**No code change needed** – reads from .env automatically.

## 4. Run Server
```
node app.js
```
See: `Server running on port 3000`

## 5. Test API with curl (Feature 4: AI Summary)
New terminal:
```
curl -X POST http://localhost:3000/api/runs/ai-summary \
  -H "Content-Type: application/json" \
  -d "{\"lat\":18.7883,\"lng\":98.9853,\"distance\":5.0,\"pace\":\"5:45\",\"steps\":5200}"
```
Response:
```json
{
  "locationName": "ประตูท่าแพ",
  "stats": {...},
  "aiSummary": "สวัสดีเจ้า! วันนี้มาวิ่งตื่อแถว ประตูท่าแพ ... (AI response)"
}
```

## Other Tests
- Record run: Same curl to `/api/runs/manual`
- List records: `curl http://localhost:3000/api/runs/records`
- Add pin: `curl -X POST http://localhost:3000/api/runs/pins -H "Content-Type: application/json" -d "{\"lat\":18.797,\"lng\":98.9817,\"name\":\"อ่างแก้ว\"}"`

## Verify DB
`runna.db` created with mock data.

All ready!

