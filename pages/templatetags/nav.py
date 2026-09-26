from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def nav_active(context, url_name):
    request = context.get("request")
    if not request:
        return ""
    try:
        target = reverse(url_name)
    except Exception:
        return ""
    path = request.path
    if url_name == "pages:home":
        return "is-active" if path == "/" else ""
    return "is-active" if path == target or path.startswith(target) else ""
