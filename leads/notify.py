import logging

import requests
from django.conf import settings

from .models import Lead

logger = logging.getLogger("leads")


def format_lead_message(lead: Lead) -> str:
    extra_lines = ""
    if lead.extra:
        extra_lines = "\n".join(f"{k}: {v}" for k, v in lead.extra.items())
        extra_lines = f"\n\n{extra_lines}"
    return (
        f"Новая заявка SPEC-KG\n"
        f"Тип: {lead.get_form_type_display()}\n"
        f"Имя: {lead.name}\n"
        f"Телефон: {lead.phone}\n"
        f"Telegram: {lead.telegram or '—'}\n"
        f"Источник: {lead.source or '—'}\n"
        f"Страница: {lead.page_url or '—'}\n"
        f"Комментарий: {lead.comment or '—'}"
        f"{extra_lines}"
    )


def notify_telegram(lead: Lead) -> None:
    """Send lead to Telegram. If token is missing, log and keep the UI working."""
    text = format_lead_message(lead)
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    if not token or not chat_id:
        logger.info("Telegram is not configured. Lead #%s saved:\n%s", lead.pk, text)
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        response = requests.post(
            url,
            json={"chat_id": chat_id, "text": text},
            timeout=8,
        )
        if not response.ok:
            logger.warning("Telegram API %s: %s", response.status_code, response.text[:300])
    except requests.RequestException:
        logger.exception("Telegram notify failed for lead #%s", lead.pk)
