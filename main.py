"""
ICT Daily Agent — Main Orchestrator
Ye file sab agents ko sequentially chalata hai:
1. Topic select karo
2. Content generate karo (Gemini AI)
3. PDF banao (Hindi, colorful)
4. WhatsApp pe bhejo
5. Analytics run karo
"""

import logging
import sys
from datetime import date

import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("ICT-Daily-Agent")


def run_daily_job(target_classes: list[str] | None = None):
    """
    Run the complete daily PDF generation and sending pipeline.

    Args:
        target_classes: List of class standards to process. 
                       If None, processes all supported classes.
    """
    classes = target_classes or config.SUPPORTED_CLASSES
    logger.info(f"{'='*60}")
    logger.info(f"🚀 ICT Daily Agent — Starting daily job for {date.today()}")
    logger.info(f"📚 Classes to process: {', '.join(classes)}")
    logger.info(f"{'='*60}")

    # Import agents (lazy import to avoid circular deps)
    from agents.topic_selector import select_daily_topic
    from agents.content_generator import generate_content
    from agents.pdf_generator import create_pdf
    from agents.whatsapp_sender import send_to_class, send_teacher_summary
    from agents.analytics_agent import (
        analyze_daily_responses,
        generate_improvement_hints,
        create_teacher_report,
    )
    from database.db_manager import db

    results = {}

    for cls in classes:
        logger.info(f"\n{'─'*50}")
        logger.info(f"📖 Processing Class {cls} ({config.CLASS_THEMES[cls]['name']})")
        logger.info(f"{'─'*50}")

        try:
            # ─────────────────────────────────────────────────
            # Step 1: Select today's topic
            # ─────────────────────────────────────────────────
            logger.info(f"🧠 Step 1: Selecting topic for class {cls}...")
            topic_info = select_daily_topic(cls)
            if not topic_info:
                logger.warning(f"⚠️ No topic available for class {cls}. Skipping.")
                results[cls] = {"status": "skipped", "reason": "no_topic"}
                continue

            topic_name = topic_info["topic_name"]
            part_number = topic_info.get("part_number", 1)
            total_parts = topic_info.get("total_parts", 1)
            subtopics = topic_info.get("subtopics", [])
            category = topic_info.get("category", "General")

            part_str = f" (भाग {part_number}/{total_parts})" if total_parts > 1 else ""
            logger.info(f"✅ Selected: {topic_name}{part_str} [{category}]")

            # ─────────────────────────────────────────────────
            # Step 2: Get improvement hints from past feedback
            # ─────────────────────────────────────────────────
            logger.info(f"📊 Step 2: Getting improvement hints for class {cls}...")
            try:
                improvement_hints = generate_improvement_hints(cls)
            except Exception as e:
                logger.warning(f"⚠️ Could not get improvement hints: {e}")
                improvement_hints = ""

            # ─────────────────────────────────────────────────
            # Step 3: Generate content using Gemini AI
            # ─────────────────────────────────────────────────
            logger.info(f"✍️ Step 3: Generating content with Gemini AI...")
            content = generate_content(
                topic_name=topic_name,
                class_standard=cls,
                part_number=part_number,
                total_parts=total_parts,
                subtopics=subtopics,
                improvement_hints=improvement_hints,
            )
            if not content:
                logger.error(f"❌ Content generation failed for class {cls}")
                results[cls] = {"status": "error", "reason": "content_generation_failed"}
                continue
            logger.info(f"✅ Content generated: {len(content.get('main_content', ''))} chars")

            # ─────────────────────────────────────────────────
            # Step 4: Create beautiful PDF
            # ─────────────────────────────────────────────────
            logger.info(f"📄 Step 4: Creating PDF...")
            pdf_path = create_pdf(
                content=content,
                class_standard=cls,
                topic_name=topic_name,
                part_number=part_number,
                total_parts=total_parts,
            )
            if not pdf_path:
                logger.error(f"❌ PDF creation failed for class {cls}")
                results[cls] = {"status": "error", "reason": "pdf_creation_failed"}
                continue
            logger.info(f"✅ PDF created: {pdf_path}")

            # ─────────────────────────────────────────────────
            # Step 5: Upload PDF to Cloudinary & optionally send via WhatsApp
            # ─────────────────────────────────────────────────
            logger.info(f"☁️ Step 5a: Uploading PDF to Cloudinary...")
            from agents.whatsapp_sender import upload_pdf_to_cloudinary
            try:
                pdf_url = upload_pdf_to_cloudinary(str(pdf_path))
                logger.info(f"✅ PDF uploaded: {pdf_url}")
            except Exception as e:
                logger.error(f"❌ PDF upload failed: {e}")
                pdf_url = ""

            response_url = f"{config.APP_BASE_URL}/form/{cls}/{date.today().isoformat()}"

            # Check if WhatsApp is configured — if yes, auto-send; if not, manual share
            if config.WHATSAPP_ACCESS_TOKEN and pdf_url:
                logger.info(f"📱 Step 5b: Auto-sending to WhatsApp group for class {cls}...")
                send_results = send_to_class(
                    class_standard=cls,
                    pdf_url=pdf_url,
                    topic_name=f"{topic_name}{part_str}",
                    response_link=response_url,
                )
                logger.info(f"✅ WhatsApp auto-send complete")
            else:
                send_results = []
                if not config.WHATSAPP_ACCESS_TOKEN:
                    logger.info(f"📋 WhatsApp token not configured — PDF ready for manual share on dashboard")
                else:
                    logger.warning(f"⚠️ Skipping WhatsApp send — no PDF URL")

            # ─────────────────────────────────────────────────
            # Step 6: Record in database
            # ─────────────────────────────────────────────────
            logger.info(f"💾 Step 6: Recording in database...")
            db.record_topic_sent(
                topic_name=topic_name,
                class_standard=cls,
                category=category,
                part_number=part_number,
                total_parts=total_parts,
                pdf_path=str(pdf_path),
                pdf_url=pdf_url,
            )
            logger.info(f"✅ Recorded in database")

            results[cls] = {
                "status": "success",
                "topic": topic_name,
                "part": f"{part_number}/{total_parts}",
                "pdf_path": str(pdf_path),
                "whatsapp": send_results,
            }

        except Exception as e:
            logger.error(f"❌ Error processing class {cls}: {e}", exc_info=True)
            results[cls] = {"status": "error", "reason": str(e)}

    # ─────────────────────────────────────────────────
    # Step 7: Analyze yesterday's responses & send teacher report
    # ─────────────────────────────────────────────────
    logger.info(f"\n{'─'*50}")
    logger.info(f"📊 Step 7: Analyzing responses & creating teacher report...")
    logger.info(f"{'─'*50}")

    try:
        teacher_report = create_teacher_report()
        if teacher_report and config.TEACHER_PHONE and config.WHATSAPP_ACCESS_TOKEN:
            send_teacher_summary(teacher_report)
            logger.info("✅ Teacher report sent via WhatsApp")
        elif teacher_report:
            logger.info("ℹ️ Teacher report ready on dashboard (WhatsApp not configured)")
        else:
            logger.info("ℹ️ No report data yet")
    except Exception as e:
        logger.error(f"⚠️ Could not process teacher report: {e}")

    # ─────────────────────────────────────────────────
    # Summary
    # ─────────────────────────────────────────────────
    logger.info(f"\n{'='*60}")
    logger.info(f"🎉 Daily job completed! Results:")
    for cls, result in results.items():
        status_emoji = "✅" if result["status"] == "success" else "⚠️" if result["status"] == "skipped" else "❌"
        logger.info(f"  {status_emoji} Class {cls}: {result['status']}")
        if result["status"] == "success":
            logger.info(f"     📖 Topic: {result['topic']} (Part {result['part']})")
    logger.info(f"{'='*60}")

    return results


def run_single_class(class_standard: str):
    """Run the pipeline for a single class only."""
    if class_standard not in config.SUPPORTED_CLASSES:
        logger.error(f"Invalid class: {class_standard}. Supported: {config.SUPPORTED_CLASSES}")
        return None
    return run_daily_job(target_classes=[class_standard])


if __name__ == "__main__":
    # If run directly, process all classes
    import argparse

    parser = argparse.ArgumentParser(description="ICT Daily Agent — Generate and send daily ICT PDFs")
    parser.add_argument(
        "--class", "-c",
        dest="target_class",
        choices=config.SUPPORTED_CLASSES,
        help="Process only a specific class (e.g., 8, 9, 10, 11, 12)",
    )
    args = parser.parse_args()

    if args.target_class:
        run_single_class(args.target_class)
    else:
        run_daily_job()
