const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const db = require('./db');
const runRoutes = require('./routes/runs');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

app.use('/api/runs', runRoutes);

app.get('/', (req, res) => {
  res.json({ message: 'Runna AI Coach API - Ready! Test POST /api/runs/ai-summary' });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log('DB path:', process.env.DB_PATH || './runna.db');
});

module.exports = app;

