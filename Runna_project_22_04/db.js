const Database = require('better-sqlite3');
const path = require('path');
require('dotenv').config();

const dbPath = process.env.DB_PATH || path.join(__dirname, 'runna.db');
const db = new Database(dbPath);

db.exec(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    age INTEGER,
    province TEXT
  );

  CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    lat REAL,
    lng REAL,
    location_name TEXT,
    distance REAL,
    pace TEXT,
    steps INTEGER,
    date TEXT,
    ai_summary TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)
  );

  CREATE TABLE IF NOT EXISTS pins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lat REAL,
    lng REAL,
    name TEXT,
    user_id INTEGER
  );
`);

// Seed mock user
const insertUser = db.prepare('INSERT OR IGNORE INTO users (id, age, province) VALUES (1, 21, ?)');
insertUser.run('เชียงใหม่');

// Mock historical runs for pace avg
const insertRun = db.prepare('INSERT OR IGNORE INTO runs (id, user_id, lat, lng, location_name, distance, pace, steps, date) VALUES (?, 1, ?, ?, ?, ?, ?, ?, ?)');
insertRun.run(1, 18.7883, 98.9853, 'ประตูท่าแพ', 4.5, '6:20', 4800, '2024-04-01');
insertRun.run(2, 18.7970, 98.9817, 'อ่างแก้ว มช.', 5.2, '6:10', 5300, '2024-04-10');

module.exports = db;

