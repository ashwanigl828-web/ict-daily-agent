"""
ICT Daily Agent — WhatsApp Sender Agent
Handles uploading PDFs to Cloudinary and dispatching messages via the
WhatsApp Cloud API (Meta Graph API v21.0).
"""

import logging
from pathlib import Path
from typing import Optional

import cloudinary
import cloudinary.uploader
import requests

import config

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Cloudinary configuration (lazy — safe to call even if creds are empty)
# ---------------------------------------------------------------------------
cloudinary.config(
    cloud_name=config.CLOUDINARY_CLOUD_NAME,
    api_key=config.CLOUDINARY_API_KEY,
    api_secret=config.CLOUDINARY_API_SECRET,
    secure=True,
)


# ===================================================================
# PDF Upload
# ===================================================================

def upload_pdf_to_cloudinary(pdf_path: str) -> str:
    """Upload a PDF file to Cloudinary and return its public URL.

    Args:
        pdf_path: Absolute or relative path to the PDF file on disk.

    Returns:
        The secure URL of the uploaded PDF.

    Raises:
        FileNotFoundError: If the PDF file does not exist.
        RuntimeError: If the upload fails.
    """
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    logger.info("Uploading PDF to Cloudinary: %s", path.name)

    try:
        result = cloudinary.uploader.upload(
            str(path),
            resource_type="raw",
            folder="ict-daily-pdfs",
            public_id=path.stem,
            overwrite=True,
            invalidate=True,
        )
        url: str = result["secure_url"]
        logger.info("PDF uploaded successfully: %s", url)
        return url

    except Exception as exc:
        logger.error("Cloudinary upload failed: %s", exc)
        raise RuntimeError(f"Cloudinary upload failed: {exc}") from exc


# ===================================================================
# WhatsApp helpers
# ===================================================================

def _whatsapp_headers() -> dict[str, str]:
    """Return standard headers for WhatsApp API calls."""
    return {
        "Authorization": f"Bearer {config.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }


def _post_whatsapp(payload: dict) -> dict:
    """Send a POST request to the WhatsApp messages endpoint.

    Args:
        payload: JSON-serialisable request body.

    Returns:
        Parsed JSON response from the API.

    Raises:
        RuntimeError: If the API returns a non-2xx status or network error.
    """
    if not config.WHATSAPP_ACCESS_TOKEN:
        logger.error("WHATSAPP_ACCESS_TOKEN is not configured.")
        raise RuntimeError("WhatsApp access token is missing.")

    if not config.WHATSAPP_PHONE_NUMBER_ID:
        logger.error("WHATSAPP_PHONE_NUMBER_ID is not configured.")
        raise RuntimeError("WhatsApp phone number ID is missing.")

    try:
        resp = requests.post(
            config.WHATSAPP_API_URL,
            headers=_whatsapp_headers(),
            json=payload,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        logger.debug("WhatsApp API response: %s", data)
        return data

    except requests.exceptions.HTTPError as exc:
        error_body = exc.response.text if exc.response is not None else "no body"
        logger.error("WhatsApp API HTTP error (%s): %s", exc.response.status_code, error_body)
        return {"error": True, "status_code": getattr(exc.response, "status_code", None), "detail": error_body}

    except requests.exceptions.RequestException as exc:
        logger.error("WhatsApp API request failed: %s", exc)
        return {"error": True, "detail": str(exc)}


# ===================================================================
# Public API
# ===================================================================

def send_document(
    phone_number: str,
    document_url: str,
    filename: str,
    caption: str,
) -> dict:
    """Send a document (PDF) via WhatsApp Cloud API.

    Args:
        phone_number: Recipient phone in international format (e.g. "919876543210").
        document_url: Publicly accessible URL of the document.
        filename: Display filename for the recipient.
        caption: Short caption text shown with the document.

    Returns:
        API response dict. Contains 'error' key on failure.
    """
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": phone_number,
        "type": "document",
        "document": {
            "link": document_url,
            "filename": filename,
            "caption": caption,
        },
    }
    logger.info("Sending document to %s — %s", phone_number, filename)
    return _post_whatsapp(payload)


def send_text_message(phone_number: str, message: str) -> dict:
    """Send a plain-text WhatsApp message.

    Args:
        phone_number: Recipient phone in international format.
        message: The text body.

    Returns:
        API response dict.
    """
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": phone_number,
        "type": "text",
        "text": {"preview_url": False, "body": message},
    }
    logger.info("Sending text message to %s", phone_number)
    return _post_whatsapp(payload)


def send_to_class(
    class_standard: str,
    pdf_url: str,
    topic_name: str,
    response_link: str,
) -> list[dict]:
    """Send the daily PDF to every student registered in a class.

    Args:
        class_standard: Class number ("8"–"12").
        pdf_url: Public URL of the PDF.
        topic_name: Topic name for the caption.
        response_link: URL where students submit feedback.

    Returns:
        List of per-number result dicts (one per student).
    """
    numbers = config.WHATSAPP_CLASS_NUMBERS.get(class_standard, [])

    if not numbers:
        logger.warning("No phone numbers configured for class %s", class_standard)
        return []

    theme = config.CLASS_THEMES.get(class_standard, {})
    class_label = theme.get("name", f"कक्षा {class_standard}")
    emoji = theme.get("emoji", "📚")

    caption = (
        f"{emoji} *{class_label} — आज का ICT टॉपिक* {emoji}\n\n"
        f"📖 *विषय:* {topic_name}\n\n"
        f"PDF पढ़ें और नीचे दिए लिंक पर अपना जवाब दें:\n"
        f"🔗 {response_link}\n\n"
        f"— आपके शिक्षक 🙏"
    )

    filename = f"ICT_{class_label}_{topic_name[:30]}.pdf"

    results: list[dict] = []
    success_count = 0
    fail_count = 0

    for number in numbers:
        result = send_document(
            phone_number=number,
            document_url=pdf_url,
            filename=filename,
            caption=caption,
        )
        result["phone_number"] = number

        if result.get("error"):
            fail_count += 1
        else:
            success_count += 1

        results.append(result)

    logger.info(
        "Class %s send complete — %d success, %d failed out of %d",
        class_standard,
        success_count,
        fail_count,
        len(numbers),
    )
    return results


def send_teacher_summary(summary_text: str) -> dict:
    """Send a daily summary text message to the teacher.

    Args:
        summary_text: The summary message body.

    Returns:
        API response dict.
    """
    teacher_phone = config.TEACHER_PHONE
    if not teacher_phone:
        logger.warning("TEACHER_PHONE not configured. Cannot send summary.")
        return {"error": True, "detail": "Teacher phone not configured"}

    logger.info("Sending daily summary to teacher (%s)", teacher_phone)
    return send_text_message(teacher_phone, summary_text)
