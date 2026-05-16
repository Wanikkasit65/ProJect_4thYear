// Test Mock for Feature 4: AI Summary
require('dotenv').config();
const { geocode } = require('./services/geocode');
const { generateSummary } = require('./services/ai');

async function testAI() {
  const lat = 18.7883, lng = 98.9853;
  const locationName = geocode(lat, lng);
  const profile = { age: 21, province: 'เชียงใหม่' };
  const stats = {
    today: { distance: 5.0, pace: '5:45', steps: 5200 },
    history30Days: { avgPace: '6:15', totalRuns: 12 }
  };

  console.log('=== Test AI Summary ===');
  console.log('Location:', locationName);
  console.log('Stats:', stats);
  
const summary = await generateSummary(profile, stats, locationName).catch(() => 'Fallback mock: สวัสดีเจ้า! Pace 5:45 ดีมาก เร็วกว่า avg 6:15 ที่ประตูท่าแพ วินัย 12 ครั้ง ปิ๊กบ้าน!');
  console.log('\\nAI Coach:', summary);
  console.log('\\nTest complete! Set GEMINI_API_KEY for real AI.');
}

testAI();

