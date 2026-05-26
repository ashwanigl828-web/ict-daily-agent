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
        """Get comprehensive dashboard data for all classes.
        
        Returns the exact structure expected by dashboard.html:
        {
            "current_date": "2025-05-26",
            "total_responses": 42,
            "total_read_percent": 75.0,
            "avg_quiz_score": 68.5,
            "total_topics": 15,
            "classes": {
                "8": { ... per-class stats ... },
                ...
            },
            "recent_topics": [ ... ],
        }
        """
        today_str = date.today().isoformat()

        classes_data = {}
        grand_total_responses = 0
        grand_read_count = 0
        grand_quiz_scores = []
        grand_total_topics = 0
        all_recent_topics = []

        for cls in config.SUPPORTED_CLASSES:
            try:
                # Get today's responses for this class
                today_responses = self.get_responses_for_date(today_str, cls)
                total_resp = len(today_responses)
                read_count = sum(1 for r in today_responses if r.get("has_read"))
                read_pct = round((read_count / total_resp) * 100, 1) if total_resp else 0

                quiz_scores = [r.get("quiz_score", 0) for r in today_responses if r.get("quiz_score") is not None]
                avg_quiz = round(sum(quiz_scores) / len(quiz_scores), 1) if quiz_scores else 0

                # Understanding breakdown
                full_count = sum(1 for r in today_responses if r.get("understanding_level") in ("easy", "पूरा समझा"))
                partial_count = sum(1 for r in today_responses if r.get("understanding_level") in ("medium", "थोड़ा समझा", "ज़्यादातर समझा"))
                none_count = sum(1 for r in today_responses if r.get("understanding_level") in ("hard", "not_understood", "नहीं समझा"))
                und_total = full_count + partial_count + none_count or 1  # avoid div by zero

                # Topic info
                last_topic_data = self.get_last_topic(cls)
                last_topic_name = last_topic_data["topic_name"] if last_topic_data else ""
                total_topics = len(self.get_covered_topics(cls))

                # Number of registered students (contacts)
                try:
                    contacts = self.client.table("whatsapp_contacts").select("id").eq("class_standard", cls).eq("is_active", True).execute()
                    total_students = len(contacts.data) if contacts.data else 0
                except Exception:
                    total_students = 0

                classes_data[cls] = {
                    "total_responses": total_resp,
                    "total_students": total_students,
                    "read_percent": read_pct,
                    "avg_quiz_score": avg_quiz,
                    "total_topics_covered": total_topics,
                    "last_topic": last_topic_name,
                    "pdf_url": last_topic_data.get("pdf_url", "") if last_topic_data else "",
                    "response_url": f"{config.APP_BASE_URL}/form/{cls}/{today_str}" if last_topic_name else "",
                    "understanding": {
                        "full": round((full_count / und_total) * 100),
                        "partial": round((partial_count / und_total) * 100),
                        "none": round((none_count / und_total) * 100),
                        "full_count": full_count,
                        "partial_count": partial_count,
                        "none_count": none_count,
                    },
                }

                grand_total_responses += total_resp
                grand_read_count += read_count
                grand_quiz_scores.extend(quiz_scores)
                grand_total_topics += total_topics

                # Build recent topics list
                if last_topic_data:
                    all_recent_topics.append({
                        "date": last_topic_data.get("sent_date", today_str),
                        "class_standard": cls,
                        "topic_name": last_topic_name,
                        "responses": total_resp,
                        "read_percent": read_pct,
                        "avg_score": avg_quiz,
                    })

            except Exception as e:
                logger.error(f"Error loading dashboard data for class {cls}: {e}")
                classes_data[cls] = {
                    "total_responses": 0,
                    "total_students": 0,
                    "read_percent": 0,
                    "avg_quiz_score": 0,
                    "total_topics_covered": 0,
                    "last_topic": "",
                    "pdf_url": "",
                    "response_url": "",
                    "understanding": {
                        "full": 0, "partial": 0, "none": 0,
                        "full_count": 0, "partial_count": 0, "none_count": 0,
                    },
                }

        grand_read_pct = round((grand_read_count / grand_total_responses) * 100, 1) if grand_total_responses else 0
        grand_avg_quiz = round(sum(grand_quiz_scores) / len(grand_quiz_scores), 1) if grand_quiz_scores else 0

        return {
            "current_date": today_str,
            "total_responses": grand_total_responses,
            "total_read_percent": grand_read_pct,
            "avg_quiz_score": grand_avg_quiz,
            "total_topics": grand_total_topics,
            "classes": classes_data,
            "recent_topics": sorted(all_recent_topics, key=lambda x: x["date"], reverse=True),
        }


# Singleton instance
db = DatabaseManager()
