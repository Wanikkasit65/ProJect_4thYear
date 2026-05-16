const { GoogleGenerativeAI } = require('@google/generative-ai');
require('dotenv').config();

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
const model = genAI.getGenerativeModel({ model: 'gemini-1.5-pro' });

async function generateSummary(profile, stats, locationName) {
  if (!process.env.GEMINI_API_KEY) {
    return 'Mock summary (set GEMINI_API_KEY): สวัสดีเจ้า! วิ่งดีมากที่ประตูท่าแพ Pace เร็วกว่าค่าเฉลี่ย ปิ๊กบ้านไปพักเถิด!';
  }

  const prompt = `
คุณคือ "โค้ชวิ่งพี่เหนือ" ที่เป็นกันเองและรอบรู้เรื่องที่เที่ยวในเชียงใหม่
ข้อมูลผู้ใช้: อายุ ${profile.age} ปี, อยู่จังหวัด ${profile.province}
พิกัดวิ่งวันนี้: ${locationName}

สถิติวันนี้: ระยะทาง ${stats.today.distance} กม., Pace ${stats.today.pace}, จำนวน ${stats.today.steps} ก้าว
สถิติ 30 วันที่ผ่านมา: Pace เฉลี่ยของคุณคือ ${stats.history30Days.avgPace} (วิ่งมาแล้ว ${stats.history30Days.totalRuns} ครั้งเดือนนี้)

เงื่อนไขการตอบ:
1. ทักทายโดยเอ่ยถึงชื่อสถานที่ ${locationName} และบรรยากาศในเชียงใหม่
2. วิเคราะห์ว่าวันนี้วิ่ง "เร็วกว่า" หรือ "ช้ากว่า" ค่าเฉลี่ย 30 วันอย่างไร
3. ชมเชยเรื่องวินัยที่วิ่งมาแล้ว ${stats.history30Days.totalRuns} ครั้ง
4. ใช้ภาษาที่เป็นกันเอง มีกลิ่นอายคนเหนือ (เช่น ใช้คำว่า "เจ้า", "ปิ๊กบ้าน")
5. สรุปสั้นๆ ไม่เกิน 3-4 ประโยค
  `;

  try {
    const result = await model.generateContent(prompt);
    return result.response.text();
  } catch (error) {
    console.error('AI Error:', error);
    return 'ขออภัย มีปัญหากับ AI โค้ช วันนี้วิ่งดีมากเลยนะ!';
  }
}

module.exports = { generateSummary };

