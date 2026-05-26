"""
ICT Daily Agent — PDF Generator Agent
Beautiful Hindi PDF generation using WeasyPrint (HTML → PDF).
Class-wise color themes, QR codes, engaging layout.
"""

import base64
import io
import logging
from datetime import date
from pathlib import Path
from typing import Optional

import qrcode
from jinja2 import Template

import config

logger = logging.getLogger(__name__)


# Hindi month names for date formatting
HINDI_MONTHS = {
    1: "जनवरी", 2: "फ़रवरी", 3: "मार्च", 4: "अप्रैल",
    5: "मई", 6: "जून", 7: "जुलाई", 8: "अगस्त",
    9: "सितंबर", 10: "अक्टूबर", 11: "नवंबर", 12: "दिसंबर",
}


def _get_hindi_date(d: date | None = None) -> str:
    """Convert a date to Hindi format like '25 मई 2025'."""
    d = d or date.today()
    month_name = HINDI_MONTHS.get(d.month, str(d.month))
    return f"{d.day} {month_name} {d.year}"


def _generate_qr_code(url: str) -> str:
    """Generate a QR code image as base64 string."""
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=8,
            border=2,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="#333333", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode("utf-8")
        return f"data:image/png;base64,{img_base64}"
    except Exception as e:
        logger.error(f"QR code generation failed: {e}")
        return ""


def _format_main_content(raw_content: str) -> str:
    """
    Format the raw main content from Gemini into HTML.
    Handles markdown-like formatting in Hindi text.
    """
    if not raw_content:
        return "<p>कोई सामग्री उपलब्ध नहीं है।</p>"

    html_lines = []
    lines = raw_content.split("\n")

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Headings
        if line.startswith("### "):
            html_lines.append(f'<h4 class="sub-heading">{line[4:]}</h4>')
        elif line.startswith("## "):
            html_lines.append(f'<h3 class="sub-heading">{line[3:]}</h3>')
        elif line.startswith("# "):
            html_lines.append(f'<h2 class="sub-heading">{line[2:]}</h2>')
        # Bold text
        elif line.startswith("**") and line.endswith("**"):
            html_lines.append(f'<p class="highlight-text"><strong>{line[2:-2]}</strong></p>')
        # Bullet points
        elif line.startswith("- ") or line.startswith("• "):
            bullet_text = line[2:]
            html_lines.append(f'<div class="bullet-point">● {bullet_text}</div>')
        elif line.startswith("* "):
            bullet_text = line[2:]
            html_lines.append(f'<div class="bullet-point">● {bullet_text}</div>')
        # Numbered items
        elif len(line) > 2 and line[0].isdigit() and line[1] in ".)" :
            html_lines.append(f'<div class="numbered-point">{line}</div>')
        # Definition boxes (lines with : separator)
        elif " : " in line and len(line) < 200:
            parts = line.split(" : ", 1)
            html_lines.append(
                f'<div class="definition-box">'
                f'<span class="def-term">{parts[0]}</span>'
                f'<span class="def-desc">{parts[1]}</span>'
                f'</div>'
            )
        # Regular paragraph
        else:
            # Handle inline bold
            import re
            formatted = re.sub(
                r'\*\*(.*?)\*\*',
                r'<strong class="key-term">\1</strong>',
                line
            )
            html_lines.append(f"<p>{formatted}</p>")

    return "\n".join(html_lines)


def create_pdf(
    content: dict,
    class_standard: str,
    topic_name: str,
    part_number: int = 1,
    total_parts: int = 1,
) -> Optional[Path]:
    """
    Create a beautiful, colorful Hindi PDF for the given content.

    Args:
        content: Dict from content_generator with keys:
            topic_title, introduction, main_content, diagrams,
            fun_facts, quiz_questions, summary
        class_standard: Class like "8", "9", etc.
        topic_name: Topic name for filename
        part_number: Current part number
        total_parts: Total parts of the topic

    Returns:
        Path to the generated PDF file, or None on failure.
    """
    try:
        # Get class theme
        theme = config.CLASS_THEMES.get(class_standard, config.CLASS_THEMES["8"])

        # Format date in Hindi
        date_str = _get_hindi_date()

        # Part info
        part_info = f"भाग {part_number}/{total_parts}" if total_parts > 1 else ""

        # Generate response form URL and QR code
        response_url = f"{config.APP_BASE_URL}/form/{class_standard}/{date.today().isoformat()}"
        qr_code_base64 = _generate_qr_code(response_url)

        # Format main content as HTML
        main_content_html = _format_main_content(content.get("main_content", ""))

        # Prepare template variables
        template_vars = {
            "topic_title": content.get("topic_title", topic_name),
            "class_standard": class_standard,
            "class_name": theme["name"],
            "date_str": date_str,
            "introduction": content.get("introduction", ""),
            "main_content": main_content_html,
            "diagrams": content.get("diagrams", []),
            "fun_facts": content.get("fun_facts", []),
            "quiz_questions": content.get("quiz_questions", []),
            "summary_points": content.get("summary", []),
            "qr_code_base64": qr_code_base64,
            "response_url": response_url,
            "part_info": part_info,
            "theme": theme,
        }

        # Load and render HTML template
        template_path = config.TEMPLATES_DIR / "pdf_template.html"
        if not template_path.exists():
            logger.error(f"PDF template not found at {template_path}")
            return None

        with open(template_path, "r", encoding="utf-8") as f:
            template_str = f.read()

        template = Template(template_str)
        rendered_html = template.render(**template_vars)

        # Generate PDF using WeasyPrint
        from weasyprint import HTML

        # Create output filename
        safe_topic = topic_name.replace(" ", "_").replace("/", "-")[:50]
        date_stamp = date.today().strftime("%Y%m%d")
        filename = f"class{class_standard}_{date_stamp}_{safe_topic}"
        if total_parts > 1:
            filename += f"_part{part_number}"
        filename += ".pdf"

        output_path = config.OUTPUT_DIR / filename

        # Generate the PDF
        logger.info(f"Generating PDF: {filename}")
        html_doc = HTML(
            string=rendered_html,
            base_url=str(config.BASE_DIR),
        )
        html_doc.write_pdf(str(output_path))

        file_size_kb = output_path.stat().st_size / 1024
        logger.info(f"✅ PDF generated successfully: {filename} ({file_size_kb:.1f} KB)")

        return output_path

    except ImportError as e:
        logger.error(
            f"WeasyPrint not installed or missing system dependencies: {e}. "
            f"Install with: pip install weasyprint"
        )
        return None
    except Exception as e:
        logger.error(f"PDF generation failed: {e}", exc_info=True)
        return None


def create_test_pdf(class_standard: str = "8") -> Optional[Path]:
    """
    Create a test PDF with sample content for verification.
    Useful for testing the PDF template without calling Gemini API.
    """
    sample_content = {
        "topic_title": "कंप्यूटर क्या है? 🖥️",
        "introduction": (
            "क्या आपने कभी सोचा है कि कंप्यूटर कैसे काम करता है? "
            "आज हम इस अद्भुत मशीन के बारे में जानेंगे जो हमारी दुनिया बदल रही है! "
            "कंप्यूटर एक ऐसी इलेक्ट्रॉनिक मशीन है जो डेटा को प्रोसेस करके "
            "उपयोगी जानकारी में बदलती है। 🚀"
        ),
        "main_content": (
            "## कंप्यूटर की परिभाषा\n\n"
            "**कंप्यूटर** एक इलेक्ट्रॉनिक उपकरण है जो डेटा (Input) को लेकर "
            "उसे प्रोसेस करता है और परिणाम (Output) देता है।\n\n"
            "कंप्यूटर शब्द अंग्रेज़ी के **'Compute'** शब्द से बना है "
            "जिसका अर्थ है **'गणना करना'**। इसीलिए इसे हिंदी में "
            "**'संगणक'** भी कहते हैं।\n\n"
            "## कंप्यूटर के मुख्य भाग\n\n"
            "- **CPU (सेंट्रल प्रोसेसिंग यूनिट)** : कंप्यूटर का दिमाग, सारी गणना यहीं होती है\n"
            "- **मॉनिटर** : स्क्रीन जिस पर हम सब कुछ देखते हैं\n"
            "- **कीबोर्ड** : टाइप करने के लिए, जैसे मोबाइल का कीबोर्ड\n"
            "- **माउस** : स्क्रीन पर चीज़ों को क्लिक करने के लिए\n"
            "- **RAM (रैम)** : अस्थायी मेमोरी, जो काम करते समय डेटा रखती है\n"
            "- **हार्ड डिस्क** : स्थायी मेमोरी, जहाँ सब फाइलें सेव होती हैं\n\n"
            "## कंप्यूटर कैसे काम करता है?\n\n"
            "कंप्यूटर **IPO (Input → Process → Output)** सिद्धांत पर काम करता है:\n\n"
            "1. **Input** : हम कीबोर्ड या माउस से डेटा देते हैं\n"
            "2. **Process** : CPU डेटा पर गणना करता है\n"
            "3. **Output** : परिणाम मॉनिटर या प्रिंटर पर दिखता है\n\n"
            "जैसे आप **Calculator** में 2+3 टाइप करते हैं (Input), "
            "कंप्यूटर जोड़ता है (Process), और 5 दिखाता है (Output)! ✨"
        ),
        "diagrams": [
            '<svg width="400" height="200" xmlns="http://www.w3.org/2000/svg">'
            '<rect x="10" y="80" width="100" height="50" rx="10" fill="#4CAF50" />'
            '<text x="60" y="110" text-anchor="middle" fill="white" font-size="14" font-family="sans-serif">Input</text>'
            '<rect x="150" y="80" width="100" height="50" rx="10" fill="#2196F3" />'
            '<text x="200" y="110" text-anchor="middle" fill="white" font-size="14" font-family="sans-serif">Process</text>'
            '<rect x="290" y="80" width="100" height="50" rx="10" fill="#FF9800" />'
            '<text x="340" y="110" text-anchor="middle" fill="white" font-size="14" font-family="sans-serif">Output</text>'
            '<line x1="110" y1="105" x2="150" y2="105" stroke="#333" stroke-width="2" marker-end="url(#arrow)"/>'
            '<line x1="250" y1="105" x2="290" y2="105" stroke="#333" stroke-width="2" marker-end="url(#arrow)"/>'
            '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
            '<path d="M 0 0 L 10 5 L 0 10 z" fill="#333"/></marker></defs>'
            '<text x="200" y="30" text-anchor="middle" fill="#333" font-size="16" font-weight="bold">IPO सिद्धांत</text>'
            '</svg>'
        ],
        "fun_facts": [
            "🌍 दुनिया का पहला कंप्यूटर ENIAC था जो 1946 में बना — यह एक पूरे कमरे जितना बड़ा था!",
            "⚡ आपका स्मार्टफोन NASA के उन कंप्यूटरों से ज़्यादा powerful है जिन्होंने इंसान को चाँद पर भेजा था!",
            "🇮🇳 भारत का पहला सुपरकंप्यूटर 'PARAM 8000' था जो 1991 में बना था।",
            "💻 'Bug' शब्द तब आया जब एक असली कीड़ा (moth) कंप्यूटर में फँस गया था!",
        ],
        "quiz_questions": [
            {
                "question": "कंप्यूटर शब्द किस अंग्रेज़ी शब्द से बना है?",
                "options": ["Computer", "Compute", "Count", "Calculate"],
                "correct_answer": "Compute",
            },
            {
                "question": "CPU का पूरा नाम क्या है?",
                "options": [
                    "Central Processing Unit",
                    "Computer Personal Unit",
                    "Central Program Utility",
                    "Core Processing Unit",
                ],
                "correct_answer": "Central Processing Unit",
            },
            {
                "question": "कंप्यूटर किस सिद्धांत पर काम करता है?",
                "options": ["ABC", "IPO", "XYZ", "CPU"],
                "correct_answer": "IPO",
            },
        ],
        "summary": [
            "कंप्यूटर एक इलेक्ट्रॉनिक मशीन है जो डेटा को प्रोसेस करती है",
            "कंप्यूटर IPO (Input → Process → Output) सिद्धांत पर काम करता है",
            "CPU कंप्यूटर का दिमाग है जो सारी गणना करता है",
            "कंप्यूटर को हिंदी में 'संगणक' कहते हैं",
        ],
    }

    return create_pdf(
        content=sample_content,
        class_standard=class_standard,
        topic_name="कंप्यूटर_क्या_है",
    )
