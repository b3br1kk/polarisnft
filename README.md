# Полярис — многостраничная демоверсия

## Структура
- `index.html` — главная страница.
- `services/index.html` — каталог услуг.
- `services/pdr.html`, `air-conditioner.html`, `autoelectric.html`, `glass-repair.html`, `car-soundproofing.html`, `car-alarms.html`, `air-heaters.html` — отдельные страницы услуг.
- `partners/index.html` и шесть страниц производителей оборудования.
- `avtopodbor.html`, `reviews.html`, `contacts.html`, `privacy.html` — дополнительные страницы.
- `css/site.css` — общие стили сайта и встроенные фирменные фоновые ресурсы.
- `data/rating.json`, `scripts/parse_2gis.py`, `.github/workflows/update-rating.yml` — механизм обновления статистики 2ГИС.

## Локальный просмотр
Открой `index.html` в браузере. Все внутренние ссылки относительные. Для тестирования ежедневного обновления рейтинга репозиторий следует загрузить на GitHub и запустить workflow вручную.

## Перед публикацией
1. Согласовать фактические цены, часы работы и тексты услуг. Цены отмечены как демонстрационные.
2. Проверить актуальность рейтинга/отзывов и успешность парсера 2ГИС в GitHub Actions.
3. Проверить формы на реальном хостинге. Обработчик заявок на сервер не добавлен; форма открывает WhatsApp с подготовленным текстом.
4. Проверить согласие и политику обработки персональных данных с владельцем сайта.
5. Сохранить существующие URL или настроить перенаправления при публикации, если демо станет заменой действующего сайта.

## Важно
Это концепт для согласования с владельцем. Не публикуйте неподтверждённые отзывы, рейтинги, цены или сведения о компании как окончательные данные.


## Update v2
- Clean service cards on the homepage (titles only).
- Full-width layout and differentiated section backgrounds.
- Partner logos shown on the brands directory.
- Service booking buttons preselect the current service in the demo form.
