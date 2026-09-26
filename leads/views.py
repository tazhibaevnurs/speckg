import json
import logging

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from .forms import LeadForm
from .models import Lead
from .notify import notify_telegram

logger = logging.getLogger("leads")


@require_POST
def create_lead(request):
    form = LeadForm(request.POST)
    wants_json = request.headers.get("X-Requested-With") == "XMLHttpRequest"

    if not form.is_valid():
        # Honeypot: pretend success so bots don't retry
        if form.data.get("website"):
            if wants_json:
                return JsonResponse({"ok": True})
            messages.success(request, "Заявка отправлена. Свяжемся в мессенджере.")
            return redirect(request.POST.get("next") or "/")
        if wants_json:
            return JsonResponse({"ok": False, "errors": form.errors}, status=400)
        messages.error(request, "Проверьте имя и телефон — заявка не отправлена.")
        return redirect(request.POST.get("next") or "/")

    lead: Lead = form.save(commit=False)
    lead.page_url = request.POST.get("page_url") or request.META.get("HTTP_REFERER", "")
    extra_raw = request.POST.get("extra_json", "").strip()
    if extra_raw:
        try:
            lead.extra = json.loads(extra_raw)
        except json.JSONDecodeError:
            lead.extra = {"raw": extra_raw}
    if not lead.form_type:
        lead.form_type = Lead.FormType.GENERAL
    lead.save()
    try:
        notify_telegram(lead)
    except Exception:
        logger.exception("Notify failed, lead #%s is still saved", lead.pk)

    if wants_json:
        return JsonResponse({"ok": True, "message": "Заявка принята. Напишем в Telegram или WhatsApp."})
    messages.success(request, "Заявка принята. Напишем в Telegram или WhatsApp.")
    return redirect(request.POST.get("next") or "/")
