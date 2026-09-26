import json

from django.conf import settings


def site_context(request):
    return {
        "site_name": settings.SITE_NAME,
        "site_url": settings.SITE_URL,
        "util_fee_json": json.dumps(settings.UTIL_FEE_RUB),
        "contact_phone": settings.CONTACT_PHONE,
        "contact_phone_tel": settings.CONTACT_PHONE_TEL,
        "contact_whatsapp": settings.CONTACT_WHATSAPP,
        "whatsapp_url": settings.WHATSAPP_URL,
        "contact_telegram": settings.CONTACT_TELEGRAM,
        "contact_telegram_url": settings.CONTACT_TELEGRAM_URL,
        "contact_email": settings.CONTACT_EMAIL,
        "contact_city": settings.CONTACT_CITY,
        "exchange_usd_rub": settings.EXCHANGE_USD_RUB,
        "legal_disclaimer": settings.LEGAL_DISCLAIMER,
        "nav_items": [
            ("pages:home", "Главная"),
            ("catalog:list", "Каталог"),
            ("pages:faw", "FAW"),
            ("pages:why_kg", "Почему Кыргызстан"),
            ("pages:services", "Услуги"),
            ("pages:about", "О компании"),
            ("pages:faq", "FAQ"),
            ("pages:contacts", "Контакты"),
        ],
    }
