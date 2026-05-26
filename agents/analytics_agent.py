"""
ICT Daily Agent — Analytics & Self-Improvement Agent
Analyses student responses and uses Gemini AI to generate improvement
suggestions so tomorrow's content is better than today's.
"""

import json
import logging
from datetime import date, timedelta
from typing import Optional

import google.generativeai as genai

import config
from database.db_manager import db

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Gemini configuration
# ---------------------------------------------------------------------------
genai.configure(api_key=config.GEMINI_API_KEY)

_analysis_model = genai.GenerativeModel(
    model_name=config.GEMINI_MODEL,
    generation_config=genai.GenerationConfig(
        temperature=0.4,
        max_output_tokens=2048,
    ),
)


# ===================================================================
# Daily Response Analysis
# ===================================================================

def analyze_daily_responses(class_standard: str, topic_name: str) -> dict:
    """Analyse all student responses received today for a given topic/class.

    Args:
        class_standard: Class number ("8"–"12").
        topic_name: The topic name whose responses are being analysed.

    Returns:
        Dictionary with aggregated analytics:
            total_responses     (int)
            read_percentage     (float)
            avg_understanding   (float) — 0-100 scale
            avg_quiz_score      (float)
            common_difficulties (list[str])
            suggestions         (list[str])
    """
    today_str = date.today().isoformat()

    try:
        responses = db.get_responses_for_topic(topic_name, class_standard)
        # Filter to today only
        responses = [
            r for r in responses
            if r.get("response_date") == today_str
        ]
    except Exception as exc:
        logger.error("DB error fetching responses for class %s: %s", class_standard, exc)
        responses = []

    if not responses:
        logger.info("No responses yet for class %s, topic '%s'.", class_standard, topic_name)
        return {
            "total_responses": 0,
            "read_percentage": 0.0,
            "avg_understanding": 0.0,
            "avg_quiz_score": 0.0,
            "common_difficulties": [],
            "suggestions": ["अभी कोई प्रतिक्रिया नहीं आई है।"],
        }

    total = len(responses)
    read_count = sum(1 for r in responses if r.get("has_read"))
    read_pct = round((read_count / total) * 100, 1) if total else 0.0

    # Map understanding levels to numeric scores
    understanding_map = {
        "पूरा समझा": 100,
        "ज़्यादातर समझा": 75,
        "थोड़ा समझा": 50,
        "नहीं समझा": 10,
    }
    understanding_scores = [
        understanding_map.get(r.get("understanding_level", ""), 50)
        for r in responses
    ]
    avg_understanding = round(sum(understanding_scores) / len(understanding_scores), 1)

    quiz_scores = [
        r.get("quiz_score", 0) for r in responses if r.get("quiz_score") is not None
    ]
    avg_quiz = round(sum(quiz_scores) / len(quiz_scores), 1) if quiz_scores else 0.0

    # Collect difficult parts mentioned by students
    difficulties: list[str] = []
    for r in responses:
        diff = r.get("difficult_part", "").strip()
        if diff and diff not in ("", "कुछ नहीं", "नहीं", "none", "None"):
            difficulties.append(diff)

    # De-duplicate keeping order
    seen: set[str] = set()
    unique_difficulties: list[str] = []
    for d in difficulties:
        if d not in seen:
            seen.add(d)
            unique_difficulties.append(d)

    # Build suggestions using simple heuristics
    suggestions: list[str] = []
    if read_pct < 50:
        suggestions.append("पढ़ने की दर कम है — WhatsApp पर रिमाइंडर भेजें।")
    if avg_understanding < 50:
        suggestions.append("समझ का स्तर कम है — अगली बार और सरल भाषा और चित्र उपयोग करें।")
    if avg_quiz < 40:
        suggestions.append("क्विज़ स्कोर कम है — मुख्य बिंदुओं को दोहराने वाला रिवीज़न भाग जोड़ें।")
    if unique_difficulties:
        suggestions.append(f"कठिन भाग: {', '.join(unique_difficulties[:5])}")

    if not suggestions:
        suggestions.append("सब अच्छा चल रहा है! 👍")

    analytics = {
        "total_responses": total,
        "read_percentage": read_pct,
        "avg_understanding": avg_understanding,
        "avg_quiz_score": avg_quiz,
        "common_difficulties": unique_difficulties[:10],
        "suggestions": suggestions,
    }

    logger.info(
        "Analytics for class %s / '%s': %d responses, %.1f%% read, avg understanding %.1f",
        class_standard, topic_name, total, read_pct, avg_understanding,
    )
    return analytics


# ===================================================================
# AI-Driven Improvement Hints
# ===================================================================

def generate_improvement_hints(class_standard: str) -> str:
    """Use Gemini to produce improvement suggestions based on historical feedback.

    Looks at the last 7 days of class stats and recent improvement logs to
    generate actionable tips that can be injected into the next content
    generation prompt.

    Args:
        class_standard: Class number string.

    Returns:
        A multi-line string with Hindi improvement hints.
    """
    # Gather historical data
    try:
        stats = db.get_class_stats(class_standard, days=7)
        recent_logs = db.get_recent_improvements(class_standard, limit=5)
    except Exception as exc:
        logger.error("DB error gathering historical data for class %s: %s", class_standard, exc)
        return ""

    if stats.get("total_responses", 0) == 0:
        logger.info("No historical responses for class %s — skipping improvement hints.", class_standard)
        return ""

    # Build a concise summary for Gemini
    past_suggestions = "\n".join(
        f"- {log.get('ai_suggestions', '')[:200]}"
        for log in recent_logs
    ) or "कोई पूर्व सुझाव नहीं"

    prompt = f"""तुम एक AI शिक्षक सहायक हो। पिछले 7 दिनों के आँकड़ों के आधार पर कक्षा {class_standard} के ICT कंटेंट
को बेहतर बनाने के लिए 4-6 ठोस सुझाव (हिंदी में) दो।

📊 पिछले 7 दिनों के आँकड़े:
- कुल प्रतिक्रियाएँ: {stats['total_responses']}
- पढ़ने की दर: {stats['read_percentage']}%
- औसत क्विज़ स्कोर: {stats['avg_quiz_score']}
- समझ का स्तर: {json.dumps(stats.get('understanding', {}), ensure_ascii=False)}

📝 पिछले सुझाव:
{past_suggestions}

सुझाव इन विषयों पर हों:
1. भाषा/कठिनाई स्तर
2. चित्र/SVG डायग्राम
3. उदाहरण
4. क्विज़ के प्रकार
5. विषय प्रस्तुति शैली

सिर्फ सुझाव दो, कुछ और नहीं। हर सुझाव एक बुलेट पॉइंट में।"""

    try:
        response = _analysis_model.generate_content(prompt)
        hints = response.text.strip()
        logger.info("Generated improvement hints for class %s (%d chars)", class_standard, len(hints))
        return hints

    except Exception as exc:
        logger.error("Gemini API error generating improvement hints: %s", exc)
        return ""


# ===================================================================
# Teacher Report
# ===================================================================

def create_teacher_report(date_str: Optional[str] = None) -> str:
    """Create a comprehensive daily summary report for the teacher.

    The report covers all classes and includes read rates, understanding
    levels, quiz scores, and AI-generated recommendations.

    Args:
        date_str: Target date in ISO format (YYYY-MM-DD).
                  Defaults to today.

    Returns:
        A formatted multi-line string report in Hindi.
    """
    if date_str is None:
        date_str = date.today().isoformat()

    report_lines: list[str] = [
        f"📊 *ICT दैनिक रिपोर्ट — {date_str}*",
        "=" * 40,
        "",
    ]

    any_data = False

    for cls in config.SUPPORTED_CLASSES:
        theme = config.CLASS_THEMES.get(cls, {})
        emoji = theme.get("emoji", "📚")
        class_label = theme.get("name", f"कक्षा {cls}")

        try:
            responses = db.get_responses_for_date(date_str, cls)
        except Exception as exc:
            logger.error("DB error fetching responses for class %s on %s: %s", cls, date_str, exc)
            responses = []

        try:
            last_topic = db.get_last_topic(cls)
        except Exception:
            last_topic = None

        topic_name = last_topic["topic_name"] if last_topic else "—"

        report_lines.append(f"{emoji} *{class_label}*")
        report_lines.append(f"   📖 विषय: {topic_name}")

        if not responses:
            report_lines.append("   ⚠️ कोई प्रतिक्रिया नहीं")
            report_lines.append("")
            continue

        any_data = True
        total = len(responses)
        read_count = sum(1 for r in responses if r.get("has_read"))
        read_pct = round((read_count / total) * 100, 1)

        quiz_scores = [
            r.get("quiz_score", 0) for r in responses if r.get("quiz_score") is not None
        ]
        avg_quiz = round(sum(quiz_scores) / len(quiz_scores), 1) if quiz_scores else 0.0

        # Understanding distribution
        understanding_counts: dict[str, int] = {}
        for r in responses:
            level = r.get("understanding_level", "अज्ञात")
            understanding_counts[level] = understanding_counts.get(level, 0) + 1

        report_lines.append(f"   👥 प्रतिक्रियाएँ: {total}")
        report_lines.append(f"   📖 पढ़ा: {read_count}/{total} ({read_pct}%)")
        report_lines.append(f"   📝 औसत क्विज़ स्कोर: {avg_quiz}")
        report_lines.append(f"   🧠 समझ: {json.dumps(understanding_counts, ensure_ascii=False)}")

        # Top difficulties
        difficulties = [
            r.get("difficult_part", "").strip()
            for r in responses
            if r.get("difficult_part", "").strip()
            and r.get("difficult_part", "").strip().lower() not in ("", "नहीं", "कुछ नहीं", "none")
        ]
        if difficulties:
            report_lines.append(f"   ❓ कठिन भाग: {', '.join(difficulties[:3])}")

        report_lines.append("")

    # Overall summary
    report_lines.append("=" * 40)
    if any_data:
        report_lines.append("✅ रिपोर्ट तैयार है। विस्तृत विश्लेषण डैशबोर्ड पर देखें।")
    else:
        report_lines.append("⚠️ आज किसी भी कक्षा से कोई प्रतिक्रिया नहीं आई।")

    report_lines.append(f"\n— ICT Daily Agent 🤖 ({date_str})")

    report = "\n".join(report_lines)

    logger.info("Teacher report generated for %s (%d chars)", date_str, len(report))
    return report
