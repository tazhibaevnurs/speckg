from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Brand(models.Model):
    name = models.CharField("Название", max_length=80)
    slug = models.SlugField("Слаг", unique=True, allow_unicode=True)
    is_flagship = models.BooleanField("Флагман (FAW)", default=False)
    short_description = models.CharField("Кратко", max_length=255, blank=True)
    sort_order = models.PositiveSmallIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"
        ordering = ["sort_order", "name"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField("Название", max_length=80)
    slug = models.SlugField("Слаг", unique=True, allow_unicode=True)
    sort_order = models.PositiveSmallIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Тип техники"
        verbose_name_plural = "Типы техники"
        ordering = ["sort_order", "name"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Vehicle(models.Model):
    class Condition(models.TextChoices):
        NEW = "new", "Новая"
        USED = "used", "Проверенный б/у"

    class Availability(models.TextChoices):
        IN_STOCK = "in_stock", "В наличии"
        ON_ORDER = "on_order", "Под заказ"

    brand = models.ForeignKey(
        Brand, verbose_name="Бренд", on_delete=models.PROTECT, related_name="vehicles"
    )
    category = models.ForeignKey(
        Category, verbose_name="Тип", on_delete=models.PROTECT, related_name="vehicles"
    )
    name = models.CharField("Название", max_length=180)
    slug = models.SlugField("Слаг", unique=True, allow_unicode=True, max_length=200)
    condition = models.CharField(
        "Состояние", max_length=12, choices=Condition.choices, default=Condition.NEW
    )
    availability = models.CharField(
        "Наличие", max_length=12, choices=Availability.choices, default=Availability.IN_STOCK
    )
    price_usd = models.PositiveIntegerField("Цена, USD")
    year = models.PositiveSmallIntegerField("Год", blank=True, null=True)
    mileage_km = models.PositiveIntegerField("Пробег, км", blank=True, null=True)
    power_hp = models.PositiveSmallIntegerField("Мощность, л.с.", blank=True, null=True)
    wheel_formula = models.CharField("Колёсная формула", max_length=16, blank=True)
    payload = models.CharField("Грузоподъёмность / ССУ", max_length=80, blank=True)
    engine = models.CharField("Двигатель", max_length=120, blank=True)
    gearbox = models.CharField("КПП", max_length=80, blank=True)
    fuel = models.CharField("Топливо", max_length=40, blank=True, default="Дизель")
    gvw = models.CharField("Полная масса", max_length=40, blank=True)
    short_specs = models.CharField("Краткие ТТХ (карточка)", max_length=220, blank=True)
    description = models.TextField("Описание", blank=True)
    extra_features = models.TextField("Дополнительно", blank=True)
    main_image = models.ImageField("Главное фото", upload_to="vehicles/", blank=True)
    use_placeholder = models.BooleanField(
        "Плейсхолдер «фото с площадки»",
        default=True,
        help_text="Показывает подпись, что фото с площадки появится позже.",
    )
    is_published = models.BooleanField("Опубликовано", default=True)
    is_featured = models.BooleanField("На главной", default=True)
    sort_order = models.PositiveSmallIntegerField("Порядок", default=0)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = "Единица техники"
        verbose_name_plural = "Техника"
        ordering = ["sort_order", "-created_at"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("catalog:detail", kwargs={"slug": self.slug})

    @property
    def condition_label(self) -> str:
        return self.get_condition_display()

    @property
    def availability_label(self) -> str:
        return self.get_availability_display()

    @property
    def mileage_display(self) -> str:
        if self.condition == self.Condition.NEW:
            return "Новая"
        if self.mileage_km is None:
            return "Пробег уточняется"
        return f"{self.mileage_km:,} км".replace(",", " ")


class VehicleImage(models.Model):
    vehicle = models.ForeignKey(
        Vehicle, verbose_name="Техника", on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField("Фото", upload_to="vehicles/gallery/")
    caption = models.CharField("Подпись", max_length=160, blank=True)
    sort_order = models.PositiveSmallIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Фото галереи"
        verbose_name_plural = "Галерея"
        ordering = ["sort_order", "id"]

    def __str__(self) -> str:
        return f"{self.vehicle.name} — фото {self.pk}"
