from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .services import VEHICLE_TYPES, estimate


def _parse_float(value, default=0.0):
    if value is None or value == "":
        return default
    try:
        return float(str(value).replace(" ", "").replace(",", "."))
    except ValueError:
        return default


@require_GET
def calculate(request):
    vehicle_type = request.GET.get("type", "tractor")
    if vehicle_type not in dict(VEHICLE_TYPES):
        vehicle_type = "other"
    rf_price = _parse_float(request.GET.get("rf_price"))
    our_usd = _parse_float(request.GET.get("our_price_usd"), 0)
    result = estimate(vehicle_type, rf_price, our_usd)

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"ok": True, "result": result})

    return render(
        request,
        "calculator/result.html",
        {
            "result": result,
            "meta_title": "Ориентировочный расчёт — SPEC-KG",
        },
    )
