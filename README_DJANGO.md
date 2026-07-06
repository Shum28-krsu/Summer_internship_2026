# Станция мониторинга — Django-версия

Веб-интерфейс на Django поверх схемы `stations` / `observations` из SQLite-этапа
практики. Позволяет смотреть станции, наблюдения (с фильтрами по параметру и
периоду) и сводную статистику через браузер, плюс готовая админ-панель.

## Структура проекта

```
django_project/
├── manage.py
├── requirements.txt
├── db.sqlite3                      ← готовая база с тестовыми данными
├── monitoring_project/             ← настройки проекта
│   ├── settings.py
│   └── urls.py
└── monitoring/                     ← приложение
    ├── models.py                   ← Station, Observation
    ├── admin.py                    ← регистрация в админке
    ├── views.py                    ← stations_list, station_detail, dashboard
    ├── urls.py
    ├── management/commands/
    │   └── load_seed_data.py       ← загрузка тестовых данных
    └── templates/monitoring/
        ├── base.html
        ├── stations_list.html
        ├── station_detail.html
        └── dashboard.html
```

## Как запустить в VS Code

1. Открой папку `django_project` в VS Code (**File → Open Folder**).
2. Открой терминал (`` Ctrl+` ``) и установи зависимости:
   ```bash
   pip install -r requirements.txt --break-system-packages
   ```
   (флаг `--break-system-packages` нужен на некоторых системах с Python 3.12; на Windows обычно не требуется — тогда просто `pip install -r requirements.txt`)

3. База данных `db.sqlite3` уже создана и заполнена тестовыми данными.
   Если нужно пересобрать с нуля:
   ```bash
   python manage.py migrate
   python manage.py load_seed_data
   ```

4. Запусти сервер разработки:
   ```bash
   python manage.py runserver
   ```
5. Открой в браузере:
   - http://127.0.0.1:8000/ — список станций
   - http://127.0.0.1:8000/dashboard/ — сводка (count/min/max/avg)
   - http://127.0.0.1:8000/station/1/ — детали станции с фильтрами
   - http://127.0.0.1:8000/admin/ — админ-панель (нужен суперпользователь)

6. Чтобы зайти в админку, создай суперпользователя:
   ```bash
   python manage.py createsuperuser
   ```
   и следуй подсказкам (логин, email, пароль).

## Что реализовано

- **Модели** — `Station` и `Observation`, повторяют схему `stations.sql` (внешний ключ, choices для parameter).
- **Django Templates** — `base.html` с наследованием, страницы списка, деталей и сводки.
- **Views** — function-based views: список, детали с фильтрацией по параметру/периоду через GET-параметры, сводка через агрегатные функции ORM (`Count`, `Min`, `Max`, `Avg` — аналог SQL-запроса №4).
- **Django Admin** — `Station` и `Observation` зарегистрированы, с inline-редактированием наблюдений прямо на странице станции.
- **Management-команда** `load_seed_data` — переносит те же тестовые данные, что были в `seed_data.sql` (3 станции, 18 наблюдений).

## Что можно добавить дальше

- Форма добавления наблюдения через `ModelForm` (сейчас данные только через admin или management-команду).
- Docker Compose с PostgreSQL вместо SQLite.
- REST API (Django REST Framework) для отдачи данных в JSON.
- Пагинация для длинных списков наблюдений.
