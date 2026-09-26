from django.shortcuts import render
from django.views.generic import TemplateView

from catalog.models import Vehicle
from leads.forms import LeadForm

from .models import Document, FAQ


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        vehicles = (
            Vehicle.objects.filter(is_published=True, is_featured=True)
            .select_related("brand", "category")[:8]
        )
        ctx.update(
            {
                "vehicles": vehicles,
                "lead_form": LeadForm(),
                "meta_title": "SPEC-KG — коммерческая техника из Кыргызстана для РФ и СНГ",
                "meta_description": (
                    "Официальный дилер FAW в Бишкеке. Купить грузовик и спецтехнику, "
                    "оформить на кыргызский учёт и получить пакет под ключ. Цена ниже "
                    "дилерской РФ, техника в наличии."
                ),
            }
        )
        return ctx


class FAWView(TemplateView):
    template_name = "pages/faw.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
                "faw_vehicles": Vehicle.objects.filter(
                    is_published=True, brand__slug="faw"
                ).select_related("brand", "category")[:8],
                "meta_title": "FAW Jiefang — официальный дилер SPEC-KG в Кыргызстане",
                "meta_description": (
                    "История FAW, линейки J6, JH6, JK6, J7, HanV, Tiger. "
                    "Официальные поставки через дилера SPEC-KG в Бишкеке, сервис и запчасти."
                ),
            }
        )
        return ctx


class WhyKGView(TemplateView):
    template_name = "pages/why_kg.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
                "meta_title": "Почему Кыргызстан — техника на кыргызских номерах | SPEC-KG",
                "meta_description": (
                    "Экономия за счёт оформления в Кыргызстане, цена ниже дилерской РФ, "
                    "ЕАЭС без таможенной границы, техника в наличии. Справочное сравнение, "
                    "не юридическая гарантия."
                ),
            }
        )
        return ctx


class ServicesView(TemplateView):
    template_name = "pages/services.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
                "meta_title": "Пакет под ключ — подбор, учёт КР, доставка | SPEC-KG",
                "meta_description": (
                    "Подбор техники, договор и оплата, регистрация в КР и кыргызские номера, "
                    "страховка, доставка в РФ или самовывоз в Бишкеке. Лизинг по запросу."
                ),
            }
        )
        return ctx


class AboutView(TemplateView):
    template_name = "pages/about.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
                "meta_title": "О компании SPEC-KG — Бишкек, официальный дилер FAW",
                "meta_description": (
                    "SPEC-KG в Бишкеке помогает гражданам и бизнесу РФ и клиентам КР "
                    "купить коммерческую и спецтехнику и оформить пакет под ключ."
                ),
            }
        )
        return ctx


class DocumentsView(TemplateView):
    template_name = "pages/documents.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
                "documents": Document.objects.all(),
                "meta_title": "Документы — SPEC-KG",
                "meta_description": "Документы компании SPEC-KG. Скан-копии будут загружены.",
            }
        )
        return ctx


class FAQView(TemplateView):
    template_name = "pages/faq.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
                "faqs": FAQ.objects.filter(is_published=True),
                "meta_title": "Вопросы и ответы — техника, учёт КР, доставка | SPEC-KG",
                "meta_description": (
                    "Утильсбор, кыргызские номера, доставка в РФ, сроки, б/у, юрлицо в КР, "
                    "гарантия FAW. Информационные ответы, не юридическая консультация."
                ),
            }
        )
        return ctx


class ContactsView(TemplateView):
    template_name = "pages/contacts.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
                "meta_title": "Контакты SPEC-KG — Бишкек, Кыргызстан",
                "meta_description": (
                    "Офис и склад в Бишкеке. Заявки в Telegram и WhatsApp ежедневно 24/7. "
                    "Представительства в РФ нет."
                ),
            }
        )
        return ctx


class PrivacyView(TemplateView):
    template_name = "pages/privacy.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
                "meta_title": "Политика конфиденциальности — SPEC-KG",
                "meta_description": "Как SPEC-KG обрабатывает заявки и контактные данные.",
            }
        )
        return ctx


def page_not_found(request, exception):
    return render(
        request,
        "pages/404.html",
        {"meta_title": "Страница не найдена — SPEC-KG"},
        status=404,
    )


def server_error(request):
    return render(
        request,
        "pages/500.html",
        {"meta_title": "Ошибка сервера — SPEC-KG"},
        status=500,
    )
