# Runna Project TODO - Breakdown from Approved Plan

## Phase 1: Project Setup ✅\n- [x] Create package.json with dependencies\n- [x] Create .env.example\n- [x] Create db.js (SQLite setup, tables: users, runs, pins)\n- [x] Create app.js (Express server)\n- [x] Run `npm install`\n- [ ] Test: Server starts on port 3000

## Phase 2: Services ✅\n- [x] Create services/geocode.js (mock Chiang Mai locations)\n- [x] Create services/ai.js (Gemini integration)

## Phase 3: Routes - Feature 4 First (AI Summary) ✅\n- [x] Create routes/runs.js\n  - POST /manual (record run, mock geocode)\n  - POST /ai-summary (full workflow, test with mocks)\n  - GET /records\n- [x] Create test-mock.js (standalone AI test)

## Phase 4: Other Features
- [ ] Add POST /pins in routes/runs.js (collaborative pins)

## Phase 5: Testing & Demo
- [ ] Set GEMINI_API_KEY
- [ ] Run `node test-mock.js`
- [ ] `npm start`, test API with curl/Postman
- [ ] All done ✅

Updated after each step.

