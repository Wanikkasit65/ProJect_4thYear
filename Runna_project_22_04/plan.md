# Runna Project Plan - AI Running Coach App (Focus: 4 Key Features with Mock Data)

## Information Gathered
- **Project State**: Empty directory (only irrelevant PNG). Starting from scratch with Node.js/Express backend.
- **Tech Stack Decision**: 
  - Backend: Node.js + Express.js (API routes).
  - DB: SQLite (via better-sqlite3) for simplicity, or JSON file mocks initially. Later migrate to real DB.
  - Geocoding: Mock with static Chiang Mai locations (no real Google Maps API needed for testing).
  - AI: @google/generative-ai (Gemini 1.5 Flash) – user must provide API key.
  - Other: Axios if needed, but keep minimal. Focus on feature 4 (AI summary).
- **Features Scope** (Test only #4, mock data):
  1. **Manual Route Gen**: POST /runs/manual - Record GPS (lat/lng), stats (pace, distance, steps).
  2. **Records CRUD**: GET/POST/PUT/DELETE /runs.
  3. **Collaborative Pin**: POST /pins - Share locations/pins.
  4. **AI Summary** (Main): POST /runs/ai-summary - Geocode -> Fetch user/historical data -> Gemini prompt -> Return summary.
- **Local Context**: Chiang Mai-focused (Northern Thai dialect in prompts), mock user: age 21, เชียงใหม่.
- **Assumptions**: Single-user app initially. Mock GPS stops at predefined Chiang Mai spots (e.g., ประตูท่าแพ). Historical pace from mock DB (30 days avg).

## Plan
### Phase 1: Project Setup (Files to Create)
1. **package.json**: Dependencies: express, better-sqlite3, @google/generative-ai, cors, dotenv.
2. **.env**: GEMINI_API_KEY placeholder.
3. **db.js**: SQLite setup, tables: users (age, province), runs (user_id, lat, lng, location_name, distance, pace, steps, date), pins.
4. **routes/runs.js**: 
   - POST /manual: Record run, mock geocode (e.g., lat 18.7883/lng 98.9853 -> \"ประตูท่าแพ\").
   - GET /records: List user runs.
   - POST /ai-summary: Workflow - get stats + user profile + 30d avg pace -> Gemini prompt -> store summary.
5. **services/geocode.js**: Mock function mapping coords to Chiang Mai places.
6. **services/ai.js**: Gemini integration with localized prompt (Northern Thai coach).
7. **app.js**: Express server, routes mount, CORS.
8. **test-mock.js**: Standalone script to test AI summary with hardcoded mocks.

### Phase 2: Implement Feature 4 First (AI Summary)
- Mock run end: {lat:18.7883, lng:98.9853, distance:5.0, pace:\"5:45\", steps:5200}
- Geocode -> \"ประตูท่าแพ\"
- User: {age:21, province:\"เชียงใหม่\"}
- History: avg_pace:\"6:15\", total_runs_30d:12
- Prompt: As specified (Northern Thai coach).
- Response: Display in console/JSON, save to DB.

### Phase 3: Other Features (Quick CRUD)
- Manual record -> DB insert.
- Records list.
- Pins: Simple shared locations.

### Dependent Files to Edit/Create
- All new: package.json, .env.example, app.js, db.js, routes/*.js, services/*.js, test-mock.js.
- No edits to existing (none).

## Followup Steps (After Creates)
1. **Install**: `npm install`
2. **API Key**: Set GEMINI_API_KEY in .env
3. **Test Feature 4**: `node test-mock.js` (see sample output).
4. **Run Server**: `npm start` (listen 3000), test with curl/Postman.
5. **Full Test**: curl POST /runs/ai-summary with mock payload.
6. **Frontend?**: Later React/Vue if needed, but backend API first.
7. **Deploy**: Heroku/Vercel.

## Confirmation
Approve this plan? Any changes (e.g., DB choice, add frontend, real geocode)? Provide GEMINI_API_KEY if ready to test AI.

Proceed step-by-step after approval: Create TODO.md, then files one-by-one.

