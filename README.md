# SPEC-KG

Сайт компании SPEC-KG (Бишкек): коммерческая и спецтехника, официальный дилер FAW, пакет под ключ с оформлением в Кыргызстане.

Стек: Django 5, шаблоны Django, SQLite для разработки, PostgreSQL через `DATABASE_URL`, WhiteNoise, админка.

## Быстрый запуск (локально)

Нужен Python 3.12+.

```bash
cd SPECKG
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py seed
python manage.py runserver
```

Открыть:

- сайт: http://127.0.0.1:8000/
- админка: http://127.0.0.1:8000/admin/

После `seed` создаётся суперпользователь **admin / admin**. Смените пароль сразу после первого входа.

Команда `seed` наполняет 8 единиц техники, бренды, типы, FAQ и заглушки документов. Повторный запуск обновляет записи по slug, не плодит дубли.

## Что менять без правки шаблонов

Файл `.env` (шаблон — `.env.example`):

- контакты: телефон, WhatsApp, Telegram, email, город
- курс-заглушка `EXCHANGE_USD_RUB` для калькулятора и кнопки «расчёт в ₽»
- `TELEGRAM_BOT_TOKEN` и `TELEGRAM_CHAT_ID` — заявки уходят в Telegram; пока пусто, пишутся в лог и в админку, сайт не падает
- `DATABASE_URL` — если задан, используется PostgreSQL, иначе SQLite `db.sqlite3`

Технику, бренды, заявки и документы добавляйте в Django Admin.

## Заявки

Формы: оставить заявку, запросить машину, рассчитать выгоду, заказать звонок. CSRF + honeypot. Статусы заявки: новая / в работе / закрыта.

Кнопка Telegram ведёт на `https://t.me/tazhibaevn` (меняется в `.env`). WhatsApp: `https://wa.me/996506055056`.

## Бесплатный деплой (сайт + админка + фото)

Чтобы сохранить **админку, заявки и каталог**, нужна Postgres. Бесплатные варианты:

| Сервис | Что даёт | Ограничение |
|---|---|---|
| **Render** (рекомендуем) | Сайт, HTTPS, gunicorn | Бесплатный веб засыпает ~15 мин |
| **Neon** или **Supabase** | Бесплатная Postgres навсегда | Лимит места (~0.5 ГБ, хватит) |
| PythonAnywhere | Сайт + файлы на диске | Слабый CPU, свой домен ограничен |
| Railway / Fly.io / Koyeb | Тоже Django | Кредит или лимит часов |

**Не подходят:** Vercel и Netlify — это фронтенд, Django с админкой и медиа там ломается.

### Render + Neon (бесплатно)

1. Создайте репозиторий на GitHub и залейте этот проект.
2. База: [neon.tech](https://neon.tech) → New Project → скопируйте `DATABASE_URL`.
3. Сайт: [dashboard.render.com](https://dashboard.render.com) → New → Web Service → ваш репозиторий.
   - Runtime: Python
   - Build: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - Start: `bash start.sh`
   - Instance: Free
4. Environment на Render:

```
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=<случайная длинная строка>
DATABASE_URL=<строка из Neon>
```

Render сам подставит хост. После деплоя:

- сайт: `https://<имя>.onrender.com/`
- админка: `https://<имя>.onrender.com/admin/`
- логин после `seed`: **admin / admin** — сразу смените пароль

`start.sh` делает migrate, заливает 8 машин с теми же фото из `static/img/stock/`, поднимает gunicorn. WhiteNoise отдаёт CSS/JS — анимации сохраняются. Фото каталога копируются в `media/` при старте.

Если загрузите **новое** фото через админку на бесплатном Render, после перезапуска оно пропадёт (диск временный). Штатные 8 фото живут в репозитории и восстанавливаются при `seed`. Новые фото лучше класть в `static/img/stock/` и прописывать в `seed.py`.

## Docker (VPS)

```bash
cp .env.example .env
docker compose up --build
```

Поднимаются PostgreSQL и gunicorn на порту 8000. Медиа раздаёт Django только при `DJANGO_DEBUG=True`; на проде повесьте Nginx на `/media/` и `/static/` (или оставьте WhiteNoise для статики).

После первого запуска контейнера:

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py seed
```

## Структура

```
config/       настройки, URL, middleware заголовков
pages/        главная, FAW, почему КР, услуги, о компании, документы, FAQ, контакты, политика
catalog/      бренды, типы, техника, сиды
leads/        заявки, формы, заготовка Telegram
calculator/   ориентировочный расчёт выгоды
templates/    Django templates
static/       CSS, JS, логотип SVG
media/        фото техники (после seed)
```

## Юридическая рамка сайта

На сайте нет формулировок «обход утиля», «гарантированно без налогов», юридических гарантий схемы. Дисклеймер в подвале и в политике конфиденциальности. Полное юрлицо, ИНН и улица не публикуются.

## SEO

`title` / `description` на страницах, Open Graph, `/sitemap.xml`, `/robots.txt`.
