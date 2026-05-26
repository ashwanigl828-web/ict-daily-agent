"""
ICT Daily Agent — Agents Package
All agent modules are imported here for easy access.
"""

from agents.topic_selector import select_daily_topic
from agents.content_generator import generate_content
from agents.pdf_generator import create_pdf, create_test_pdf
from agents.whatsapp_sender import (
    upload_pdf_to_cloudinary,
    send_document,
    send_to_class,
    send_text_message,
    send_teacher_summary,
)
from agents.analytics_agent import (
    analyze_daily_responses,
    generate_improvement_hints,
    create_teacher_report,
)

__all__ = [
    "select_daily_topic",
    "generate_content",
    "create_pdf",
    "create_test_pdf",
    "upload_pdf_to_cloudinary",
    "send_document",
    "send_to_class",
    "send_text_message",
    "send_teacher_summary",
    "analyze_daily_responses",
    "generate_improvement_hints",
    "create_teacher_report",
]
