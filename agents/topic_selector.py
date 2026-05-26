"""
ICT Daily Agent — Topic Selection Agent
Selects the next uncovered topic for a given class, respecting multi-part
continuation. Uses the database to track what has already been sent.
"""

import json
import logging
import random
from pathlib import Path
from typing import Optional

import config
from database.db_manager import db

logger = logging.getLogger(__name__)

# Path to the master topic bank
TOPICS_FILE = config.DATA_DIR / "topics.json"


def _load_topic_bank() -> dict[str, list[dict]]:
    """Load the full topic bank from the JSON data file.

    Returns:
        Dictionary mapping class standard strings to lists of topic dicts.

    Raises:
        FileNotFoundError: If topics.json is missing.
        json.JSONDecodeError: If topics.json is malformed.
    """
    if not TOPICS_FILE.exists():
        logger.error("Topic bank file not found: %s", TOPICS_FILE)
        raise FileNotFoundError(f"Topic bank file not found: {TOPICS_FILE}")

    with open(TOPICS_FILE, "r", encoding="utf-8") as fh:
        data: dict = json.load(fh)

    logger.info(
        "Loaded topic bank — classes: %s, total topics: %d",
        list(data.keys()),
        sum(len(v) for v in data.values()),
    )
    return data


def _pick_uncovered_topic(
    all_topics: list[dict],
    covered_names: list[str],
) -> Optional[dict]:
    """Return a random topic that has NOT been covered yet.

    Args:
        all_topics: Full list of topics for a class.
        covered_names: Topic names already sent.

    Returns:
        A topic dict, or None if every topic is already covered.
    """
    uncovered = [t for t in all_topics if t["topic_name"] not in covered_names]

    if not uncovered:
        logger.warning("All topics have been covered! Resetting pool.")
        # When every topic has been sent once, allow re-selection
        uncovered = all_topics

    selected = random.choice(uncovered)
    logger.info("Picked uncovered topic: %s", selected["topic_name"])
    return selected


def select_daily_topic(class_standard: str) -> dict:
    """Select the topic to send today for a given class.

    Logic:
    1. If the last sent topic was multi-part and not all parts have been
       sent, continue with the next part.
    2. Otherwise pick a random uncovered topic from the bank.

    Args:
        class_standard: The class number as a string ("8"–"12").

    Returns:
        Dictionary with keys:
            topic_name  (str)  — Topic name in Hindi
            category    (str)  — English category label
            part_number (int)  — Current part (1-indexed)
            total_parts (int)  — Total parts for this topic
            subtopics   (list) — List of subtopic strings

    Raises:
        ValueError: If class_standard is not supported.
        FileNotFoundError: If topics.json is missing.
    """
    if class_standard not in config.SUPPORTED_CLASSES:
        raise ValueError(
            f"Unsupported class: {class_standard}. "
            f"Supported: {config.SUPPORTED_CLASSES}"
        )

    # ------------------------------------------------------------------
    # Step 1 — Check if a multi-part topic is in progress
    # ------------------------------------------------------------------
    try:
        last_topic = db.get_last_topic(class_standard)
    except Exception as exc:
        logger.error("DB error fetching last topic for class %s: %s", class_standard, exc)
        last_topic = None

    if last_topic and last_topic.get("total_parts", 1) > 1:
        part_status = db.get_topic_part_status(
            last_topic["topic_name"], class_standard
        )
        last_part_sent = part_status["last_part"]
        total = part_status["total_parts"]

        if last_part_sent < total:
            next_part = last_part_sent + 1
            logger.info(
                "Continuing multi-part topic '%s' — part %d/%d",
                last_topic["topic_name"],
                next_part,
                total,
            )
            # Look up subtopics from the bank for completeness
            topic_bank = _load_topic_bank()
            class_topics = topic_bank.get(class_standard, [])
            matched = [
                t for t in class_topics
                if t["topic_name"] == last_topic["topic_name"]
            ]
            subtopics = matched[0]["subtopics"] if matched else []

            return {
                "topic_name": last_topic["topic_name"],
                "category": last_topic.get("category", "General"),
                "part_number": next_part,
                "total_parts": total,
                "subtopics": subtopics,
            }

    # ------------------------------------------------------------------
    # Step 2 — Pick a fresh topic
    # ------------------------------------------------------------------
    topic_bank = _load_topic_bank()
    class_topics = topic_bank.get(class_standard, [])

    if not class_topics:
        raise ValueError(f"No topics defined for class {class_standard} in topics.json")

    try:
        covered_names = db.get_covered_topic_names(class_standard)
    except Exception as exc:
        logger.error("DB error fetching covered topics: %s", exc)
        covered_names = []

    selected = _pick_uncovered_topic(class_topics, covered_names)

    if selected is None:
        # Fallback — should not happen because _pick_uncovered_topic resets
        selected = random.choice(class_topics)

    result = {
        "topic_name": selected["topic_name"],
        "category": selected.get("category", "General"),
        "part_number": 1,
        "total_parts": selected.get("total_parts", 1),
        "subtopics": selected.get("subtopics", []),
    }

    logger.info(
        "Selected topic for class %s: %s (part %d/%d)",
        class_standard,
        result["topic_name"],
        result["part_number"],
        result["total_parts"],
    )
    return result
