"""Run performance analysis with Gemini API."""

from __future__ import annotations

import json
from dataclasses import dataclass

import httpx

from app.core.config import settings


@dataclass
class AnalysisResult:
    insight: str
    reasoning: str
    recommendations: str


class AnalysisService:
    def analyze(
        self,
        *,
        distance_km: float,
        duration_seconds: int,
        step_count: int,
        avg_pace_min_per_km: float | None,
        recent_runs: list[dict],
    ) -> AnalysisResult:
        structured = self._build_structured_summary(
            distance_km=distance_km,
            duration_seconds=duration_seconds,
            step_count=step_count,
            avg_pace_min_per_km=avg_pace_min_per_km,
            recent_runs=recent_runs,
        )

        if settings.gemini_api_key:
            gemini_result = self._call_gemini(structured)
            if gemini_result is not None:
                return gemini_result

        return self._rule_based_analysis(structured)

    def _build_structured_summary(
        self,
        *,
        distance_km: float,
        duration_seconds: int,
        step_count: int,
        avg_pace_min_per_km: float | None,
        recent_runs: list[dict],
    ) -> dict:
        # ดักจับและป้องกันปัญหาระยะทางเป็น 0 ไม่ให้สูตรคำนวณ Pace พัง (Division by Zero)
        pace = avg_pace_min_per_km
        if pace is None and distance_km > 0:
            pace = (duration_seconds / 60.0) / distance_km
        elif distance_km == 0:
            pace = 0.0

        recent_paces = [
            item["avg_pace_min_per_km"]
            for item in recent_runs
            if item.get("avg_pace_min_per_km") is not None and item.get("avg_pace_min_per_km") > 0
        ]
        avg_recent_pace = sum(recent_paces) / len(recent_paces) if recent_paces else None

        pace_delta = 0.0
        if pace > 0 and avg_recent_pace is not None:
            pace_delta = round(pace - avg_recent_pace, 2)

        # ดักจับและป้องกันปัญหาระยะเวลาเป็น 0 ไม่ให้สูตรคำนวณ รอบขา (Cadence) พัง
        cadence = 0.0
        if duration_seconds > 0 and step_count > 0:
            cadence = round(step_count / (duration_seconds / 60.0), 0)

        return {
            "distance_km": round(distance_km, 2),
            "duration_minutes": round(duration_seconds / 60.0, 1),
            "step_count": step_count,
            "avg_pace_min_per_km": round(pace, 2),
            "cadence_spm": cadence,
            "recent_run_count": len(recent_runs),
            "pace_delta_vs_recent": pace_delta,
        }

    def _rule_based_analysis(self, data: dict) -> AnalysisResult:
        """ระบบวิเคราะห์สำรอง (Fallback) กรณีที่เชื่อมต่อ Gemini API ไม่สำเร็จ."""
        pace = data.get("avg_pace_min_per_km", 0)
        pace_delta = data.get("pace_delta_vs_recent", 0)
        cadence = data.get("cadence_spm", 0)

        if data["distance_km"] == 0:
            insight = "Your run was recorded, but distance is zero."
        elif pace_delta <= -0.3:
            insight = "Strong run. Your pace was faster than your recent average."
        elif pace_delta >= 0.3:
            insight = "This run was slower than your recent average. Recovery or fatigue may be a factor."
        else:
            insight = "Steady performance. Your pace stayed close to your recent average."

        reasoning_parts = [
            f"You covered {data['distance_km']} km in {data['duration_minutes']} minutes.",
        ]
        if pace > 0:
            reasoning_parts.append(f"Average pace was {pace} min/km.")
        if cadence > 0:
            reasoning_parts.append(f"Estimated cadence was about {cadence} steps per minute.")

        recommendations = []
        if data["distance_km"] == 0:
            recommendations.append("Please check your GPS settings or try running a longer distance next time.")
        elif pace > 7.5:
            recommendations.append("Try shorter intervals to gradually improve pace consistency.")
        else:
            recommendations.append("Maintain this pace on your next easy run to build consistency.")

        return AnalysisResult(
            insight=insight,
            reasoning=" ".join(reasoning_parts),
            recommendations=" ".join(recommendations),
        )

    def _call_gemini(self, data: dict) -> AnalysisResult | None:
        """เรียกใช้งาน Google Gemini API เพื่อสรุปผลการวิ่งเป็นภาษาไทยในรูปแบบ JSON."""
        prompt = (
            "คุณคือโค้ชวิ่งมืออาชีพและผู้เชี่ยวชาญด้านวิทยาศาสตร์การกีฬา "
            "จงวิเคราะห์ข้อมูลการวิ่งต่อไปนี้และตอบกลับมาเป็น 'ภาษาไทยเท่านั้น' ในรูปแบบ JSON "
            "ที่มีคีย์คือ \"insight\", \"reasoning\", และ \"recommendations\" ให้ถูกต้องสมบูรณ์ครบถ้วน\n\n"
            "⚠️ เงื่อนไขพิเศษ: หากข้อมูล distance_km หรือ duration_minutes เป็น 0 หรือน้อยมาก "
            "แปลว่าผู้ใช้อาจจะเพิ่งกดทดสอบปุ่มระบบ, ลืมเปิด GPS หรือเพิ่งเริ่มใช้งานแอปครั้งแรก "
            "ในคีย์ 'insight' ให้บอกยินดีต้อนรับสู่การทดสอบระบบพินและรอบวิ่งจำลอง, คีย์ 'reasoning' ให้เขียนอธิบายสั้นๆ ว่าทำไมข้อมูลสถิติรอบนี้ถึงออกมาเป็นศูนย์ "
            "และคีย์ 'recommendations' ให้เขียนแนะนำให้ลองเปิดสิทธิ์ GPS หรือเดินก้าวทดสอบเพื่อให้ระบบจับสัญญาณ หรือให้กำลังใจสั้นๆ ในการเริ่มวิ่งรอบจริงครั้งแรก\n\n"
            f"ข้อมูลการวิ่ง: {json.dumps(data)}"
        )
        
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"gemini-2.0-flash:generateContent?key={settings.gemini_api_key}"
        )
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.4},
        }

        try:
            with httpx.Client(timeout=20.0) as client:
                response = client.post(url, json=payload)
                response.raise_for_status()
                body = response.json()
                text = body["candidates"][0]["content"]["parts"][0]["text"]
                
                # ทำความสะอาดข้อมูลข้อความสำเร็จรูป
                cleaned = text.strip()
                if cleaned.startswith("```"):
                    cleaned = cleaned.split("\n", 1)[1]
                    if "```" in cleaned:
                        cleaned = cleaned.rsplit("```", 1)[0]
                if cleaned.startswith("json"):
                    cleaned = cleaned.split("\n", 1)[1]
                
                parsed = json.loads(cleaned.strip())
                return AnalysisResult(
                    insight=str(parsed.get("insight", "")),
                    reasoning=str(parsed.get("reasoning", "")),
                    recommendations=str(parsed.get("recommendations", "")),
                )
        except Exception:
            return None