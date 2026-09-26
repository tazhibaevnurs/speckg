from django.db import models


class Lead(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Новая"
        IN_PROGRESS = "in_progress", "В работе"
        CLOSED = "closed", "Закрыта"

    class FormType(models.TextChoices):
        GENERAL = "general", "Оставить заявку"
        VEHICLE = "vehicle", "Запросить эту машину"
        CALCULATOR = "calculator", "Рассчитать выгоду"
        CALLBACK = "callback", "Заказать звонок"

    name = models.CharField("Имя", max_length=120)
    phone = models.CharField("Телефон", max_length=40)
    telegram = models.CharField("Telegram", max_length=80, blank=True)
    comment = models.TextField("Комментарий", blank=True)
    source = models.CharField(
        "Источник (техника / услуга)",
        max_length=255,
        blank=True,
        help_text="Какая машина или услуга интересует",
    )
    form_type = models.CharField(
        "Тип формы", max_length=20, choices=FormType.choices, default=FormType.GENERAL
    )
    status = models.CharField(
        "Статус", max_length=20, choices=Status.choices, default=Status.NEW
    )
    page_url = models.CharField("Страница", max_length=255, blank=True)
    extra = models.JSONField("Данные калькулятора", blank=True, null=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} · {self.get_form_type_display()} · {self.created_at:%d.%m.%Y %H:%M}"
