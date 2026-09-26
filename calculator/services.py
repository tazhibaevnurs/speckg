from django.conf import settings


VEHICLE_TYPES = (
    ("tractor", "Тягач"),
    ("dump", "Самосвал"),
    ("chassis", "Шасси"),
    ("other", "Другое"),
)


def estimate(vehicle_type: str, rf_price_rub: float, our_price_usd: float) -> dict:
    rate = settings.EXCHANGE_USD_RUB
    util = settings.UTIL_FEE_RUB.get(vehicle_type, settings.UTIL_FEE_RUB["other"])
    our_rub = round(our_price_usd * rate)
    delta = round(rf_price_rub - our_rub) if rf_price_rub else None
    return {
        "vehicle_type": vehicle_type,
        "vehicle_type_label": dict(VEHICLE_TYPES).get(vehicle_type, "Другое"),
        "rf_price_rub": int(rf_price_rub) if rf_price_rub else None,
        "our_price_usd": int(our_price_usd),
        "our_price_rub": our_rub,
        "rate": rate,
        "util_fee_rub": util,
        "delta_rub": delta,
    }
