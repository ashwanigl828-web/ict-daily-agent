"""
ICT Daily Agent — Content Generation Agent
Uses Google Gemini AI to generate engaging ICT content in Hindi with
SVG diagrams, quiz questions, fun facts, and summaries.
"""

import json
import logging
import time
from typing import Optional

import google.generativeai as genai

import config

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Gemini Configuration
# ---------------------------------------------------------------------------
genai.configure(api_key=config.GEMINI_API_KEY)

_content_model = genai.GenerativeModel(
    model_name=config.GEMINI_MODEL,
    generation_config=genai.GenerationConfig(
        temperature=0.8,
        max_output_tokens=8192,
        response_mime_type="application/json",
    ),
)

# Maximum retries for Gemini API calls
_MAX_RETRIES = 3
_RETRY_DELAY_BASE = 4  # seconds, exponential back-off base


def _build_prompt(
    topic_name: str,
    class_standard: str,
    part_number: int,
    total_parts: int,
    subtopics: list[str],
    improvement_hints: str,
) -> str:
    """Build the full Gemini prompt for content generation.

    Args:
        topic_name: Topic title in Hindi.
        class_standard: Class number string ("8"–"12").
        part_number: Which part of the topic this is (1-indexed).
        total_parts: Total number of parts for this topic.
        subtopics: List of subtopic strings.
        improvement_hints: AI-generated suggestions from past feedback.

    Returns:
        The prompt string.
    """
    difficulty = config.CLASS_DIFFICULTY.get(class_standard, config.CLASS_DIFFICULTY["8"])
    level = difficulty["level"]
    description = difficulty["description"]
    word_limit = difficulty["word_limit"]
    quiz_diff = difficulty["quiz_difficulty"]

    subtopic_str = "\n".join(f"  - {st}" for st in subtopics) if subtopics else "  (कोई विशेष उपविषय नहीं)"

    part_instruction = ""
    if total_parts > 1:
        part_instruction = f"""
यह टॉपिक {total_parts} भागों में बँटा है। यह भाग {part_number}/{total_parts} है।
- भाग {part_number} के लिए उचित उपविषय कवर करो।
- पिछले भागों का संक्षिप्त रिकैप दो (अगर part > 1)।
- "अगले भाग में..." जोड़ो (अगर अभी last part नहीं है)।"""

    hints_section = ""
    if improvement_hints.strip():
        hints_section = f"""

🔧 *सुधार सुझाव (पिछले feedback के आधार पर):*
{improvement_hints}

ऊपर दिए सुझावों को इस कंटेंट में apply करो।"""

    prompt = f"""तुम एक भारतीय स्कूल शिक्षक हो जो कक्षा {class_standard} के छात्रों को ICT (Information and Communication Technology) सिखाते हो।

📋 *विषय:* {topic_name}
📚 *कक्षा:* {class_standard}
📊 *कठिनाई स्तर:* {level}
📝 *विवरण:* {description}
📏 *शब्द सीमा:* {word_limit}
{part_instruction}

*उपविषय:*
{subtopic_str}
{hints_section}

तुम्हें नीचे दिए JSON format में कंटेंट generate करना है। **पूरा कंटेंट हिंदी (देवनागरी लिपि) में होना चाहिए।**

**ज़रूरी नियम:**
1. भाषा सरल हिंदी में हो — जैसे बच्चों को समझा रहे हो। अंग्रेज़ी technical terms को brackets में हिंदी अनुवाद के साथ रखो।
2. कहानी या उदाहरण से शुरू करो — जैसे "सोचो अगर तुम्हारे पास कोई computer न हो..."
3. भारतीय संदर्भ के उदाहरण दो — UPI, Aadhaar, IRCTC, Digital India, Paytm, Google Pay, आदि।
4. इमोजी का भरपूर उपयोग करो 🎯📱💡🖥️
5. हर section को रोचक और engaging बनाओ।

**SVG Diagrams के नियम:**
- 2-3 SVG diagrams generate करो (flowchart, block diagram, hierarchy chart, etc.)
- हर SVG का width="400" और height="300" हो
- SVG में Hindi labels (Devanagari) का उपयोग करो
- रंगीन design बनाओ — fills, strokes, rounded rectangles, arrows
- SVG code complete और valid होना चाहिए
- Font family "Noto Sans Devanagari, Arial Unicode MS, sans-serif" use करो
- SVG simple और clear हो — ज़्यादा complex मत बनाओ

**Quiz के नियम ({quiz_diff}):**
- 4 multiple-choice questions दो
- हर question में 4 options (A, B, C, D) हों
- correct_answer में सही option का letter (A/B/C/D) दो
- Class level के हिसाब से difficulty adjust करो

**JSON Schema (STRICTLY follow करो):**
{{
  "topic_title": "विषय का शीर्षक हिंदी में",
  "introduction": "एक रोचक paragraph (50-80 words) जो topic introduce करे। कहानी या सवाल से शुरू करो।",
  "main_content": "विस्तृत explanation ({word_limit}). Headings ## use करो. हर concept को उदाहरण से समझाओ. Bullet points use करो.",
  "diagrams": [
    "<svg width='400' height='300' xmlns='http://www.w3.org/2000/svg'>...</svg>",
    "<svg width='400' height='300' xmlns='http://www.w3.org/2000/svg'>...</svg>"
  ],
  "fun_facts": [
    "🌟 रोचक तथ्य 1 हिंदी में",
    "🌟 रोचक तथ्य 2 हिंदी में",
    "🌟 रोचक तथ्य 3 हिंदी में"
  ],
  "quiz_questions": [
    {{
      "question": "प्रश्न हिंदी में?",
      "options": ["A) विकल्प 1", "B) विकल्प 2", "C) विकल्प 3", "D) विकल्प 4"],
      "correct_answer": "A"
    }}
  ],
  "summary": [
    "✅ मुख्य बिंदु 1",
    "✅ मुख्य बिंदु 2",
    "✅ मुख्य बिंदु 3"
  ]
}}

**IMPORTANT:**
- ONLY return valid JSON. No markdown, no code fences, no extra text.
- "diagrams" must be a JSON array of SVG strings (2 or 3 elements).
- "fun_facts" must have 3-5 items.
- "quiz_questions" must have exactly 4 items.
- "summary" must have 3-4 items.
- All content MUST be in Hindi (Devanagari)."""

    return prompt


def _parse_gemini_response(raw_text: str) -> dict:
    """Parse and validate the JSON response from Gemini.

    Handles minor formatting issues like markdown code fences that Gemini
    sometimes wraps around JSON.

    Args:
        raw_text: The raw text from Gemini's response.

    Returns:
        Parsed and validated content dictionary.

    Raises:
        ValueError: If parsing fails or required keys are missing.
    """
    text = raw_text.strip()

    # Strip markdown code fences if present
    if text.startswith("```"):
        first_newline = text.index("\n")
        text = text[first_newline + 1:]
    if text.endswith("```"):
        text = text[:-3].rstrip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        logger.error("JSON parse error: %s\nRaw text (first 500 chars): %s", exc, text[:500])
        raise ValueError(f"Failed to parse Gemini response as JSON: {exc}") from exc

    # Validate required keys
    required_keys = [
        "topic_title", "introduction", "main_content",
        "diagrams", "fun_facts", "quiz_questions", "summary",
    ]
    missing = [k for k in required_keys if k not in data]
    if missing:
        raise ValueError(f"Gemini response missing required keys: {missing}")

    # Ensure correct types and apply defaults
    if not isinstance(data["diagrams"], list):
        data["diagrams"] = []
    if not isinstance(data["fun_facts"], list):
        data["fun_facts"] = []
    if not isinstance(data["quiz_questions"], list):
        data["quiz_questions"] = []
    if not isinstance(data["summary"], list):
        data["summary"] = []

    return data


def generate_content(
    topic_name: str,
    class_standard: str,
    part_number: int = 1,
    total_parts: int = 1,
    subtopics: Optional[list[str]] = None,
    improvement_hints: str = "",
) -> dict:
    """Generate complete ICT lesson content using Gemini AI.

    Args:
        topic_name: The topic title in Hindi.
        class_standard: Class number ("8"–"12").
        part_number: Current part number (1-indexed).
        total_parts: Total parts for this topic.
        subtopics: List of subtopic strings.
        improvement_hints: AI feedback-based improvement suggestions.

    Returns:
        Dictionary with keys: topic_title, introduction, main_content,
        diagrams (list of SVG strings), fun_facts, quiz_questions, summary.

    Raises:
        RuntimeError: If all retry attempts fail.
    """
    if subtopics is None:
        subtopics = []

    prompt = _build_prompt(
        topic_name=topic_name,
        class_standard=class_standard,
        part_number=part_number,
        total_parts=total_parts,
        subtopics=subtopics,
        improvement_hints=improvement_hints,
    )

    last_error: Optional[Exception] = None

    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            logger.info(
                "Generating content for '%s' class %s (attempt %d/%d)",
                topic_name, class_standard, attempt, _MAX_RETRIES,
            )
            response = _content_model.generate_content(prompt)

            if not response.text:
                raise ValueError("Gemini returned an empty response.")

            content = _parse_gemini_response(response.text)

            logger.info(
                "Content generated successfully — title: '%s', diagrams: %d, quiz: %d",
                content.get("topic_title", "?"),
                len(content.get("diagrams", [])),
                len(content.get("quiz_questions", [])),
            )
            return content

        except (ValueError, json.JSONDecodeError) as exc:
            logger.warning("Parse error on attempt %d: %s", attempt, exc)
            last_error = exc

        except Exception as exc:
            logger.warning("Gemini API error on attempt %d: %s", attempt, exc)
            last_error = exc

        # Exponential back-off before retry
        if attempt < _MAX_RETRIES:
            delay = _RETRY_DELAY_BASE * (2 ** (attempt - 1))
            logger.info("Retrying in %d seconds...", delay)
            time.sleep(delay)

    # All retries exhausted
    error_msg = f"Content generation failed after {_MAX_RETRIES} attempts. Last error: {last_error}"
    logger.error(error_msg)
    raise RuntimeError(error_msg)
