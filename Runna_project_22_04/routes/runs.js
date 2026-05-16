const express = require('express');
const db = require('../db');
const { geocode } = require('../services/geocode');
const { generateSummary } = require('../services/ai');

const router = express.Router();

// 1. Manual route gen / record
router.post('/manual', (req, res) => {
  const { lat, lng, distance, pace, steps } = req.body;
  const locationName = geocode(lat, lng);
  
  const stmt = db.prepare('INSERT INTO runs (user_id, lat, lng, location_name, distance, pace, steps, date) VALUES (1, ?, ?, ?, ?, ?, ?, datetime("now"))');
  const info = stmt.run(lat, lng, locationName, distance, pace, steps);
  
  res.json({ id: info.lastInsertRowid, locationName, message: 'Run recorded!' });
});

// 4. AI Summary (main feature)
router.post('/ai-summary', async (req, res) => {
  try {
    const { lat, lng, distance, pace, steps } = req.body;
    const locationName = geocode(lat, lng);
    
    // User profile
    const user = db.prepare('SELECT * FROM users WHERE id = 1').get();
    
    // 30d history avg (mock query)
    const history = db.prepare(`
      SELECT AVG(CASE 
        WHEN CAST(strftime('%s', date) AS int) > strftime('%s', date('now', '-30 days')) 
        THEN 1 ELSE 0 END) as totalRuns,
      AVG(CASE WHEN pace != '' THEN CAST((substring(pace,1,instr(pace,':')-1)*60 + substring(pace,instr(pace,':')+1))*60/distance AS int) END) / 60 as avgPaceMin
      FROM runs WHERE user_id = 1
    `).get();
    
    const stats = {
      today: { distance, pace, steps },
      history30Days: { 
        avgPace: history.avgPaceMin ? `${Math.floor(history.avgPaceMin)}:${Math.floor((history.avgPaceMin % 1)*60).toString().padStart(2,'0')}` : '6:15',
        totalRuns: history.totalRuns || 12
      }
    };
    
    const aiSummary = await generateSummary(user, stats, locationName);
    
    // Save summary
    const stmt = db.prepare('UPDATE runs SET ai_summary = ? WHERE id = (SELECT MAX(id) FROM runs)');
    stmt.run(aiSummary);
    
    res.json({ locationName, stats, aiSummary });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// 2. Records CRUD - GET
router.get('/records', (req, res) => {
  const runs = db.prepare('SELECT * FROM runs WHERE user_id = 1 ORDER BY date DESC').all();
  res.json(runs);
});

// 3. Collaborative pin
router.post('/pins', (req, res) => {
  const { lat, lng, name } = req.body;
  const stmt = db.prepare('INSERT INTO pins (lat, lng, name, user_id) VALUES (?, ?, ?, 1)');
  const info = stmt.run(lat, lng, name);
  res.json({ id: info.lastInsertRowid, message: 'Pin added!' });
});

module.exports = router;

