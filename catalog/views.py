from django.db.models import Q, QuerySet
from django.views.generic import DetailView, ListView

from leads.forms import LeadForm

from .models import Brand, Category, Vehicle


def _filtered_vehicles(request) -> QuerySet[Vehicle]:
    qs = Vehicle.objects.filter(is_published=True).select_related("brand", "category")
    brand = request.GET.get("brand")
    category = request.GET.get("type")
    condition = request.GET.get("condition")
    availability = request.GET.get("availability")
    price_min = request.GET.get("price_min")
    price_max = request.GET.get("price_max")
    q = request.GET.get("q")

    if brand:
        qs = qs.filter(brand__slug=brand)
    if category:
        qs = qs.filter(category__slug=category)
    if condition in {Vehicle.Condition.NEW, Vehicle.Condition.USED}:
        qs = qs.filter(condition=condition)
    if availability in {Vehicle.Availability.IN_STOCK, Vehicle.Availability.ON_ORDER}:
        qs = qs.filter(availability=availability)
    if price_min and price_min.isdigit():
        qs = qs.filter(price_usd__gte=int(price_min))
    if price_max and price_max.isdigit():
        qs = qs.filter(price_usd__lte=int(price_max))
    if q:
        qs = qs.filter(
            Q(name__icontains=q)
            | Q(short_specs__icontains=q)
            | Q(description__icontains=q)
            | Q(brand__name__icontains=q)
        )
    return qs


class CatalogListView(ListView):
    model = Vehicle
    template_name = "catalog/list.html"
    context_object_name = "vehicles"
    paginate_by = 12

    def get_queryset(self):
        return _filtered_vehicles(self.request)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
                "brands": Brand.objects.all(),
                "categories": Category.objects.all(),
                "filters": self.request.GET,
                "page_title": "Каталог коммерческой техники",
                "meta_title": "Каталог грузовиков и спецтехники — SPEC-KG, Бишкек",
                "meta_description": (
                    "Купить грузовик FAW, самосвал, шасси и спецтехнику в Кыргызстане. "
                    "Новые и проверенный б/у. Цены в USD, расчёт в рублях по запросу."
                ),
            }
        )
        brand = self.request.GET.get("brand")
        if brand == "faw":
            ctx["page_title"] = "Каталог FAW"
            ctx["meta_title"] = "FAW в наличии и под заказ — официальный дилер SPEC-KG"
            ctx["meta_description"] = (
                "Тягачи, самосвалы и шасси FAW Jiefang в Бишкеке. Официальный дилер, "
                "заводская гарантия, пакет под ключ с оформлением в КР."
            )
        return ctx


class VehicleDetailView(DetailView):
    model = Vehicle
    template_name = "catalog/detail.html"
    context_object_name = "vehicle"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Vehicle.objects.filter(is_published=True).select_related("brand", "category")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        vehicle: Vehicle = self.object
        similar = (
            Vehicle.objects.filter(is_published=True)
            .exclude(pk=vehicle.pk)
            .filter(Q(category=vehicle.category) | Q(brand=vehicle.brand))
            .select_related("brand", "category")[:4]
        )
        ctx.update(
            {
                "similar": similar,
                "lead_form": LeadForm(
                    initial={
                        "source": vehicle.name,
                        "comment": f"Запрос по технике: {vehicle.name}",
                    }
                ),
                "meta_title": f"{vehicle.name} — купить в Бишкеке | SPEC-KG",
                "meta_description": (
                    f"{vehicle.name}: {vehicle.short_specs or vehicle.category.name}. "
                    f"Цена ${vehicle.price_usd:,} USD. Оформление в Кыргызстане, пакет под ключ."
                ).replace(",", " "),
            }
        )
        return ctx
