from django import template
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()


@register.filter
def usd(value):
    if value is None or value == "":
        return "по запросу"
    try:
        number = int(value)
    except (TypeError, ValueError):
        return value
    formatted = intcomma(number).replace(",", " ")
    return f"$ {formatted}"


@register.filter
def rub_from_usd(value):
    try:
        number = int(value)
    except (TypeError, ValueError):
        return ""
    rub = int(round(number * settings.EXCHANGE_USD_RUB))
    formatted = intcomma(rub).replace(",", " ")
    return f"{formatted} ₽"


@register.filter
def spaceint(value):
    try:
        number = int(value)
    except (TypeError, ValueError):
        return value
    return intcomma(number).replace(",", " ")
