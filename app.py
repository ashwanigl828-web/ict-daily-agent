"""
ICT Daily Agent — Flask Web Application
24/7 Render.com pe chalega. Ye handle karta hai:
1. Student response form (QR code se open hota hai)
2. Teacher analytics dashboard
3. API endpoint for GitHub Actions to trigger daily job
4. Health check endpoint
"""

import logging
import sys
import threading
from datetime import date, datetime, timedelta

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    flash,
)

import config
from database.db_manager import db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("ICT-WebApp")

# Create Flask app
app = Flask(
    __name__,
    template_folder=str(config.TEMPLATES_DIR),
    static_folder=str(config.STATIC_DIR),
)
app.secret_key = config.FLASK_SECRET_KEY


# ================================================================
# Health Check — Render.com uses this to keep the app alive
# ================================================================

@app.route("/")
def home():
    """Home page — redirect to dashboard."""
    return redirect(url_for("dashboard"))


@app.route("/health")
def health():
    """Health check endpoint for Render.com."""
    return jsonify({
        "status": "healthy",
        "app": "ICT Daily Agent",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
    })


# ================================================================
# Student Response Form
# ================================================================

@app.route("/form/<class_standard>/<date_str>")
def response_form(class_standard: str, date_str: str):
    """Show the student response form for a specific class and date."""
    if class_standard not in config.SUPPORTED_CLASSES:
        return "कक्षा नहीं मिली! (Invalid class)", 404

    # Get today's topic for this class
    try:
        last_topic = db.get_last_topic(class_standard)
        topic_name = last_topic["topic_name"] if last_topic else "आज का टॉपिक"

        # Get quiz questions if available (stored in topic history or generate defaults)
        quiz_questions = []
    except Exception as e:
        logger.error(f"Error loading form data: {e}")
        topic_name = "ICT टॉपिक"
        quiz_questions = []

    theme = config.CLASS_THEMES.get(class_standard, config.CLASS_THEMES["8"])

    return render_template(
        "response_form.html",
        topic_name=topic_name,
        class_standard=class_standard,
        date_str=date_str,
        quiz_questions=quiz_questions,
        theme=theme,
    )


@app.route("/submit-response", methods=["POST"])
def submit_response():
    """Handle student response form submission."""
    try:
        student_name = request.form.get("student_name", "").strip()
        class_standard = request.form.get("class_standard", "")
        topic_name = request.form.get("topic_name", "")
        has_read = request.form.get("has_read") == "yes"
        understanding_level = request.form.get("understanding_level", "")
        difficult_part = request.form.get("difficult_part", "").strip()

        # Collect quiz answers
        quiz_answers = []
        for key in sorted(request.form.keys()):
            if key.startswith("quiz_"):
                quiz_answers.append(request.form[key])
        quiz_answers_str = ",".join(quiz_answers)

        # Calculate quiz score (we'll need to compare with correct answers)
        quiz_score = 0  # Will be calculated by analytics agent later

        if not student_name or not class_standard:
            flash("कृपया अपना नाम और कक्षा भरें!", "error")
            return redirect(request.referrer or "/")

        # Save to database
        db.save_student_response(
            student_name=student_name,
            class_standard=class_standard,
            topic_name=topic_name,
            has_read=has_read,
            understanding_level=understanding_level,
            difficult_part=difficult_part,
            quiz_answers=quiz_answers_str,
            quiz_score=quiz_score,
        )

        logger.info(f"✅ Response saved: {student_name} (Class {class_standard})")

        # Show success page
        return render_template(
            "response_success.html",
            student_name=student_name,
            class_standard=class_standard,
            theme=config.CLASS_THEMES.get(class_standard, config.CLASS_THEMES["8"]),
        )

    except Exception as e:
        logger.error(f"Error saving response: {e}", exc_info=True)
        flash("कुछ गड़बड़ हो गई! कृपया दोबारा कोशिश करें।", "error")
        return redirect(request.referrer or "/")


# ================================================================
# Teacher Dashboard
# ================================================================

@app.route("/dashboard")
def dashboard():
    """Teacher analytics dashboard."""
    try:
        dashboard_data = db.get_dashboard_data()
    except Exception as e:
        logger.error(f"Error loading dashboard: {e}")
        dashboard_data = {}

    # Enrich class data with PDF download URLs and response form URLs
    if isinstance(dashboard_data, dict) and "classes" in dashboard_data:
        for cls, cd in dashboard_data["classes"].items():
            # Get the latest topic's PDF URL from DB
            try:
                last_topic_data = db.get_last_topic(cls)
                if last_topic_data:
                    cd["pdf_url"] = last_topic_data.get("pdf_url", "")
                    cd["response_url"] = f"{config.APP_BASE_URL}/form/{cls}/{date.today().isoformat()}"
                else:
                    cd["pdf_url"] = ""
                    cd["response_url"] = ""
            except Exception:
                cd["pdf_url"] = ""
                cd["response_url"] = ""

    whatsapp_configured = bool(config.WHATSAPP_ACCESS_TOKEN)

    return render_template(
        "dashboard.html",
        dashboard_data=dashboard_data,
        supported_classes=config.SUPPORTED_CLASSES,
        class_themes=config.CLASS_THEMES,
        today=date.today().isoformat(),
        whatsapp_configured=whatsapp_configured,
        trigger_api_key=config.TRIGGER_API_KEY,
    )


@app.route("/dashboard/class/<class_standard>")
def class_detail(class_standard: str):
    """Detailed view for a specific class."""
    if class_standard not in config.SUPPORTED_CLASSES:
        return "कक्षा नहीं मिली!", 404

    try:
        stats = db.get_class_stats(class_standard, days=30)
        covered_topics = db.get_covered_topics(class_standard)
        recent_responses = db.get_responses_for_date(
            date.today().isoformat(), class_standard
        )
        improvements = db.get_recent_improvements(class_standard)
    except Exception as e:
        logger.error(f"Error loading class detail: {e}")
        stats = {}
        covered_topics = []
        recent_responses = []
        improvements = []

    theme = config.CLASS_THEMES.get(class_standard, config.CLASS_THEMES["8"])

    return render_template(
        "class_detail.html",
        class_standard=class_standard,
        theme=theme,
        stats=stats,
        covered_topics=covered_topics[-20:],  # Last 20 topics
        recent_responses=recent_responses,
        improvements=improvements,
    )


# ================================================================
# API Endpoints
# ================================================================

@app.route("/api/trigger-daily", methods=["POST"])
def trigger_daily():
    """
    API endpoint to trigger the daily PDF generation.
    Called by GitHub Actions cron job.
    Requires TRIGGER_API_KEY for authentication.
    """
    # Authenticate
    api_key = request.headers.get("X-API-Key") or request.args.get("api_key")
    if api_key != config.TRIGGER_API_KEY:
        logger.warning("⚠️ Unauthorized trigger attempt")
        return jsonify({"error": "Unauthorized"}), 401

    logger.info("🚀 Daily job triggered via API!")

    # Run in background thread so the API responds quickly
    def run_job():
        try:
            from main import run_daily_job
            run_daily_job()
        except Exception as e:
            logger.error(f"Daily job error: {e}", exc_info=True)

    thread = threading.Thread(target=run_job, daemon=True)
    thread.start()

    return jsonify({
        "status": "triggered",
        "message": "Daily PDF generation started in background",
        "timestamp": datetime.now().isoformat(),
    })


@app.route("/api/trigger-class/<class_standard>", methods=["POST"])
def trigger_single_class(class_standard: str):
    """Trigger PDF generation for a single class."""
    api_key = request.headers.get("X-API-Key") or request.args.get("api_key")
    if api_key != config.TRIGGER_API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    if class_standard not in config.SUPPORTED_CLASSES:
        return jsonify({"error": f"Invalid class: {class_standard}"}), 400

    def run_job():
        try:
            from main import run_single_class
            run_single_class(class_standard)
        except Exception as e:
            logger.error(f"Single class job error: {e}", exc_info=True)

    thread = threading.Thread(target=run_job, daemon=True)
    thread.start()

    return jsonify({
        "status": "triggered",
        "class": class_standard,
        "message": f"PDF generation started for class {class_standard}",
    })


@app.route("/api/stats")
def api_stats():
    """Get current stats for all classes (JSON API)."""
    try:
        dashboard_data = db.get_dashboard_data()
        # Convert to JSON-serializable format
        stats = {}
        for cls, data in dashboard_data.items():
            stats[cls] = {
                "total_topics_covered": data["total_topics_covered"],
                "last_topic": data["last_topic"]["topic_name"] if data["last_topic"] else None,
                "stats": data["stats"],
            }
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/responses/<class_standard>/<date_str>")
def api_responses(class_standard: str, date_str: str):
    """Get responses for a specific class and date."""
    try:
        responses = db.get_responses_for_date(date_str, class_standard)
        return jsonify({"responses": responses, "count": len(responses)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================================================================
# Error Handlers
# ================================================================

@app.errorhandler(404)
def not_found(e):
    """Custom 404 page."""
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(e):
    """Custom 500 page."""
    logger.error(f"Server error: {e}")
    return jsonify({"error": "Internal server error"}), 500


# ================================================================
# Run the app
# ================================================================

if __name__ == "__main__":
    port = int(config.APP_BASE_URL.split(":")[-1]) if "localhost" in config.APP_BASE_URL else 5000
    app.run(
        host="0.0.0.0",
        port=port,
        debug=True,
    )
