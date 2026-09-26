from pathlib import Path

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction

from catalog.models import Brand, Category, Vehicle
from pages.models import Document, FAQ


VEHICLES = [
    {
        "brand": "faw",
        "category": "tyagachi",
        "name": "FAW J7 4×2 седельный тягач",
        "slug": "faw-j7-4x2-tyagach",
        "condition": Vehicle.Condition.NEW,
        "availability": Vehicle.Availability.IN_STOCK,
        "price_usd": 68500,
        "year": 2025,
        "mileage_km": 0,
        "power_hp": 460,
        "wheel_formula": "4×2",
        "payload": "ССУ до 40 т",
        "engine": "FAW CA6DM2, 11 л",
        "gearbox": "12 ст. ZF-тип",
        "fuel": "Дизель",
        "gvw": "18 т / автопоезд 40 т",
        "short_specs": "2025 · 460 л.с. · 4×2 · новая",
        "description": (
            "Флагманская линейка FAW Jiefang J7 — магистральный тягач под СНГ: "
            "кабина с высокой крышей, пневмоподвеска, подготовка под зимнюю эксплуатацию. "
            "Поставляется официально через SPEC-KG в Бишкеке. Подходит перевозчикам РФ и КР, "
            "которым нужна машина в наличии без дилерской очереди 3–6 месяцев."
        ),
        "extra_features": "Спальник · ретардер · круиз · подготовка под РФ/КР климат",
        "sort_order": 1,
        "stock_file": "catalog-faw-j7.jpg",
    },
    {
        "brand": "faw",
        "category": "samosvaly",
        "name": "FAW JH6 6×4 самосвал",
        "slug": "faw-jh6-6x4-samosval",
        "condition": Vehicle.Condition.NEW,
        "availability": Vehicle.Availability.IN_STOCK,
        "price_usd": 61200,
        "year": 2025,
        "mileage_km": 0,
        "power_hp": 420,
        "wheel_formula": "6×4",
        "payload": "25 т",
        "engine": "FAW CA6DM2",
        "gearbox": "10 ст. механическая",
        "fuel": "Дизель",
        "gvw": "32 т",
        "short_specs": "2025 · 420 л.с. · 6×4 · 25 т",
        "description": (
            "Самосвал JH6 — рабочая лошадка карьера и стройки. Надстройка под объём кузова "
            "согласовывается при заказе. Официальная поставка FAW, сервис и запчасти через дилера в КР."
        ),
        "extra_features": "Кузов 16–20 м³ · обогрев кузова · блокировка дифференциала",
        "sort_order": 2,
        "stock_file": "catalog-faw-dump.jpg",
    },
    {
        "brand": "faw",
        "category": "shassi",
        "name": "FAW J6P 6×4 шасси под надстройку",
        "slug": "faw-j6p-6x4-shassi",
        "condition": Vehicle.Condition.NEW,
        "availability": Vehicle.Availability.ON_ORDER,
        "price_usd": 47800,
        "year": 2025,
        "mileage_km": 0,
        "power_hp": 375,
        "wheel_formula": "6×4",
        "payload": "до 20 т на шасси",
        "engine": "FAW CA6DL1",
        "gearbox": "9 ст. механическая",
        "fuel": "Дизель",
        "gvw": "25 т",
        "short_specs": "2025 · 375 л.с. · шасси 6×4",
        "description": (
            "Универсальное шасси J6 под самосвал, реф, автовоз, цистерну или КМУ. "
            "Надстройку собираем под задачу — не «серый» импорт, а официальный канал FAW."
        ),
        "extra_features": "Колёсная база под разные надстройки · подготовка электропроводки",
        "sort_order": 3,
        "stock_file": "catalog-faw-chassis.jpg",
    },
    {
        "brand": "faw",
        "category": "furgony",
        "name": "FAW JK6 изотермический фургон",
        "slug": "faw-jk6-izotermicheskiy-furgon",
        "condition": Vehicle.Condition.NEW,
        "availability": Vehicle.Availability.IN_STOCK,
        "price_usd": 42900,
        "year": 2025,
        "mileage_km": 0,
        "power_hp": 190,
        "wheel_formula": "4×2",
        "payload": "5–8 т",
        "engine": "FAW CA4DK",
        "gearbox": "6 ст. механическая",
        "fuel": "Дизель",
        "gvw": "12 т",
        "short_specs": "2025 · 190 л.с. · изотерма 50 м³",
        "description": (
            "Среднетоннажник JK6 под городскую и межгородскую развозку. "
            "Изотерма или реф — по запросу. Удобен ИП и компаниям с коротким плечом."
        ),
        "extra_features": "Фургон ~50 м³ · гидроборт опционально · кондиционер",
        "sort_order": 4,
        "stock_file": "catalog-faw-van.jpg",
    },
    {
        "brand": "shacman",
        "category": "tyagachi",
        "name": "Shacman X3000 6×4 тягач",
        "slug": "shacman-x3000-6x4-tyagach",
        "condition": Vehicle.Condition.NEW,
        "availability": Vehicle.Availability.IN_STOCK,
        "price_usd": 57200,
        "year": 2024,
        "mileage_km": 0,
        "power_hp": 430,
        "wheel_formula": "6×4",
        "payload": "автопоезд до 60 т",
        "engine": "Weichai WP12",
        "gearbox": "12 ст. Fast Gear",
        "fuel": "Дизель",
        "gvw": "25 т",
        "short_specs": "2024 · 430 л.с. · 6×4 · Weichai",
        "description": (
            "Китайский магистральный 6×4 для тяжёлых направлений. В наличии на площадке в Бишкеке. "
            "Оформление на кыргызский учёт и пакет под ключ — как у остального парка SPEC-KG."
        ),
        "extra_features": "Высокая кабина · автономный отопитель · ретардер",
        "sort_order": 5,
        "stock_file": "catalog-shacman.jpg",
    },
    {
        "brand": "howo",
        "category": "samosvaly",
        "name": "Howo T5G 6×4 самосвал, проверенный б/у",
        "slug": "howo-t5g-6x4-samosval-bu",
        "condition": Vehicle.Condition.USED,
        "availability": Vehicle.Availability.IN_STOCK,
        "price_usd": 36500,
        "year": 2021,
        "mileage_km": 142000,
        "power_hp": 380,
        "wheel_formula": "6×4",
        "payload": "25 т",
        "engine": "Sinotruk MC11",
        "gearbox": "HW19710",
        "fuel": "Дизель",
        "gvw": "32 т",
        "short_specs": "2021 · 142 тыс. км · 380 л.с. · 6×4",
        "description": (
            "Проверенный б/у с площадки в Бишкеке: осмотр ходовой, рамы и кузова до сделки. "
            "VIN и госномер не публикуем как реквизиты сделки — детали по конкретной машине отправим в мессенджер."
        ),
        "extra_features": "Кузов 18 м³ · предпусковой подогреватель · история обслуживания по запросу",
        "sort_order": 6,
        "stock_file": "catalog-howo.jpg",
    },
    {
        "brand": "sany",
        "category": "spec",
        "name": "Гусеничный экскаватор 20–22 т",
        "slug": "ekskavator-gusenichnyy-20t",
        "condition": Vehicle.Condition.NEW,
        "availability": Vehicle.Availability.ON_ORDER,
        "price_usd": 54800,
        "year": 2025,
        "mileage_km": 0,
        "power_hp": 163,
        "wheel_formula": "гусеницы",
        "payload": "ковш 0,9–1,1 м³",
        "engine": "Cummins-тип, рядный",
        "gearbox": "гидростатика",
        "fuel": "Дизель",
        "gvw": "21,5 т",
        "short_specs": "класс 20–22 т · ковш ~1 м³ · под заказ",
        "description": (
            "Строительная спецтехника под запрос: экскаваторы, погрузчики, тракторы. "
            "Марка и комплектация фиксируются в договоре. Не серийный «чужой» VIN — машина подбирается клиенту."
        ),
        "extra_features": "Молоток / узкий ковш опционально · доставка на объект КР или в РФ",
        "sort_order": 7,
        "stock_file": "catalog-excavator.jpg",
    },
    {
        "brand": "xcmg",
        "category": "spec",
        "name": "Фронтальный погрузчик 5 т",
        "slug": "frontalnyy-pogruzchik-5t",
        "condition": Vehicle.Condition.NEW,
        "availability": Vehicle.Availability.IN_STOCK,
        "price_usd": 41200,
        "year": 2025,
        "mileage_km": 0,
        "power_hp": 162,
        "wheel_formula": "4×4",
        "payload": "5 т / ковш 3 м³",
        "engine": "Weichai",
        "gearbox": "гидромеханическая",
        "fuel": "Дизель",
        "gvw": "16,5 т",
        "short_specs": "5 т · ковш 3 м³ · 162 л.с.",
        "description": (
            "Погрузчик для склада инертных, карьера и площадки. В наличии ориентировочная единица — "
            "точную комплектацию подтвердит менеджер."
        ),
        "extra_features": "Кондиционер · быстросъём · джойстик",
        "sort_order": 8,
        "stock_file": "catalog-loader.jpg",
    },
]

BRANDS = [
    ("FAW", "faw", True, "Официальный дилер в КР. Флагман каталога.", 1),
    ("Shacman", "shacman", False, "Китайские тягачи и самосвалы под запрос и в наличии.", 2),
    ("Howo", "howo", False, "Sinotruk: самосвалы и шасси, в том числе проверенный б/у.", 3),
    ("SANY", "sany", False, "Строительная спецтехника под запрос.", 4),
    ("XCMG", "xcmg", False, "Погрузчики и строительная техника.", 5),
    ("JAC", "jac", False, "Среднетоннажники и коммерция под запрос.", 6),
    ("Dongfeng", "dongfeng", False, "Коммерческая техника под запрос.", 7),
]

CATEGORIES = [
    ("Тягачи", "tyagachi", 1),
    ("Самосвалы", "samosvaly", 2),
    ("Шасси", "shassi", 3),
    ("Фургоны и рефы", "furgony", 4),
    ("Автовозы", "avtovozy", 5),
    ("Цистерны", "cisterny", 6),
    ("КМУ", "kmu", 7),
    ("Автобусы", "avtobusy", 8),
    ("Спецтехника", "spec", 9),
]

DOCUMENTS = [
    ("Свидетельство о регистрации", "Юридический документ компании. Будет загружен."),
    ("Дилерский сертификат FAW", "Подтверждение официального дилерства. Документ будет загружен."),
    ("Образец договора купли-продажи", "Типовая форма. Не оферта, согласовывается индивидуально."),
    ("Образец документов учёта КР", "Пример комплекта постановки на учёт. Не публичная копия чужого учёта."),
]

FAQS = [
    (
        "Что с утильсбором РФ, если техника на кыргызском учёте?",
        "При оформлении и эксплуатации на регистрации Кыргызстана российский коммерческий "
        "утильсбор, который возникает при постановке на учёт в РФ, не начисляется. Это не «обход "
        "налогов» и не гарантия для любой ситуации: если вы позже ставите машину на учёт в России, "
        "применяются правила РФ. Итог зависит от статуса клиента и актуального законодательства. "
        "SPEC-KG не даёт юридическую консультацию.",
    ),
    (
        "Можно ли ездить по России на кыргызских номерах?",
        "КР и РФ входят в ЕАЭС: коммерческая техника перемещается между странами союза без "
        "таможенной границы как внутри союза. Режим эксплуатации, срок пребывания и налоговые "
        "последствия зависят от того, кто собственник, есть ли перевозчик в КР, и от действующих "
        "правил. Мы не обещаем, что «ездишь как на российских номерах». Схему согласуем под вас.",
    ),
    (
        "Как устроена доставка в РФ?",
        "Два базовых варианта: самовывоз со склада в Бишкеке или доставка в согласованный город РФ "
        "своим ходом / тралом — в составе пакета под ключ. Маршрут, страховка на перевозку и сроки "
        "считаются отдельно. Онлайн-оплаты на сайте нет: договор и расчёт — с менеджером.",
    ),
    (
        "Сколько занимает сделка?",
        "Если машина в наличии, подбор и договор занимают дни, не месяцы. Регистрация в КР и "
        "комплект «номера + страховка» зависят от готовности документов клиента и загрузки служб. "
        "Под заказ из КНР срок короче типичной очереди дилера РФ 3–6 месяцев — точную вилку скажем "
        "по конкретной модели.",
    ),
    (
        "Берёте ли проверенный б/у?",
        "Да. Б/у проходит осмотр: рама, кабина, двигатель, коробка, мосты. На сайт не выкладываем "
        "чужие VIN и госномера. Фото с площадки и историю по конкретной машине отправляем в заявке.",
    ),
    (
        "Можно ли открыть юрлицо или перевозчика в КР под парк?",
        "Помогаем с маршрутом: компания в Кыргызстане, постановка техники, дальнейшая работа как "
        "перевозчика по ЕАЭС — в том числе международные рейсы для перевозчика, зарегистрированного "
        "в КР. Это отдельный контур, не «гарантия схемы для всех». Обсуждается индивидуально.",
    ),
    (
        "Какая гарантия на FAW?",
        "На новую технику FAW, поставленную официально, действует заводская гарантия и доступ к "
        "запчастям через дилерский канал SPEC-KG. Срок и покрытие — по сертификату и договору на "
        "конкретную модель. Серый импорт мы не продаём как «официальный FAW».",
    ),
    (
        "Кто ваши клиенты?",
        "Физические лица РФ, ИП РФ, ООО и транспортные компании РФ, а также клиенты КР. "
        "Широкий B2B и частные покупатели. Представительства в России нет: офис и склад — в Бишкеке.",
    ),
    (
        "Есть ли лизинг или рассрочка?",
        "Лизинг и рассрочка — по запросу, через партнёра, не как готовый продукт на сайте. "
        "Если нужна финансовая схема, укажите это в заявке: подберём, что реально доступно под сделку.",
    ),
    (
        "Какие схемы покупки вы показываете?",
        "Три рабочих контура, без навязывания одного: покупка на себя в КР; техника на компании КР "
        "(аренда / управление); лизинг или рассрочка через партнёра. Какая схема уместна — зависит "
        "от вас и законодательства. Сайт носит информационный характер.",
    ),
]


def stock_image(filename: str) -> ContentFile | None:
    path = Path(settings.BASE_DIR) / "static" / "img" / "stock" / filename
    if not path.exists():
        return None
    return ContentFile(path.read_bytes(), name=filename)


class Command(BaseCommand):
    help = "Seed brands, categories, 8 vehicles, documents and FAQ"

    @transaction.atomic
    def handle(self, *args, **options):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser("admin", "info@spec-kg.com", "admin")
            self.stdout.write("Created superuser admin / admin — смените пароль после входа")

        brands = {}
        for name, slug, flagship, desc, order in BRANDS:
            obj, _ = Brand.objects.update_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "is_flagship": flagship,
                    "short_description": desc,
                    "sort_order": order,
                },
            )
            brands[slug] = obj

        categories = {}
        for name, slug, order in CATEGORIES:
            obj, _ = Category.objects.update_or_create(
                slug=slug, defaults={"name": name, "sort_order": order}
            )
            categories[slug] = obj

        for data in VEHICLES:
            payload = {**data}
            brand = brands[payload.pop("brand")]
            category = categories[payload.pop("category")]
            stock_file = payload.pop("stock_file")
            vehicle, created = Vehicle.objects.update_or_create(
                slug=payload["slug"],
                defaults={
                    **payload,
                    "brand": brand,
                    "category": category,
                    "use_placeholder": False,
                    "is_published": True,
                    "is_featured": True,
                },
            )
            image = stock_image(stock_file)
            if image:
                if vehicle.main_image:
                    vehicle.main_image.delete(save=False)
                vehicle.main_image.save(f"{vehicle.slug}.jpg", image, save=True)
            status = "created" if created else "updated"
            self.stdout.write(f"  vehicle {status}: {vehicle.name}")

        for i, (title, desc) in enumerate(DOCUMENTS, start=1):
            Document.objects.update_or_create(
                title=title,
                defaults={"description": desc, "is_placeholder": True, "sort_order": i},
            )

        FAQ.objects.all().delete()
        for i, (q, a) in enumerate(FAQS, start=1):
            FAQ.objects.create(question=q, answer=a, sort_order=i, is_published=True)

        media = Path(settings.MEDIA_ROOT)
        (media / "vehicles").mkdir(parents=True, exist_ok=True)
        (media / "documents").mkdir(parents=True, exist_ok=True)

        self.stdout.write(self.style.SUCCESS("Seed complete: 8 vehicles, documents, FAQ."))
