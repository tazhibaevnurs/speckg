from django.db import models


class Document(models.Model):
    title = models.CharField("Название", max_length=160)
    description = models.CharField("Подпись", max_length=255, blank=True)
    file = models.FileField("Файл", upload_to="documents/", blank=True)
    is_placeholder = models.BooleanField("Заглушка", default=True)
    sort_order = models.PositiveSmallIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
        ordering = ["sort_order", "id"]

    def __str__(self) -> str:
        return self.title


class FAQ(models.Model):
    question = models.CharField("Вопрос", max_length=255)
    answer = models.TextField("Ответ")
    sort_order = models.PositiveSmallIntegerField("Порядок", default=0)
    is_published = models.BooleanField("Опубликовано", default=True)

    class Meta:
        verbose_name = "Вопрос FAQ"
        verbose_name_plural = "FAQ"
        ordering = ["sort_order", "id"]

    def __str__(self) -> str:
        return self.question
