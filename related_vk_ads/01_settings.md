# 01 · Настройки VK-кампании — полные значения

Снято чтением объектов из API после создания (18.11.2026), не из памяти.
Кабинет: `account_id 672134` (UID_2044680_Реклама в VK), валюта RUB, баланс 4 072,05 ₽.

## Кампания (ad_plan 42017182)

| Поле API | Значение | Комментарий |
|---|---|---|
| `name` | Finindi — VK Ads — основной тест | как в задании |
| `status` | `blocked` | остановлена |
| `objective` | `site_conversions` | цель «Сайт», конверсии |
| `date_start` | `2026-11-13` | как в РСЯ-кампании 716189770 |
| `date_end` | `null` | без ограничения |
| `budget_limit_day` | `750` | ₽/день |
| `budget_limit` | `null` | общий бюджет не задан |
| `autobidding_mode` | `null` | не применяется для CPC-пакета |
| `delivery` | `not_delivering` | причина: `STOPPED` (остановлена вручную) |

## Группа (campaign 168570772)

| Поле API | Значение |
|---|---|
| `name` | Основная аудитория · собственники, руководители, финансы |
| `status` | `blocked` |
| `package_id` | `3232` (`or_tt_crossdevice_site_multiformat_all_cpc_conversions`) |
| `package_priced_event_type` | `1` — оплата за клики (CPC) |
| `objective` | `site_conversions` |
| `budget_limit_day` | `750` |
| `date_start` | `2026-11-13` |
| `date_end` | `null` |
| `enable_utm` | `true` |
| `utm` | `utm_source=vk_ads&utm_medium=cpc&utm_campaign=finindi_vk&utm_content={{banner_id}}` |
| `priced_goal` | не задан |

### Таргетинги группы

| Поле API | Значение | Расшифровка |
|---|---|---|
| `geo.regions` | `[188]` | Россия (вся) |
| `age.age_list` | `20…45` (26 значений) | строго 20–45, по годам |
| `age.expand` | `false` | без расширения возраста |
| `sex` | `["male", "female"]` | все |
| `interests` | `8493, 8962, 8494, 7404, 7403, 7402, 25267, 9381, 10263` | тематические интересы, внутри — «ИЛИ» |
| `interests_soc_dem` | `24824, 9080, 24826, 9073` | профессия/отдел, внутри — «ИЛИ» |
| `fulltime.flags` | `["cross_timezone"]` | расписание по местному времени пользователя |
| `fulltime.mon…sun` | `7…22` | 07:00–23:00 ежедневно (слоты часов) |
| `pads` | 24 площадки | VK подставил автоматически по пакету (мультиформат) |
| `group_members` | `not_group_member` | значение VK по умолчанию |
| `segments` | нет | ретаргетинг не использовался |
| `device_types` / `mobile_types` | не заданы | все устройства |

## Объявление (banner 252858750)

| Поле API | Значение |
|---|---|
| `name` | cr_karta_600x600_v1 |
| `status` | `blocked` |
| `moderation_status` | `pending` (ожидает модерации) |
| `urls.primary.url` | `https://finindi.ru/` (url object id 135461900) |
| `content.icon_256x256.id` | `133960746` (256×256, 9 919 Б) |
| `content.image_600x600.id` | `133960892` (600×600, 112 559 Б) |
| `textblocks.title_40_vkads.text` | Инвестиционные показатели без воды |
| `textblocks.text_90.text` | Собственнику и директору: формулы, примеры, ориентиры. Гид 490 ₽ или комплект 990 ₽. |
| `textblocks.text_long.text` | см. README п. 7 (383 знака) |
| `textblocks.cta_sites_full.text` | `buy` («Купить») |
| `ord_marker` | пусто — маркировку присвоит VK после проверки/активации |

## Технические примечания

- Пакет 3232 — мультиформатный, поэтому объявление автоматически получает ленту, боковые, нативные и другие площадки пакета; отдельные `pads` не ограничивались.
- `cta_sites_full` в API — это текстблок с кодом кнопки, а не поле `call_to_action` (оно `null`). Код `buy` принят VK; в интерфейсе кнопка отображается как «Купить».
- Смена `objective`, `package_id` и `priced_goal` после запуска невозможна — только пересоздание.
