"""
ICT Daily Agent — Database Manager
Supabase (free cloud PostgreSQL) se sab data manage karta hai.
Tables: topics, topic_history, student_responses, improvement_log
"""

import logging
from datetime import date, datetime
from typing import Optional

from supabase import create_client, Client

import config

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Supabase database manager for the ICT Daily Agent system."""

    def __init__(self):
        """Initialize Supabase client."""
        if not config.SUPABASE_URL or not config.SUPABASE_KEY:
            logger.warning("Supabase credentials not configured. Database operations will fail.")
            self.client: Optional[Client] = None
            return
        self.client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
        logger.info("Supabase database connected successfully.")

    def _ensure_client(self) -> Client:
        """Ensure Supabase client is available."""
        if self.client is None:
            raise ConnectionError("Supabase client not initialized. Check SUPABASE_URL and SUPABASE_KEY.")
        return self.client

    # ================================================================
    # TOPIC HISTORY — Track which topics have been sent
    # ================================================================

    def get_covered_topics(self, class_standard: str) -> list[dict]:
        """Get list of all topics already covered for a class."""
        client = self._ensure_client()
        response = (
            client.table("topic_history")
            .select("*")
            .eq("class_standard", class_standard)
            .execute()
        )
        return response.data or []

    def get_covered_topic_names(self, class_standard: str) -> list[str]:
        """Get just the names of covered topics for a class."""
        covered = self.get_covered_topics(class_standard)
        return [t["topic_name"] for t in covered]

    def record_topic_sent(
        self,
        topic_name: str,
        class_standard: str,
        category: str,
        part_number: int,
        total_parts: int,
        pdf_path: str,
        pdf_url: str,
    ) -> dict:
        """Record that a topic PDF was sent to a class."""
        client = self._ensure_client()
        data = {
            "topic_name": topic_name,
            "class_standard": class_standard,
            "category": category,
            "part_number": part_number,
            "total_parts": total_parts,
            "pdf_path": pdf_path,
            "pdf_url": pdf_url,
            "sent_date": date.today().isoformat(),
            "sent_at": datetime.now().isoformat(),
        }
        response = client.table("topic_history").insert(data).execute()
        logger.info(f"Recorded topic '{topic_name}' part {part_number} sent to class {class_standard}")
        return response.data[0] if response.data else {}

    def get_last_topic(self, class_standard: str) -> Optional[dict]:
        """Get the most recently sent topic for a class."""
        client = self._ensure_client()
        response = (
            client.table("topic_history")
            .select("*")
            .eq("class_standard", class_standard)
            .order("sent_date", desc=True)
            .limit(1)
            .execute()
        )
        return response.data[0] if response.data else None

    def get_topic_part_status(self, topic_name: str, class_standard: str) -> dict:
        """Check how many parts of a multi-part topic have been sent."""
        client = self._ensure_client()
        response = (
            client.table("topic_history")
            .select("*")
            .eq("topic_name", topic_name)
            .eq("class_standard", class_standard)
            .order("part_number")
            .execute()
        )
        parts_sent = response.data or []
        return {
            "parts_sent": len(parts_sent),
            "last_part": parts_sent[-1]["part_number"] if parts_sent else 0,
            "total_parts": parts_sent[0]["total_parts"] if parts_sent else 0,
            "details": parts_sent,
        }

    # ================================================================
    # STUDENT RESPONSES — Track feedback from students
    # ================================================================

    def save_student_response(
        self,
        student_name: str,
        class_standard: str,
        topic_name: str,
        has_read: bool,
        understanding_level: str,
        difficult_part: str,
        quiz_answers: str,
        quiz_score: int,
    ) -> dict:
        """Save a student's response/feedback."""
        client = self._ensure_client()
        data = {
            "student_name": student_name,
            "class_standard": class_standard,
            "topic_name": topic_name,
            "has_read": has_read,
            "understanding_level": understanding_level,
            "difficult_part": difficult_part,
            "quiz_answers": quiz_answers,
            "quiz_score": quiz_score,
            "response_date": date.today().isoformat(),
            "responded_at": datetime.now().isoformat(),
        }
        response = client.table("student_responses").insert(data).execute()
        logger.info(f"Saved response from '{student_name}' for class {class_standard}")
        return response.data[0] if response.data else {}

    def get_responses_for_topic(self, topic_name: str, class_standard: str) -> list[dict]:
        """Get all student responses for a specific topic and class."""
        client = self._ensure_client()
        response = (
            client.table("student_responses")
            .select("*")
            .eq("topic_name", topic_name)
            .eq("class_standard", class_standard)
            .execute()
        )
        return response.data or []

    def get_responses_for_date(self, target_date: str, class_standard: Optional[str] = None) -> list[dict]:
        """Get all responses for a specific date, optionally filtered by class."""
        client = self._ensure_client()
        query = (
            client.table("student_responses")
            .select("*")
            .eq("response_date", target_date)
        )
        if class_standard:
            query = query.eq("class_standard", class_standard)
        response = query.execute()
        return response.data or []

    def get_class_stats(self, class_standard: str, days: int = 7) -> dict:
        """Get statistics for a class over the last N days."""
        client = self._ensure_client()
        from datetime import timedelta
        start_date = (date.today() - timedelta(days=days)).isoformat()

        responses = (
            client.table("student_responses")
            .select("*")
            .eq("class_standard", class_standard)
            .gte("response_date", start_date)
            .execute()
        ).data or []

        if not responses:
            return {
                "total_responses": 0,
                "read_count": 0,
                "read_percentage": 0,
                "avg_quiz_score": 0,
                "understanding": {"पूरा समझा": 0, "थोड़ा समझा": 0, "नहीं समझा": 0},
            }

        read_count = sum(1 for r in responses if r.get("has_read"))
        quiz_scores = [r.get("quiz_score", 0) for r in responses if r.get("quiz_score") is not None]
        understanding = {}
        for r in responses:
            level = r.get("understanding_level", "अज्ञात")
            understanding[level] = understanding.get(level, 0) + 1

        return {
            "total_responses": len(responses),
            "read_count": read_count,
            "read_percentage": round((read_count / len(responses)) * 100, 1) if responses else 0,
            "avg_quiz_score": round(sum(quiz_scores) / len(quiz_scores), 1) if quiz_scores else 0,
            "understanding": understanding,
        }

    # ================================================================
    # IMPROVEMENT LOG — Track AI self-improvement suggestions
    # ================================================================

    def save_improvement_log(
        self,
        topic_name: str,
        class_standard: str,
        avg_understanding: float,
        avg_quiz_score: float,
        ai_suggestions: str,
    ) -> dict:
        """Save AI improvement suggestions based on student feedback."""
        client = self._ensure_client()
        data = {
            "topic_name": topic_name,
            "class_standard": class_standard,
            "avg_understanding": avg_understanding,
            "avg_quiz_score": avg_quiz_score,
            "ai_suggestions": ai_suggestions,
            "log_date": date.today().isoformat(),
        }
        response = client.table("improvement_log").insert(data).execute()
        logger.info(f"Saved improvement log for '{topic_name}' class {class_standard}")
        return response.data[0] if response.data else {}

    def get_recent_improvements(self, class_standard: str, limit: int = 5) -> list[dict]:
        """Get recent improvement suggestions for a class."""
        client = self._ensure_client()
        response = (
            client.table("improvement_log")
            .select("*")
            .eq("class_standard", class_standard)
            .order("log_date", desc=True)
            .limit(limit)
            .execute()
        )
        return response.data or []

    # ================================================================
    # DASHBOARD DATA — Aggregated stats for teacher
    # ================================================================

    def get_dashboard_data(self) -> dict:
        """Get comprehensive dashboard data for all classes."""
        dashboard = {}
        for cls in config.SUPPORTED_CLASSES:
            stats = self.get_class_stats(cls, days=7)
            last_topic = self.get_last_topic(cls)
            total_topics = len(self.get_covered_topics(cls))
            dashboard[cls] = {
                "stats": stats,
                "last_topic": last_topic,
                "total_topics_covered": total_topics,
                "theme": config.CLASS_THEMES[cls],
            }
        return dashboard


# Singleton instance
db = DatabaseManager()
